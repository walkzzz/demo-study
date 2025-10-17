"""基础智能体类

所有专业智能体的基类，提供通用功能
"""

import logging
from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod
import yaml

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """基础智能体抽象类"""
    
    def __init__(
        self,
        name: str,
        model_manager,
        prompt_engine,
        memory_manager,
        tools,
        config: Optional[Dict[str, Any]] = None
    ):
        """初始化智能体
        
        Args:
            name: 智能体名称
            model_manager: 模型管理器
            prompt_engine: 提示词引擎
            memory_manager: 记忆管理器
            tools: 工具实例
            config: 配置信息
        """
        self.name = name
        self.model_manager = model_manager
        self.prompt_engine = prompt_engine
        self.memory_manager = memory_manager
        self.tools = tools
        self.config = config or {}
        
        # 从配置中读取智能体参数
        self.model_name = self.config.get("model_name", "llama3:8b")
        self.temperature = self.config.get("temperature", 0.7)
        self.max_iterations = self.config.get("max_iterations", 10)
        self.memory_enabled = self.config.get("memory_enabled", True)
        self.reflection_enabled = self.config.get("reflection_enabled", True)
        
        logger.info(f"{self.name} 初始化完成")
    
    @abstractmethod
    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """执行任务
        
        Args:
            task: 任务信息
            
        Returns:
            执行结果
        """
        pass
    
    def plan(self, task: Dict[str, Any]) -> List[Dict[str, Any]]:
        """规划执行步骤
        
        Args:
            task: 任务信息
            
        Returns:
            执行步骤列表
        """
        logger.info(f"{self.name} 规划任务")
        
        # 使用LLM生成执行计划
        prompt = f"""任务: {task.get('description', '')}
        
请规划具体的执行步骤。

输出格式:
1. 步骤1
2. 步骤2
..."""
        
        messages = [{"role": "user", "content": prompt}]
        response = self.model_manager.invoke(
            messages,
            model_name=self.model_name,
            temperature=self.temperature
        )
        
        # 解析响应为步骤列表
        steps = []
        for line in response.split('\n'):
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('-')):
                steps.append({"description": line, "status": "pending"})
        
        return steps
    
    def select_tool(self, task: str, available_tools: List[Dict[str, Any]]) -> Dict[str, Any]:
        """选择合适的工具
        
        Args:
            task: 当前任务
            available_tools: 可用工具列表
            
        Returns:
            工具选择结果
        """
        logger.debug(f"{self.name} 选择工具")
        
        prompt = self.prompt_engine.render_tool_selection(task, available_tools)
        messages = [{"role": "user", "content": prompt}]
        
        response = self.model_manager.invoke(
            messages,
            model_name=self.model_name,
            temperature=0.3
        )
        
        # TODO: 解析JSON响应
        return {"tool_name": "default_tool", "parameters": {}, "reason": "示例"}
    
    def reflect(self, task: str, history: List[str], result: str) -> Dict[str, Any]:
        """反思执行结果
        
        Args:
            task: 任务目标
            history: 执行历史
            result: 当前结果
            
        Returns:
            反思结果
        """
        if not self.reflection_enabled:
            return {"should_retry": False}
        
        logger.info(f"{self.name} 反思执行结果")
        
        prompt = self.prompt_engine.render_reflection(task, history, result)
        messages = [{"role": "user", "content": prompt}]
        
        response = self.model_manager.invoke(
            messages,
            model_name=self.model_name,
            temperature=0.3
        )
        
        # TODO: 解析JSON响应
        return {
            "quality_score": 0.8,
            "meets_goal": True,
            "should_retry": False
        }
    
    def save_memory(self, key: str, value: Any):
        """保存记忆
        
        Args:
            key: 键
            value: 值
        """
        if self.memory_enabled:
            self.memory_manager.save_knowledge(key, value, category=self.name.lower())
    
    def get_memory(self, key: str) -> Optional[Any]:
        """获取记忆
        
        Args:
            key: 键
            
        Returns:
            值
        """
        if self.memory_enabled:
            return self.memory_manager.get_knowledge(key, category=self.name.lower())
        return None
