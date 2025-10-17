"""文件系统管理智能体 - 处理文件整理任务"""
import logging
from typing import Dict, Any
from .base_agent import BaseAgent

logger = logging.getLogger(__name__)

class FileAgent(BaseAgent):
    """文件系统管理智能体"""
    
    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """执行文件管理任务"""
        logger.info(f"{self.name} 执行任务: {task.get('description')}")
        
        task_type = task.get('type', 'unknown')
        
        if task_type == 'organize':
            return self._organize_files(task)
        elif task_type == 'detect_duplicates':
            return self._detect_duplicates(task)
        elif task_type == 'clean_temp':
            return self._clean_temp_files(task)
        elif task_type == 'search':
            return self._search_files(task)
        elif task_type == 'analyze_storage':
            return self._analyze_storage(task)
        else:
            return {"status": "error", "message": f"未知任务类型: {task_type}"}
    
    def _organize_files(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """整理文件"""
        result = self.tools.organize_files(
            source_dir=task.get('directory', ''),
            strategy=task.get('strategy', 'by_type'),
            dry_run=task.get('dry_run', True)
        )
        return {"status": "success", "result": result}
    
    def _detect_duplicates(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """检测重复文件"""
        duplicates = self.tools.detect_duplicates(
            directory=task.get('directory', ''),
            method=task.get('method', 'hash')
        )
        return {"status": "success", "duplicates": duplicates, "groups_count": len(duplicates)}
    
    def _clean_temp_files(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """清理临时文件"""
        result = self.tools.clean_temp_files(
            directory=task.get('directory', ''),
            patterns=task.get('patterns')
        )
        return {"status": "success", "result": result}
    
    def _search_files(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """搜索文件"""
        results = self.tools.search_files(
            search_root=task.get('directory', ''),
            keyword=task.get('keyword', ''),
            file_types=task.get('file_types')
        )
        return {"status": "success", "files": results, "count": len(results)}
    
    def _analyze_storage(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """分析磁盘空间"""
        report = self.tools.analyze_storage(task.get('directory', ''))
        return {"status": "success", "report": report}
