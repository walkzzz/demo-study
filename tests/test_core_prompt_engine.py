"""PromptEngine 单元测试"""
import pytest
from src.core.prompt_engine import PromptEngine


class TestPromptEngine:
    """测试提示词引擎"""
    
    def test_init(self):
        """测试初始化"""
        engine = PromptEngine()
        assert engine is not None
    
    def test_render_task_understanding(self):
        """测试任务理解提示词渲染"""
        engine = PromptEngine()
        
        user_input = "帮我整理下载文件夹"
        result = engine.render_task_understanding(user_input)
        
        assert result is not None
        assert "帮我整理下载文件夹" in result
        assert "任务目标" in result
        assert "JSON格式" in result
    
    def test_render_task_decomposition(self):
        """测试任务分解提示词渲染"""
        engine = PromptEngine()
        
        task_description = "整理文件并发送邮件"
        intent = "文件整理和邮件发送"
        entities = {"file": ["下载文件夹"], "email": ["boss@company.com"]}
        
        result = engine.render_task_decomposition(
            task_description=task_description,
            intent=intent,
            entities=entities
        )
        
        assert result is not None
        assert task_description in result
        assert intent in result
        assert "subtasks" in result
        assert "可执行的子任务" in result
    
    def test_render_tool_selection(self):
        """测试工具选择提示词渲染"""
        engine = PromptEngine()
        
        task = "扫描目录查找重复文件"
        tools = [
            {
                "name": "scan_directory",
                "description": "扫描目录获取文件列表",
                "parameters": {"directory": "目录路径"}
            },
            {
                "name": "detect_duplicates",
                "description": "检测重复文件",
                "parameters": {"files": "文件列表"}
            }
        ]
        
        result = engine.render_tool_selection(task, tools)
        
        assert result is not None
        assert task in result
        assert "scan_directory" in result
        assert "detect_duplicates" in result
        assert "工具名称" in result
    
    def test_render_tool_selection_empty_tools(self):
        """测试空工具列表的工具选择"""
        engine = PromptEngine()
        
        task = "完成任务"
        tools = []
        
        result = engine.render_tool_selection(task, tools)
        
        assert result is not None
        assert task in result
    
    def test_render_reflection(self):
        """测试反思提示词渲染"""
        engine = PromptEngine()
        
        task = "整理文件"
        history = [
            "扫描目录找到100个文件",
            "按类型分类文件",
            "移动文件到对应文件夹"
        ]
        result = "成功整理了100个文件"
        
        rendered = engine.render_reflection(task, history, result)
        
        assert rendered is not None
        assert task in rendered
        assert "扫描目录找到100个文件" in rendered
        assert "成功整理了100个文件" in rendered
        assert "quality_score" in rendered
    
    def test_render_email_classification(self):
        """测试邮件分类提示词渲染"""
        engine = PromptEngine()
        
        subject = "项目进度汇报"
        sender = "boss@company.com"
        content = "请于本周五前提交项目进度报告。" * 100  # 长内容
        
        result = engine.render_email_classification(subject, sender, content)
        
        assert result is not None
        assert subject in result
        assert sender in result
        # 内容会被截断到500字符
        assert len(result) < len(content) + 500
        assert "分类标准" in result
        assert "important" in result
    
    def test_render_email_reply(self):
        """测试邮件回复提示词渲染"""
        engine = PromptEngine()
        
        subject = "会议邀请"
        sender = "colleague@company.com"
        content = "明天下午2点开会讨论项目方案。" * 100
        reply_intent = "确认参会"
        
        result = engine.render_email_reply(subject, sender, content, reply_intent)
        
        assert result is not None
        assert subject in result
        assert sender in result
        assert reply_intent in result
        # 内容会被截断到1000字符
        assert "语气专业礼貌" in result
    
    def test_render_document_summary(self):
        """测试文档摘要提示词渲染"""
        engine = PromptEngine()
        
        content = "这是一份很长的文档内容。" * 1000
        length = 200
        
        result = engine.render_document_summary(content, length)
        
        assert result is not None
        assert str(length) in result
        # 内容会被截断到5000字符
        assert "摘要要求" in result
        assert "保留核心信息" in result
    
    def test_render_document_summary_default_length(self):
        """测试文档摘要默认长度"""
        engine = PromptEngine()
        
        content = "文档内容"
        result = engine.render_document_summary(content)
        
        assert result is not None
        assert "200" in result  # 默认长度
    
    def test_render_knowledge_qa(self):
        """测试知识问答提示词渲染"""
        engine = PromptEngine()
        
        question = "如何配置Ollama模型？"
        context = """
        Ollama是一个本地大模型服务。
        可以通过config.yaml配置模型参数。
        支持多种模型如llama3、qwen等。
        """
        
        result = engine.render_knowledge_qa(question, context)
        
        assert result is not None
        assert question in result
        assert "Ollama" in result
        assert "基于上下文回答" in result
    
    def test_render_file_organize(self):
        """测试文件整理策略提示词渲染"""
        engine = PromptEngine()
        
        directory = "/home/user/Downloads"
        total_files = 150
        file_types = {
            ".pdf": 50,
            ".jpg": 40,
            ".txt": 30,
            ".docx": 30
        }
        
        result = engine.render_file_organize(directory, total_files, file_types)
        
        assert result is not None
        assert directory in result
        assert "150" in result
        assert ".pdf: 50个" in result
        assert ".jpg: 40个" in result
        assert "strategy" in result
    
    def test_render_custom_template(self):
        """测试自定义模板渲染"""
        engine = PromptEngine()
        
        template = "用户: ${username}, 任务: ${task}"
        result = engine.render_custom(template, username="张三", task="数据分析")
        
        assert result is not None
        assert "张三" in result
        assert "数据分析" in result
    
    def test_render_custom_template_missing_param(self):
        """测试自定义模板缺少参数"""
        engine = PromptEngine()
        
        template = "用户: ${username}, 任务: ${task}"
        # safe_substitute会保留未替换的变量
        result = engine.render_custom(template, username="张三")
        
        assert result is not None
        assert "张三" in result
        assert "${task}" in result  # 未提供的参数保持原样
    
    def test_all_template_constants_exist(self):
        """测试所有模板常量是否存在"""
        engine = PromptEngine()
        
        # 验证所有模板常量都已定义
        assert hasattr(engine, 'TASK_UNDERSTANDING_TEMPLATE')
        assert hasattr(engine, 'TASK_DECOMPOSITION_TEMPLATE')
        assert hasattr(engine, 'TOOL_SELECTION_TEMPLATE')
        assert hasattr(engine, 'REFLECTION_TEMPLATE')
        assert hasattr(engine, 'EMAIL_CLASSIFICATION_TEMPLATE')
        assert hasattr(engine, 'EMAIL_REPLY_TEMPLATE')
        assert hasattr(engine, 'DOCUMENT_SUMMARY_TEMPLATE')
        assert hasattr(engine, 'KNOWLEDGE_QA_TEMPLATE')
        assert hasattr(engine, 'FILE_ORGANIZE_TEMPLATE')
        
        # 验证模板不为空
        assert len(engine.TASK_UNDERSTANDING_TEMPLATE) > 0
        assert len(engine.TASK_DECOMPOSITION_TEMPLATE) > 0
    
    def test_template_has_required_placeholders(self):
        """测试模板包含必需的占位符"""
        engine = PromptEngine()
        
        # 任务理解模板应包含user_input占位符
        assert "${user_input}" in engine.TASK_UNDERSTANDING_TEMPLATE
        
        # 任务分解模板应包含相应占位符
        assert "${task_description}" in engine.TASK_DECOMPOSITION_TEMPLATE
        assert "${intent}" in engine.TASK_DECOMPOSITION_TEMPLATE
        
        # 工具选择模板
        assert "${task}" in engine.TOOL_SELECTION_TEMPLATE
        assert "${tools}" in engine.TOOL_SELECTION_TEMPLATE
    
    def test_render_with_special_characters(self):
        """测试包含特殊字符的渲染"""
        engine = PromptEngine()
        
        user_input = "帮我整理包含$符号和{括号}的文件"
        result = engine.render_task_understanding(user_input)
        
        assert result is not None
        assert "整理" in result
    
    def test_render_with_multiline_content(self):
        """测试多行内容渲染"""
        engine = PromptEngine()
        
        question = "如何使用系统？"
        context = """
        第一步：安装依赖
        第二步：配置文件
        第三步：启动服务
        """
        
        result = engine.render_knowledge_qa(question, context)
        
        assert result is not None
        assert "第一步" in result
        assert "第三步" in result
