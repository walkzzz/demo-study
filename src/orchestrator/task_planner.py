"""任务规划器 - 将复杂任务分解为子任务"""
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class TaskPlanner:
    """任务规划器"""
    
    def __init__(self, model_manager, prompt_engine):
        self.model_manager = model_manager
        self.prompt_engine = prompt_engine
        logger.info("任务规划器初始化完成")
    
    def decompose_task(self, task_understanding: Dict[str, Any]) -> List[Dict[str, Any]]:
        """分解任务
        
        Args:
            task_understanding: 任务理解结果
            
        Returns:
            子任务列表
        """
        logger.info("分解任务")
        
        intent = task_understanding.get('intent', '')
        required_agents = task_understanding.get('required_agents', [])
        
        # 根据识别的智能体生成子任务
        subtasks = []
        
        for agent_type in required_agents:
            subtask = {
                "id": f"task_{len(subtasks) + 1}",
                "description": f"{agent_type}相关任务",
                "agent_type": agent_type,
                "type": self._infer_task_type(task_understanding['original_input'], agent_type),
                "inputs": self._extract_inputs(task_understanding, agent_type),
                "dependencies": []
            }
            subtasks.append(subtask)
        
        logger.info(f"生成 {len(subtasks)} 个子任务")
        return subtasks
    
    def _infer_task_type(self, user_input: str, agent_type: str) -> str:
        """推断任务类型"""
        if agent_type == 'email':
            if '读' in user_input or '查' in user_input:
                return 'read_emails'
            elif '回复' in user_input:
                return 'reply'
            elif '归档' in user_input:
                return 'archive'
            return 'classify'
        
        elif agent_type == 'file':
            if '整理' in user_input:
                return 'organize'
            elif '重复' in user_input:
                return 'detect_duplicates'
            elif '搜索' in user_input:
                return 'search'
            elif '分析' in user_input or '空间' in user_input:
                return 'analyze_storage'
            return 'organize'
        
        elif agent_type == 'data':
            if '分析' in user_input:
                return 'analyze'
            elif '图表' in user_input or '可视化' in user_input:
                return 'visualize'
            return 'load_data'
        
        return 'default'
    
    def _extract_inputs(self, task_understanding: Dict[str, Any], agent_type: str) -> Dict[str, Any]:
        """提取输入参数"""
        # 简化版本，从原始输入中提取关键信息
        inputs = {}
        original_input = task_understanding.get('original_input', '')
        
        if agent_type == 'file':
            # 尝试提取目录路径
            if '下载' in original_input:
                inputs['directory'] = '~/Downloads'
            elif '文档' in original_input:
                inputs['directory'] = '~/Documents'
            else:
                inputs['directory'] = '.'
            
            inputs['strategy'] = 'by_type'
            inputs['dry_run'] = True  # 默认预览模式
        
        return inputs
