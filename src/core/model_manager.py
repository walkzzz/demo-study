"""Ollama 模型管理器

负责与 Ollama 服务交互，管理模型调用、参数配置和响应解析
"""

import logging
from typing import Dict, Any, Optional, List
import yaml
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

logger = logging.getLogger(__name__)


class ModelManager:
    """Ollama 模型管理器"""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        """初始化模型管理器
        
        Args:
            config_path: 配置文件路径
        """
        self.config = self._load_config(config_path)
        self.ollama_config = self.config.get("ollama", {})
        self.model_strategies = self.config.get("model_strategy", {})
        self.models: Dict[str, ChatOllama] = {}
        
        logger.info(f"模型管理器初始化完成，Ollama服务地址: {self.ollama_config.get('base_url')}")
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """加载配置文件
        
        Args:
            config_path: 配置文件路径
            
        Returns:
            配置字典
        """
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"加载配置文件失败: {e}")
            return {}
    
    def get_model(
        self, 
        task_type: Optional[str] = None,
        model_name: Optional[str] = None,
        **kwargs
    ) -> ChatOllama:
        """获取模型实例
        
        Args:
            task_type: 任务类型 (task_understanding, document_summary, email_reply等)
            model_name: 指定模型名称，优先级高于task_type
            **kwargs: 其他模型参数
            
        Returns:
            ChatOllama实例
        """
        # 确定使用的模型配置
        if model_name:
            # 使用指定模型
            model_config = {
                "model": model_name,
                "temperature": kwargs.get("temperature", 0.7),
                "top_p": kwargs.get("top_p", 0.9),
            }
        elif task_type and task_type in self.model_strategies:
            # 使用任务类型对应的策略
            model_config = self.model_strategies[task_type].copy()
        else:
            # 使用默认模型
            model_config = {
                "model": self.ollama_config.get("default_model", "llama3:8b"),
                "temperature": 0.7,
                "top_p": 0.9,
            }
        
        # 覆盖配置参数
        model_config.update(kwargs)
        
        # 生成缓存key
        cache_key = f"{model_config['model']}_{model_config.get('temperature', 0.7)}"
        
        # 检查缓存
        if cache_key in self.models:
            logger.debug(f"使用缓存的模型实例: {cache_key}")
            return self.models[cache_key]
        
        # 创建新模型实例
        try:
            model = ChatOllama(
                base_url=self.ollama_config.get("base_url", "http://localhost:11434"),
                model=model_config["model"],
                temperature=model_config.get("temperature", 0.7),
                top_p=model_config.get("top_p", 0.9),
                num_predict=model_config.get("max_tokens", 2000),
                timeout=self.ollama_config.get("timeout", 300),
            )
            
            # 缓存模型实例
            self.models[cache_key] = model
            logger.info(f"创建新模型实例: {model_config['model']}")
            
            return model
            
        except Exception as e:
            logger.error(f"创建模型实例失败: {e}")
            raise
    
    def invoke(
        self,
        messages: List[Dict[str, str]],
        task_type: Optional[str] = None,
        model_name: Optional[str] = None,
        **kwargs
    ) -> str:
        """调用模型生成响应
        
        Args:
            messages: 消息列表，格式 [{"role": "system/user/assistant", "content": "..."}]
            task_type: 任务类型
            model_name: 模型名称
            **kwargs: 其他参数
            
        Returns:
            模型响应文本
        """
        try:
            # 获取模型实例
            model = self.get_model(task_type=task_type, model_name=model_name, **kwargs)
            
            # 转换消息格式
            langchain_messages = []
            for msg in messages:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                
                if role == "system":
                    langchain_messages.append(SystemMessage(content=content))
                elif role == "user":
                    langchain_messages.append(HumanMessage(content=content))
                elif role == "assistant":
                    langchain_messages.append(AIMessage(content=content))
            
            # 调用模型
            logger.debug(f"调用模型，消息数量: {len(langchain_messages)}")
            response = model.invoke(langchain_messages)
            
            # 提取响应内容
            result = response.content if hasattr(response, 'content') else str(response)
            logger.debug(f"模型响应长度: {len(result)} 字符")
            
            return result
            
        except Exception as e:
            logger.error(f"模型调用失败: {e}")
            raise
    
    async def ainvoke(
        self,
        messages: List[Dict[str, str]],
        task_type: Optional[str] = None,
        model_name: Optional[str] = None,
        **kwargs
    ) -> str:
        """异步调用模型生成响应
        
        Args:
            messages: 消息列表
            task_type: 任务类型
            model_name: 模型名称
            **kwargs: 其他参数
            
        Returns:
            模型响应文本
        """
        try:
            model = self.get_model(task_type=task_type, model_name=model_name, **kwargs)
            
            # 转换消息格式
            langchain_messages = []
            for msg in messages:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                
                if role == "system":
                    langchain_messages.append(SystemMessage(content=content))
                elif role == "user":
                    langchain_messages.append(HumanMessage(content=content))
                elif role == "assistant":
                    langchain_messages.append(AIMessage(content=content))
            
            # 异步调用模型
            response = await model.ainvoke(langchain_messages)
            result = response.content if hasattr(response, 'content') else str(response)
            
            return result
            
        except Exception as e:
            logger.error(f"异步模型调用失败: {e}")
            raise
    
    def clear_cache(self):
        """清除模型缓存"""
        self.models.clear()
        logger.info("模型缓存已清除")
