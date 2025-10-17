"""超级智能体协调器

作为系统中枢，接收用户任务并调度专业智能体
"""

import logging
from typing import Dict, Any, Optional
import yaml

logger = logging.getLogger(__name__)


class SuperAgent:
    """超级智能体协调器"""
    
    def __init__(
        self,
        model_manager,
        prompt_engine,
        memory_manager,
        task_planner,
        agents: Dict[str, Any]
    ):
        """初始化超级智能体
        
        Args:
            model_manager: 模型管理器
            prompt_engine: 提示词引擎
            memory_manager: 记忆管理器
            task_planner: 任务规划器
            agents: 专业智能体字典
        """
        self.model_manager = model_manager
        self.prompt_engine = prompt_engine
        self.memory_manager = memory_manager
        self.task_planner = task_planner
        self.agents = agents
        
        logger.info("超级智能体初始化完成")
    
    def process_request(self, user_input: str) -> Dict[str, Any]:
        """处理用户请求
        
        Args:
            user_input: 用户输入
            
        Returns:
            处理结果
        """
        logger.info(f"处理用户请求: {user_input[:50]}...")
        
        try:
            # 1. 任务理解
            task_understanding = self._understand_task(user_input)
            logger.info(f"任务理解: {task_understanding.get('intent')}")
            
            # 2. 任务分解
            subtasks = self.task_planner.decompose_task(task_understanding)
            logger.info(f"任务分解: {len(subtasks)} 个子任务")
            
            # 3. 执行子任务
            results = []
            for subtask in subtasks:
                result = self._execute_subtask(subtask)
                results.append(result)
            
            # 4. 结果聚合
            final_result = self._aggregate_results(results)
            
            # 5. 保存到记忆
            self.memory_manager.add_message("user", user_input)
            self.memory_manager.add_message("assistant", str(final_result))
            
            return {
                "status": "success",
                "result": final_result,
                "task_understanding": task_understanding,
                "subtasks_count": len(subtasks)
            }
            
        except Exception as e:
            logger.error(f"处理请求失败: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def _understand_task(self, user_input: str) -> Dict[str, Any]:
        """理解任务
        
        Args:
            user_input: 用户输入
            
        Returns:
            任务理解结果
        """
        prompt = self.prompt_engine.render_task_understanding(user_input)
        messages = [{"role": "user", "content": prompt}]
        
        response = self.model_manager.invoke(
            messages,
            task_type="task_understanding"
        )
        
        # TODO: 解析JSON响应
        # 这里返回简化的结果
        return {
            "intent": "执行用户任务",
            "entities": {},
            "priority": "medium",
            "required_agents": self._identify_required_agents(user_input),
            "confidence": 0.9,
            "original_input": user_input
        }
    
    def _identify_required_agents(self, user_input: str) -> list:
        """识别需要的智能体"""
        agents = []
        
        if any(keyword in user_input.lower() for keyword in ['邮件', 'email', '回复']):
            agents.append('email')
        if any(keyword in user_input.lower() for keyword in ['文档', 'document', '合同', '报告']):
            agents.append('doc')
        if any(keyword in user_input.lower() for keyword in ['日程', 'schedule', '会议', '安排']):
            agents.append('schedule')
        if any(keyword in user_input.lower() for keyword in ['数据', 'data', '分析', '图表']):
            agents.append('data')
        if any(keyword in user_input.lower() for keyword in ['文件', 'file', '整理', '重复']):
            agents.append('file')
        if any(keyword in user_input.lower() for keyword in ['知识', '问答', '查询']):
            agents.append('knowledge')
        
        return agents if agents else ['knowledge']  # 默认使用知识问答
    
    def _execute_subtask(self, subtask: Dict[str, Any]) -> Dict[str, Any]:
        """执行子任务
        
        Args:
            subtask: 子任务信息
            
        Returns:
            执行结果
        """
        agent_type = subtask.get('agent_type', 'knowledge')
        
        # 路由到对应的智能体
        if agent_type in self.agents:
            agent = self.agents[agent_type]
            result = agent.execute(subtask)
            logger.info(f"子任务执行完成: {agent_type}")
            return result
        else:
            logger.warning(f"未找到智能体: {agent_type}")
            return {"status": "error", "message": f"未找到智能体: {agent_type}"}
    
    def _aggregate_results(self, results: list) -> str:
        """聚合结果
        
        Args:
            results: 结果列表
            
        Returns:
            聚合后的结果
        """
        # 简单的结果合并
        if not results:
            return "未获取到执行结果"
        
        if len(results) == 1:
            return str(results[0].get('result', results[0]))
        
        # 多个结果
        aggregated = "任务执行完成:\n\n"
        for i, result in enumerate(results, 1):
            aggregated += f"{i}. {result.get('status', 'unknown')}\n"
        
        return aggregated
