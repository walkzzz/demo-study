"""记忆管理系统

实现短期记忆、长期记忆和工作记忆的管理
"""

import logging
import json
import os
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path
import yaml

logger = logging.getLogger(__name__)


class MemoryManager:
    """记忆管理器"""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        """初始化记忆管理器
        
        Args:
            config_path: 配置文件路径
        """
        self.config = self._load_config(config_path)
        self.memory_config = self.config.get("memory", {})
        self.store_path = Path(self.memory_config.get("store_path", "./data/memory"))
        
        # 确保存储目录存在
        self.store_path.mkdir(parents=True, exist_ok=True)
        
        # 短期记忆(对话上下文)
        self.short_term_memory: List[Dict[str, Any]] = []
        self.max_short_term = self.memory_config.get("max_short_term_messages", 50)
        
        # 长期记忆(持久化知识)
        self.long_term_memory_file = self.store_path / "long_term_memory.json"
        self.long_term_memory: Dict[str, Any] = self._load_long_term_memory()
        
        # 工作记忆(任务执行状态)
        self.working_memory: Dict[str, Any] = {}
        
        logger.info(f"记忆管理器初始化完成，存储路径: {self.store_path}")
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """加载配置文件"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"加载配置文件失败: {e}")
            return {}
    
    def _load_long_term_memory(self) -> Dict[str, Any]:
        """加载长期记忆"""
        if self.long_term_memory_file.exists():
            try:
                with open(self.long_term_memory_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"加载长期记忆失败: {e}")
                return {}
        return {}
    
    def _save_long_term_memory(self):
        """保存长期记忆"""
        try:
            with open(self.long_term_memory_file, 'w', encoding='utf-8') as f:
                json.dump(self.long_term_memory, f, ensure_ascii=False, indent=2)
            logger.debug("长期记忆已保存")
        except Exception as e:
            logger.error(f"保存长期记忆失败: {e}")
    
    # ========== 短期记忆管理 ==========
    
    def add_message(self, role: str, content: str, metadata: Optional[Dict] = None):
        """添加消息到短期记忆
        
        Args:
            role: 角色 (user/assistant/system)
            content: 消息内容
            metadata: 元数据
        """
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        
        self.short_term_memory.append(message)
        
        # 限制短期记忆大小
        if len(self.short_term_memory) > self.max_short_term:
            self.short_term_memory = self.short_term_memory[-self.max_short_term:]
        
        logger.debug(f"添加{role}消息到短期记忆")
    
    def get_recent_messages(self, n: int = 10) -> List[Dict[str, Any]]:
        """获取最近的N条消息
        
        Args:
            n: 消息数量
            
        Returns:
            消息列表
        """
        return self.short_term_memory[-n:]
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """获取对话历史(格式化为模型输入)
        
        Returns:
            对话历史列表
        """
        return [
            {"role": msg["role"], "content": msg["content"]}
            for msg in self.short_term_memory
        ]
    
    def clear_short_term(self):
        """清除短期记忆"""
        self.short_term_memory.clear()
        logger.info("短期记忆已清除")
    
    # ========== 长期记忆管理 ==========
    
    def save_knowledge(self, key: str, value: Any, category: str = "general"):
        """保存知识到长期记忆
        
        Args:
            key: 知识键
            value: 知识值
            category: 分类
        """
        if category not in self.long_term_memory:
            self.long_term_memory[category] = {}
        
        self.long_term_memory[category][key] = {
            "value": value,
            "timestamp": datetime.now().isoformat()
        }
        
        self._save_long_term_memory()
        logger.debug(f"保存知识到长期记忆: {category}/{key}")
    
    def get_knowledge(self, key: str, category: str = "general") -> Optional[Any]:
        """从长期记忆检索知识
        
        Args:
            key: 知识键
            category: 分类
            
        Returns:
            知识值，如果不存在返回None
        """
        if category in self.long_term_memory:
            item = self.long_term_memory[category].get(key)
            if item:
                return item.get("value")
        return None
    
    def search_knowledge(self, keyword: str, category: Optional[str] = None) -> List[Dict]:
        """搜索长期记忆中的知识
        
        Args:
            keyword: 关键词
            category: 分类，如果为None则搜索所有分类
            
        Returns:
            匹配的知识列表
        """
        results = []
        categories = [category] if category else self.long_term_memory.keys()
        
        for cat in categories:
            if cat not in self.long_term_memory:
                continue
            
            for key, item in self.long_term_memory[cat].items():
                if keyword.lower() in key.lower() or keyword.lower() in str(item["value"]).lower():
                    results.append({
                        "category": cat,
                        "key": key,
                        "value": item["value"],
                        "timestamp": item["timestamp"]
                    })
        
        return results
    
    def delete_knowledge(self, key: str, category: str = "general"):
        """删除长期记忆中的知识
        
        Args:
            key: 知识键
            category: 分类
        """
        if category in self.long_term_memory:
            if key in self.long_term_memory[category]:
                del self.long_term_memory[category][key]
                self._save_long_term_memory()
                logger.info(f"删除知识: {category}/{key}")
    
    # ========== 工作记忆管理 ==========
    
    def set_task_state(self, task_id: str, state: Dict[str, Any]):
        """设置任务状态到工作记忆
        
        Args:
            task_id: 任务ID
            state: 任务状态
        """
        self.working_memory[task_id] = {
            "state": state,
            "timestamp": datetime.now().isoformat()
        }
        logger.debug(f"设置任务状态: {task_id}")
    
    def get_task_state(self, task_id: str) -> Optional[Dict[str, Any]]:
        """获取任务状态
        
        Args:
            task_id: 任务ID
            
        Returns:
            任务状态，如果不存在返回None
        """
        item = self.working_memory.get(task_id)
        if item:
            return item.get("state")
        return None
    
    def update_task_state(self, task_id: str, updates: Dict[str, Any]):
        """更新任务状态
        
        Args:
            task_id: 任务ID
            updates: 更新的字段
        """
        if task_id in self.working_memory:
            self.working_memory[task_id]["state"].update(updates)
            self.working_memory[task_id]["timestamp"] = datetime.now().isoformat()
            logger.debug(f"更新任务状态: {task_id}")
    
    def clear_task_state(self, task_id: str):
        """清除任务状态
        
        Args:
            task_id: 任务ID
        """
        if task_id in self.working_memory:
            del self.working_memory[task_id]
            logger.debug(f"清除任务状态: {task_id}")
    
    def archive_task(self, task_id: str):
        """归档任务到长期记忆
        
        Args:
            task_id: 任务ID
        """
        if task_id in self.working_memory:
            task_data = self.working_memory[task_id]
            self.save_knowledge(task_id, task_data, category="archived_tasks")
            self.clear_task_state(task_id)
            logger.info(f"任务已归档: {task_id}")
    
    # ========== 工具方法 ==========
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """获取记忆统计信息
        
        Returns:
            统计信息字典
        """
        long_term_count = sum(len(items) for items in self.long_term_memory.values())
        
        return {
            "short_term_messages": len(self.short_term_memory),
            "long_term_knowledge": long_term_count,
            "working_tasks": len(self.working_memory),
            "categories": list(self.long_term_memory.keys())
        }
    
    def export_memory(self, output_path: str):
        """导出所有记忆到文件
        
        Args:
            output_path: 输出文件路径
        """
        export_data = {
            "short_term": self.short_term_memory,
            "long_term": self.long_term_memory,
            "working": self.working_memory,
            "exported_at": datetime.now().isoformat()
        }
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
            logger.info(f"记忆已导出到: {output_path}")
        except Exception as e:
            logger.error(f"导出记忆失败: {e}")
