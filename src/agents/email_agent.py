"""邮件智能体 - 处理邮件相关任务"""
import logging
from typing import Dict, Any
from .base_agent import BaseAgent

logger = logging.getLogger(__name__)

class EmailAgent(BaseAgent):
    """邮件智能体"""
    
    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """执行邮件任务"""
        logger.info(f"{self.name} 执行任务: {task.get('description')}")
        
        task_type = task.get('type', 'unknown')
        
        if task_type == 'read_emails':
            return self._read_emails(task)
        elif task_type == 'classify':
            return self._classify_emails(task)
        elif task_type == 'reply':
            return self._generate_reply(task)
        elif task_type == 'archive':
            return self._archive_emails(task)
        else:
            return {"status": "error", "message": f"未知任务类型: {task_type}"}
    
    def _read_emails(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """读取邮件"""
        emails = self.tools.read_emails(
            account=task.get('account', ''),
            password=task.get('password', ''),
            time_range=task.get('time_range'),
            filters=task.get('filters')
        )
        return {"status": "success", "emails": emails}
    
    def _classify_emails(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """分类邮件"""
        emails = task.get('emails', [])
        classified = []
        
        for email in emails:
            classification = self.tools.classify_email(email)
            email['classification'] = classification
            classified.append(email)
        
        return {"status": "success", "classified_emails": classified}
    
    def _generate_reply(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """生成回复"""
        draft = self.tools.draft_reply(
            original_email=task.get('email'),
            reply_intent=task.get('intent', '感谢并确认')
        )
        return {"status": "success", "draft": draft}
    
    def _archive_emails(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """归档邮件"""
        result = self.tools.archive_emails(
            account=task.get('account', ''),
            password=task.get('password', ''),
            email_ids=task.get('email_ids', [])
        )
        return {"status": "success", "result": result}
