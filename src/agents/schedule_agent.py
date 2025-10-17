"""日程智能体 - 处理日程管理任务"""
import logging
from typing import Dict, Any
from .base_agent import BaseAgent

logger = logging.getLogger(__name__)

class ScheduleAgent(BaseAgent):
    """日程智能体"""
    
    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """执行日程任务"""
        logger.info(f"{self.name} 执行任务: {task.get('description')}")
        
        task_type = task.get('type', 'unknown')
        
        if task_type == 'get_schedule':
            schedule = self.tools.get_schedule(task.get('start_date'), task.get('end_date'))
            return {"status": "success", "schedule": schedule}
        elif task_type == 'create_event':
            event_id = self.tools.create_event(task.get('event'))
            return {"status": "success", "event_id": event_id}
        elif task_type == 'suggest_time':
            suggestions = self.tools.suggest_time(
                task.get('participants', []),
                task.get('duration', 60),
                task.get('constraints', {})
            )
            return {"status": "success", "suggestions": suggestions}
        else:
            return {"status": "error", "message": f"未知任务类型: {task_type}"}
