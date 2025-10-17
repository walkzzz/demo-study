"""提示词引擎

管理和渲染各类提示词模板，支持动态参数注入
"""

import logging
from typing import Dict, Any, List, Optional
from string import Template

logger = logging.getLogger(__name__)


class PromptEngine:
    """提示词引擎"""
    
    # 任务理解提示词模板
    TASK_UNDERSTANDING_TEMPLATE = """你是一个专业的任务分析专家。

任务目标: 分析用户的办公需求并提取关键信息

用户输入: ${user_input}

请按照以下步骤分析:
1. 理解用户意图
2. 识别关键实体(人名、时间、文件等)
3. 确定任务优先级
4. 判断需要哪些智能体参与

请以JSON格式输出分析结果:
{
    "intent": "任务意图描述",
    "entities": {
        "person": ["人名列表"],
        "time": ["时间信息"],
        "file": ["文件路径"],
        "other": ["其他实体"]
    },
    "priority": "high/medium/low",
    "required_agents": ["agent1", "agent2"],
    "confidence": 0.0-1.0
}"""

    # 任务分解提示词模板
    TASK_DECOMPOSITION_TEMPLATE = """你是一个任务规划专家。

任务描述: ${task_description}
任务意图: ${intent}
识别的实体: ${entities}

请将此任务分解为可执行的子任务，每个子任务应该:
- 目标明确
- 可由单个智能体完成
- 有清晰的输入输出

请以JSON格式输出:
{
    "subtasks": [
        {
            "id": "task_1",
            "description": "子任务描述",
            "agent_type": "email/doc/schedule/data/knowledge/file",
            "dependencies": ["依赖的任务ID"],
            "inputs": {"key": "value"},
            "expected_output": "预期输出描述"
        }
    ],
    "execution_order": ["task_1", "task_2"]
}"""

    # 工具选择提示词模板
    TOOL_SELECTION_TEMPLATE = """你是一个能够使用工具的智能助手。

当前任务: ${task}
可用工具列表:
${tools}

请根据任务选择合适的工具并生成调用参数。

注意事项:
- 每次只调用一个工具
- 参数必须完整且符合工具要求
- 如果信息不足，说明需要什么额外信息

请以JSON格式输出:
{
    "tool_name": "工具名称",
    "parameters": {"param1": "value1"},
    "reason": "选择此工具的理由"
}"""

    # 反思优化提示词模板
    REFLECTION_TEMPLATE = """你是一个善于自我反思的智能体。

任务目标: ${task}
执行历史: 
${history}

当前执行结果: ${result}

请评估结果质量并提出改进建议:
1. 结果是否满足任务目标?
2. 是否存在错误或遗漏?
3. 如何改进执行策略?

请以JSON格式输出:
{
    "quality_score": 0.0-1.0,
    "meets_goal": true/false,
    "issues": ["问题1", "问题2"],
    "improvements": ["改进建议1", "改进建议2"],
    "should_retry": true/false,
    "optimized_plan": "优化后的执行计划"
}"""

    # 邮件分类提示词模板
    EMAIL_CLASSIFICATION_TEMPLATE = """请对以下邮件进行分类。

邮件主题: ${subject}
发件人: ${sender}
邮件内容: ${content}

分类标准:
- important: 重要邮件(来自领导、紧急事项、待办任务)
- work: 工作邮件
- notification: 通知类邮件
- spam: 垃圾邮件
- other: 其他

请以JSON格式输出:
{
    "category": "分类结果",
    "priority": "high/medium/low",
    "reason": "分类理由",
    "keywords": ["关键词1", "关键词2"]
}"""

    # 邮件回复生成提示词模板
    EMAIL_REPLY_TEMPLATE = """请根据原邮件生成回复草稿。

原邮件:
主题: ${subject}
发件人: ${sender}
内容: ${content}

回复意图: ${reply_intent}

要求:
- 语气专业礼貌
- 内容简洁明了
- 针对性强

请生成回复邮件正文:"""

    # 文档摘要提取提示词模板
    DOCUMENT_SUMMARY_TEMPLATE = """请为以下文档生成摘要。

文档内容:
${content}

摘要要求:
- 长度: ${length} 字以内
- 保留核心信息
- 结构清晰

请生成摘要:"""

    # 知识问答提示词模板
    KNOWLEDGE_QA_TEMPLATE = """请基于以下上下文回答问题。

问题: ${question}

相关上下文:
${context}

回答要求:
- 基于上下文回答，不要编造
- 如果上下文中没有相关信息，明确说明
- 引用具体的上下文片段

请回答:"""

    # 文件整理策略生成提示词模板
    FILE_ORGANIZE_TEMPLATE = """你是一个文件整理专家。

目录信息:
路径: ${directory}
文件总数: ${total_files}
文件类型分布: ${file_types}

请分析并生成整理策略:
1. 识别主要文件类型
2. 建议分类方式(按类型/日期/项目)
3. 预估整理效果

请以JSON格式输出:
{
    "strategy": "by_type/by_date/by_project",
    "categories": {
        "category_name": {
            "file_count": 100,
            "target_folder": "目标文件夹路径"
        }
    },
    "estimated_improvement": "预估改善效果",
    "warnings": ["注意事项"]
}"""

    def __init__(self):
        """初始化提示词引擎"""
        logger.info("提示词引擎初始化完成")
    
    def render_task_understanding(self, user_input: str) -> str:
        """渲染任务理解提示词
        
        Args:
            user_input: 用户输入
            
        Returns:
            渲染后的提示词
        """
        template = Template(self.TASK_UNDERSTANDING_TEMPLATE)
        return template.safe_substitute(user_input=user_input)
    
    def render_task_decomposition(
        self, 
        task_description: str,
        intent: str,
        entities: Dict[str, Any]
    ) -> str:
        """渲染任务分解提示词
        
        Args:
            task_description: 任务描述
            intent: 任务意图
            entities: 识别的实体
            
        Returns:
            渲染后的提示词
        """
        template = Template(self.TASK_DECOMPOSITION_TEMPLATE)
        return template.safe_substitute(
            task_description=task_description,
            intent=intent,
            entities=str(entities)
        )
    
    def render_tool_selection(self, task: str, tools: List[Dict[str, Any]]) -> str:
        """渲染工具选择提示词
        
        Args:
            task: 当前任务
            tools: 可用工具列表
            
        Returns:
            渲染后的提示词
        """
        # 格式化工具列表
        tools_str = "\n".join([
            f"- {tool['name']}: {tool['description']}\n  参数: {tool.get('parameters', {})}"
            for tool in tools
        ])
        
        template = Template(self.TOOL_SELECTION_TEMPLATE)
        return template.safe_substitute(task=task, tools=tools_str)
    
    def render_reflection(
        self,
        task: str,
        history: List[str],
        result: str
    ) -> str:
        """渲染反思优化提示词
        
        Args:
            task: 任务目标
            history: 执行历史
            result: 当前结果
            
        Returns:
            渲染后的提示词
        """
        history_str = "\n".join([f"{i+1}. {h}" for i, h in enumerate(history)])
        
        template = Template(self.REFLECTION_TEMPLATE)
        return template.safe_substitute(
            task=task,
            history=history_str,
            result=result
        )
    
    def render_email_classification(
        self,
        subject: str,
        sender: str,
        content: str
    ) -> str:
        """渲染邮件分类提示词
        
        Args:
            subject: 邮件主题
            sender: 发件人
            content: 邮件内容
            
        Returns:
            渲染后的提示词
        """
        template = Template(self.EMAIL_CLASSIFICATION_TEMPLATE)
        return template.safe_substitute(
            subject=subject,
            sender=sender,
            content=content[:500]  # 限制内容长度
        )
    
    def render_email_reply(
        self,
        subject: str,
        sender: str,
        content: str,
        reply_intent: str
    ) -> str:
        """渲染邮件回复提示词
        
        Args:
            subject: 原邮件主题
            sender: 发件人
            content: 原邮件内容
            reply_intent: 回复意图
            
        Returns:
            渲染后的提示词
        """
        template = Template(self.EMAIL_REPLY_TEMPLATE)
        return template.safe_substitute(
            subject=subject,
            sender=sender,
            content=content[:1000],
            reply_intent=reply_intent
        )
    
    def render_document_summary(self, content: str, length: int = 200) -> str:
        """渲染文档摘要提示词
        
        Args:
            content: 文档内容
            length: 摘要长度限制
            
        Returns:
            渲染后的提示词
        """
        template = Template(self.DOCUMENT_SUMMARY_TEMPLATE)
        return template.safe_substitute(
            content=content[:5000],  # 限制输入长度
            length=length
        )
    
    def render_knowledge_qa(self, question: str, context: str) -> str:
        """渲染知识问答提示词
        
        Args:
            question: 问题
            context: 上下文
            
        Returns:
            渲染后的提示词
        """
        template = Template(self.KNOWLEDGE_QA_TEMPLATE)
        return template.safe_substitute(
            question=question,
            context=context
        )
    
    def render_file_organize(
        self,
        directory: str,
        total_files: int,
        file_types: Dict[str, int]
    ) -> str:
        """渲染文件整理策略提示词
        
        Args:
            directory: 目录路径
            total_files: 文件总数
            file_types: 文件类型分布
            
        Returns:
            渲染后的提示词
        """
        file_types_str = "\n".join([f"- {ext}: {count}个" for ext, count in file_types.items()])
        
        template = Template(self.FILE_ORGANIZE_TEMPLATE)
        return template.safe_substitute(
            directory=directory,
            total_files=total_files,
            file_types=file_types_str
        )
    
    def render_custom(self, template_str: str, **kwargs) -> str:
        """渲染自定义提示词模板
        
        Args:
            template_str: 模板字符串
            **kwargs: 模板参数
            
        Returns:
            渲染后的提示词
        """
        template = Template(template_str)
        return template.safe_substitute(**kwargs)
