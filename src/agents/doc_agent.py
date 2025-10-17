"""文档智能体 - 处理文档相关任务"""
import logging
from typing import Dict, Any
from .base_agent import BaseAgent

logger = logging.getLogger(__name__)

class DocAgent(BaseAgent):
    """文档智能体"""
    
    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """执行文档任务"""
        logger.info(f"{self.name} 执行任务: {task.get('description')}")
        
        task_type = task.get('type', 'unknown')
        
        if task_type == 'load':
            return self._load_document(task)
        elif task_type == 'convert':
            return self._convert_format(task)
        elif task_type == 'summarize':
            return self._extract_summary(task)
        elif task_type == 'compare':
            return self._compare_documents(task)
        else:
            return {"status": "error", "message": f"未知任务类型: {task_type}"}
    
    def _load_document(self, task: Dict[str, Any]) -> Dict[str, Any]:
        doc = self.tools.load_document(task.get('file_path', ''))
        return {"status": "success", "document": doc}
    
    def _convert_format(self, task: Dict[str, Any]) -> Dict[str, Any]:
        output = self.tools.convert_format(task.get('source'), task.get('format'))
        return {"status": "success", "output_path": output}
    
    def _extract_summary(self, task: Dict[str, Any]) -> Dict[str, Any]:
        summary = self.tools.extract_summary(task.get('content', ''), task.get('length', 200))
        return {"status": "success", "summary": summary}
    
    def _compare_documents(self, task: Dict[str, Any]) -> Dict[str, Any]:
        result = self.tools.compare_documents(task.get('doc1'), task.get('doc2'))
        return {"status": "success", "comparison": result}
