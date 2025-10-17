"""状态管理器 - 基于LangGraph管理任务执行状态"""
import logging
from typing import Dict, Any, Optional
from enum import Enum

logger = logging.getLogger(__name__)


class TaskStatus(Enum):
    """任务状态枚举"""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    RETRY = "retry"


class StateManager:
    """状态管理器"""
    
    def __init__(self):
        self.states: Dict[str, Dict[str, Any]] = {}
        logger.info("状态管理器初始化完成")
    
    def create_state(self, task_id: str, initial_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """创建任务状态
        
        Args:
            task_id: 任务ID
            initial_data: 初始数据
            
        Returns:
            状态对象
        """
        state = {
            "task_id": task_id,
            "status": TaskStatus.PENDING.value,
            "data": initial_data or {},
            "history": [],
            "current_step": None
        }
        self.states[task_id] = state
        logger.info(f"创建状态: {task_id}")
        return state
    
    def update_state(self, task_id: str, updates: Dict[str, Any]):
        """更新状态
        
        Args:
            task_id: 任务ID
            updates: 更新内容
        """
        if task_id in self.states:
            self.states[task_id].update(updates)
            logger.debug(f"更新状态: {task_id}")
    
    def get_state(self, task_id: str) -> Optional[Dict[str, Any]]:
        """获取状态
        
        Args:
            task_id: 任务ID
            
        Returns:
            状态对象
        """
        return self.states.get(task_id)
    
    def delete_state(self, task_id: str):
        """删除状态
        
        Args:
            task_id: 任务ID
        """
        if task_id in self.states:
            del self.states[task_id]
            logger.info(f"删除状态: {task_id}")
