"""EmailTools 单元测试"""
import pytest
from datetime import datetime, timedelta
from src.tools.email_tools import EmailTools


class TestEmailTools:
    """测试邮件工具集"""
    
    @pytest.fixture
    def email_config(self):
        """邮件配置"""
        return {
            "protocol": "IMAP",
            "imap_server": "imap.example.com",
            "smtp_server": "smtp.example.com",
            "port": 993
        }
    
    @pytest.fixture
    def email_tools(self, email_config):
        """创建EmailTools实例"""
        return EmailTools(email_config)
    
    def test_init_with_config(self, email_config):
        """测试使用配置初始化"""
        tools = EmailTools(email_config)
        
        assert tools is not None
        assert tools.config == email_config
        assert tools.protocol == "IMAP"
        assert tools.imap_server == "imap.example.com"
        assert tools.smtp_server == "smtp.example.com"
    
    def test_init_without_config(self):
        """测试不带配置初始化"""
        tools = EmailTools()
        
        assert tools is not None
        assert tools.config == {}
        assert tools.protocol == "IMAP"
        assert tools.imap_server == ""
        assert tools.smtp_server == ""
    
    def test_read_emails(self, email_tools):
        """测试读取邮件"""
        account = "user@example.com"
        password = "password123"
        
        emails = email_tools.read_emails(account, password)
        
        # 验证返回邮件列表
        assert isinstance(emails, list)
        assert len(emails) > 0
        
        # 验证邮件结构
        email = emails[0]
        assert 'id' in email
        assert 'from' in email
        assert 'to' in email
        assert 'subject' in email
        assert 'content' in email
        assert 'date' in email
        assert 'attachments' in email
    
    def test_read_emails_with_time_range(self, email_tools):
        """测试带时间范围读取邮件"""
        account = "user@example.com"
        password = "password123"
        time_range = {
            "start": "2024-01-01",
            "end": "2024-01-31"
        }
        
        emails = email_tools.read_emails(account, password, time_range=time_range)
        
        assert isinstance(emails, list)
    
    def test_read_emails_with_filters(self, email_tools):
        """测试带过滤条件读取邮件"""
        account = "user@example.com"
        password = "password123"
        filters = {
            "from": "boss@company.com",
            "subject_contains": "项目"
        }
        
        emails = email_tools.read_emails(account, password, filters=filters)
        
        assert isinstance(emails, list)
    
    def test_classify_email_urgent(self, email_tools):
        """测试紧急邮件分类"""
        email = {
            "id": "email_001",
            "from": "sender@example.com",
            "subject": "urgent: 紧急任务",
            "content": "请立即处理"
        }
        
        result = email_tools.classify_email(email)
        
        assert result['category'] == 'important'
        assert result['priority'] == 'high'
        assert '紧急' in result['reason'] or 'urgent' in result['reason'].lower()
    
    def test_classify_email_from_boss(self, email_tools):
        """测试来自领导的邮件分类"""
        email = {
            "id": "email_002",
            "from": "boss@company.com",
            "subject": "周会安排",
            "content": "下周一开会"
        }
        
        result = email_tools.classify_email(email)
        
        assert result['category'] == 'important'
        assert result['priority'] == 'high'
        assert '重要' in result['reason'] or '发件人' in result['reason']
    
    def test_classify_email_notification(self, email_tools):
        """测试通知邮件分类"""
        email = {
            "id": "email_003",
            "from": "notification@service.com",
            "subject": "系统通知",
            "content": "您有新消息"
        }
        
        result = email_tools.classify_email(email)
        
        assert result['category'] == 'notification'
        assert result['priority'] == 'low'
        assert '通知' in result['reason']
    
    def test_classify_email_work(self, email_tools):
        """测试工作邮件分类"""
        email = {
            "id": "email_004",
            "from": "colleague@company.com",
            "subject": "项目资料",
            "content": "附件是项目相关资料"
        }
        
        result = email_tools.classify_email(email)
        
        assert result['category'] == 'work'
        assert result['priority'] == 'medium'
        assert '工作' in result['reason']
    
    def test_classify_email_structure(self, email_tools):
        """测试邮件分类结果结构"""
        email = {
            "id": "test",
            "from": "test@example.com",
            "subject": "测试",
            "content": "测试内容"
        }
        
        result = email_tools.classify_email(email)
        
        # 验证结果包含必需字段
        assert 'category' in result
        assert 'priority' in result
        assert 'reason' in result
        
        # 验证字段值有效
        assert result['category'] in ['important', 'work', 'notification', 'spam', 'other']
        assert result['priority'] in ['high', 'medium', 'low']
        assert isinstance(result['reason'], str)
    
    def test_draft_reply(self, email_tools):
        """测试生成回复草稿"""
        original_email = {
            "id": "email_001",
            "from": "sender@example.com",
            "subject": "会议邀请",
            "content": "明天下午2点开会"
        }
        reply_intent = "确认参加会议"
        
        draft = email_tools.draft_reply(original_email, reply_intent)
        
        # 验证草稿不为空
        assert draft is not None
        assert len(draft) > 0
        
        # 验证包含回复意图
        assert reply_intent in draft
        
        # 验证包含基本礼貌用语
        assert "您好" in draft or "收到" in draft
    
    def test_draft_reply_preserves_subject(self, email_tools):
        """测试回复草稿保留主题"""
        original_email = {
            "from": "test@example.com",
            "subject": "项目进度",
            "content": "请汇报进度"
        }
        reply_intent = "项目进展顺利"
        
        draft = email_tools.draft_reply(original_email, reply_intent)
        
        # 回复中应该引用原主题
        assert "项目进度" in draft
    
    def test_send_email(self, email_tools):
        """测试发送邮件"""
        account = "sender@example.com"
        password = "password123"
        to = "recipient@example.com"
        subject = "测试邮件"
        content = "这是一封测试邮件"
        
        result = email_tools.send_email(account, password, to, subject, content)
        
        # 验证发送结果
        assert result['status'] == 'success'
        assert 'message_id' in result
        assert 'sent_at' in result
    
    def test_send_email_with_attachments(self, email_tools):
        """测试发送带附件的邮件"""
        account = "sender@example.com"
        password = "password123"
        to = "recipient@example.com"
        subject = "测试邮件"
        content = "这是一封测试邮件"
        attachments = ["/path/to/file1.pdf", "/path/to/file2.docx"]
        
        result = email_tools.send_email(
            account, password, to, subject, content,
            attachments=attachments
        )
        
        assert result['status'] == 'success'
        assert 'message_id' in result
    
    def test_archive_emails(self, email_tools):
        """测试归档邮件"""
        account = "user@example.com"
        password = "password123"
        email_ids = ["email_001", "email_002", "email_003"]
        
        result = email_tools.archive_emails(account, password, email_ids)
        
        # 验证归档结果
        assert result['archived_count'] == 3
        assert result['failed'] == []
        assert result['folder'] == 'Archive'
    
    def test_archive_emails_custom_folder(self, email_tools):
        """测试归档到自定义文件夹"""
        account = "user@example.com"
        password = "password123"
        email_ids = ["email_001"]
        archive_folder = "Important/2024"
        
        result = email_tools.archive_emails(
            account, password, email_ids,
            archive_folder=archive_folder
        )
        
        assert result['folder'] == archive_folder
    
    def test_archive_emails_empty_list(self, email_tools):
        """测试归档空邮件列表"""
        account = "user@example.com"
        password = "password123"
        email_ids = []
        
        result = email_tools.archive_emails(account, password, email_ids)
        
        assert result['archived_count'] == 0
    
    def test_get_tool_descriptions(self, email_tools):
        """测试获取工具描述"""
        descriptions = email_tools.get_tool_descriptions()
        
        assert isinstance(descriptions, list)
        assert len(descriptions) > 0
        
        # 验证每个工具描述的结构
        for tool in descriptions:
            assert 'name' in tool
            assert 'description' in tool
            assert 'parameters' in tool
    
    def test_get_tool_descriptions_contains_all_tools(self, email_tools):
        """测试工具描述包含所有工具"""
        descriptions = email_tools.get_tool_descriptions()
        
        tool_names = [tool['name'] for tool in descriptions]
        
        # 验证包含主要工具
        assert 'read_emails' in tool_names
        assert 'classify_email' in tool_names
        assert 'draft_reply' in tool_names
        assert 'send_email' in tool_names
        assert 'archive_emails' in tool_names
    
    def test_read_emails_returns_recent_first(self, email_tools):
        """测试读取邮件按时间降序返回"""
        account = "user@example.com"
        password = "password123"
        
        emails = email_tools.read_emails(account, password)
        
        if len(emails) >= 2:
            # 第一封邮件时间应该晚于或等于第二封
            date1 = datetime.fromisoformat(emails[0]['date'])
            date2 = datetime.fromisoformat(emails[1]['date'])
            assert date1 >= date2
    
    def test_classify_email_case_insensitive(self, email_tools):
        """测试邮件分类大小写不敏感"""
        email_upper = {
            "id": "test1",
            "from": "BOSS@company.com",
            "subject": "URGENT Task",
            "content": "Please handle"
        }
        
        email_lower = {
            "id": "test2",
            "from": "boss@company.com",
            "subject": "urgent task",
            "content": "please handle"
        }
        
        result1 = email_tools.classify_email(email_upper)
        result2 = email_tools.classify_email(email_lower)
        
        # 两者分类结果应该一致
        assert result1['category'] == result2['category']
        assert result1['priority'] == result2['priority']
    
    def test_email_tool_integration_workflow(self, email_tools):
        """测试邮件工具集成工作流"""
        # 1. 读取邮件
        emails = email_tools.read_emails("user@example.com", "password")
        assert len(emails) > 0
        
        # 2. 分类第一封邮件
        email = emails[0]
        classification = email_tools.classify_email(email)
        assert 'category' in classification
        
        # 3. 如果是重要邮件，生成回复
        if classification['category'] == 'important':
            draft = email_tools.draft_reply(email, "已收到，正在处理")
            assert len(draft) > 0
            
            # 4. 发送回复
            result = email_tools.send_email(
                "user@example.com",
                "password",
                email['from'],
                f"Re: {email['subject']}",
                draft
            )
            assert result['status'] == 'success'
        
        # 5. 归档已处理邮件
        archive_result = email_tools.archive_emails(
            "user@example.com",
            "password",
            [email['id']]
        )
        assert archive_result['archived_count'] == 1
