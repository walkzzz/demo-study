"""TaskPlanner 单元测试"""
import pytest
from unittest.mock import Mock
from src.orchestrator.task_planner import TaskPlanner


class TestTaskPlanner:
    """测试任务规划器"""
    
    @pytest.fixture
    def mock_model_manager(self):
        """Mock模型管理器"""
        mock = Mock()
        mock.invoke = Mock(return_value="Mock response")
        return mock
    
    @pytest.fixture
    def mock_prompt_engine(self):
        """Mock提示词引擎"""
        mock = Mock()
        mock.render_task_decomposition = Mock(return_value="Mock prompt")
        return mock
    
    @pytest.fixture
    def task_planner(self, mock_model_manager, mock_prompt_engine):
        """创建TaskPlanner实例"""
        return TaskPlanner(mock_model_manager, mock_prompt_engine)
    
    def test_init(self, mock_model_manager, mock_prompt_engine):
        """测试初始化"""
        planner = TaskPlanner(mock_model_manager, mock_prompt_engine)
        
        assert planner is not None
        assert planner.model_manager == mock_model_manager
        assert planner.prompt_engine == mock_prompt_engine
    
    def test_decompose_task_single_agent(self, task_planner):
        """测试分解单个智能体任务"""
        task_understanding = {
            'intent': '整理文件',
            'original_input': '帮我整理下载文件夹',
            'required_agents': ['file'],
            'entities': {}
        }
        
        subtasks = task_planner.decompose_task(task_understanding)
        
        assert len(subtasks) == 1
        assert subtasks[0]['agent_type'] == 'file'
        assert subtasks[0]['type'] == 'organize'
        assert 'id' in subtasks[0]
        assert 'description' in subtasks[0]
        assert 'inputs' in subtasks[0]
        assert 'dependencies' in subtasks[0]
    
    def test_decompose_task_multiple_agents(self, task_planner):
        """测试分解多个智能体任务"""
        task_understanding = {
            'intent': '整理文件并发送邮件',
            'original_input': '整理下载文件夹然后给老板发邮件汇报',
            'required_agents': ['file', 'email'],
            'entities': {}
        }
        
        subtasks = task_planner.decompose_task(task_understanding)
        
        assert len(subtasks) == 2
        assert subtasks[0]['agent_type'] == 'file'
        assert subtasks[1]['agent_type'] == 'email'
        
        # 验证每个子任务有唯一ID
        ids = [task['id'] for task in subtasks]
        assert len(ids) == len(set(ids))
    
    def test_decompose_task_empty_agents(self, task_planner):
        """测试空智能体列表"""
        task_understanding = {
            'intent': '未知任务',
            'original_input': '帮我做点什么',
            'required_agents': [],
            'entities': {}
        }
        
        subtasks = task_planner.decompose_task(task_understanding)
        
        assert subtasks == []
    
    def test_infer_task_type_email_read(self, task_planner):
        """测试推断邮件读取任务类型"""
        task_type = task_planner._infer_task_type('读取今天的邮件', 'email')
        assert task_type == 'read_emails'
        
        task_type = task_planner._infer_task_type('查看未读邮件', 'email')
        assert task_type == 'read_emails'
    
    def test_infer_task_type_email_reply(self, task_planner):
        """测试推断邮件回复任务类型"""
        task_type = task_planner._infer_task_type('回复老板的邮件', 'email')
        assert task_type == 'reply'
    
    def test_infer_task_type_email_archive(self, task_planner):
        """测试推断邮件归档任务类型"""
        task_type = task_planner._infer_task_type('归档所有通知邮件', 'email')
        assert task_type == 'archive'
    
    def test_infer_task_type_email_default(self, task_planner):
        """测试邮件默认任务类型"""
        task_type = task_planner._infer_task_type('处理邮件', 'email')
        assert task_type == 'classify'
    
    def test_infer_task_type_file_organize(self, task_planner):
        """测试推断文件整理任务类型"""
        task_type = task_planner._infer_task_type('整理下载文件夹', 'file')
        assert task_type == 'organize'
    
    def test_infer_task_type_file_duplicates(self, task_planner):
        """测试推断重复文件检测任务类型"""
        task_type = task_planner._infer_task_type('找出重复的文件', 'file')
        assert task_type == 'detect_duplicates'
    
    def test_infer_task_type_file_search(self, task_planner):
        """测试推断文件搜索任务类型"""
        task_type = task_planner._infer_task_type('搜索PDF文件', 'file')
        assert task_type == 'search'
    
    def test_infer_task_type_file_analyze_storage(self, task_planner):
        """测试推断存储分析任务类型"""
        task_type = task_planner._infer_task_type('分析磁盘空间占用', 'file')
        assert task_type == 'analyze_storage'
        
        task_type = task_planner._infer_task_type('查看空间使用情况', 'file')
        assert task_type == 'analyze_storage'
    
    def test_infer_task_type_file_default(self, task_planner):
        """测试文件默认任务类型"""
        task_type = task_planner._infer_task_type('处理文件', 'file')
        assert task_type == 'organize'
    
    def test_infer_task_type_data_analyze(self, task_planner):
        """测试推断数据分析任务类型"""
        task_type = task_planner._infer_task_type('分析销售数据', 'data')
        assert task_type == 'analyze'
    
    def test_infer_task_type_data_visualize(self, task_planner):
        """测试推断数据可视化任务类型"""
        task_type = task_planner._infer_task_type('生成销售图表', 'data')
        assert task_type == 'visualize'
        
        task_type = task_planner._infer_task_type('可视化数据', 'data')
        assert task_type == 'visualize'
    
    def test_infer_task_type_data_default(self, task_planner):
        """测试数据默认任务类型"""
        task_type = task_planner._infer_task_type('处理数据', 'data')
        assert task_type == 'load_data'
    
    def test_infer_task_type_unknown_agent(self, task_planner):
        """测试未知智能体类型"""
        task_type = task_planner._infer_task_type('执行任务', 'unknown')
        assert task_type == 'default'
    
    def test_extract_inputs_file_downloads(self, task_planner):
        """测试提取文件任务输入 - 下载文件夹"""
        task_understanding = {
            'original_input': '整理下载文件夹',
            'entities': {}
        }
        
        inputs = task_planner._extract_inputs(task_understanding, 'file')
        
        assert 'directory' in inputs
        assert inputs['directory'] == '~/Downloads'
        assert inputs['strategy'] == 'by_type'
        assert inputs['dry_run'] is True
    
    def test_extract_inputs_file_documents(self, task_planner):
        """测试提取文件任务输入 - 文档文件夹"""
        task_understanding = {
            'original_input': '整理文档文件夹',
            'entities': {}
        }
        
        inputs = task_planner._extract_inputs(task_understanding, 'file')
        
        assert inputs['directory'] == '~/Documents'
    
    def test_extract_inputs_file_default(self, task_planner):
        """测试提取文件任务输入 - 默认路径"""
        task_understanding = {
            'original_input': '整理文件',
            'entities': {}
        }
        
        inputs = task_planner._extract_inputs(task_understanding, 'file')
        
        assert inputs['directory'] == '.'
        assert inputs['dry_run'] is True
    
    def test_extract_inputs_non_file_agent(self, task_planner):
        """测试非文件智能体的输入提取"""
        task_understanding = {
            'original_input': '读取邮件',
            'entities': {}
        }
        
        inputs = task_planner._extract_inputs(task_understanding, 'email')
        
        # 非file类型应返回空字典
        assert inputs == {}
    
    def test_subtask_structure(self, task_planner):
        """测试子任务结构完整性"""
        task_understanding = {
            'intent': '整理文件',
            'original_input': '帮我整理下载文件夹',
            'required_agents': ['file'],
            'entities': {}
        }
        
        subtasks = task_planner.decompose_task(task_understanding)
        
        # 验证子任务包含所有必需字段
        required_fields = ['id', 'description', 'agent_type', 'type', 'inputs', 'dependencies']
        for subtask in subtasks:
            for field in required_fields:
                assert field in subtask, f"Missing field: {field}"
    
    def test_subtask_ids_sequential(self, task_planner):
        """测试子任务ID是顺序的"""
        task_understanding = {
            'intent': '多任务处理',
            'original_input': '整理文件、读邮件、分析数据',
            'required_agents': ['file', 'email', 'data'],
            'entities': {}
        }
        
        subtasks = task_planner.decompose_task(task_understanding)
        
        # 验证ID是task_1, task_2, task_3...
        for i, subtask in enumerate(subtasks):
            assert subtask['id'] == f'task_{i + 1}'
    
    def test_decompose_task_preserves_original_input(self, task_planner):
        """测试任务分解保留原始输入信息"""
        original_input = '帮我整理下载文件夹中的PDF文件'
        task_understanding = {
            'intent': '文件整理',
            'original_input': original_input,
            'required_agents': ['file'],
            'entities': {}
        }
        
        subtasks = task_planner.decompose_task(task_understanding)
        
        # 任务类型应该能够从原始输入推断
        assert subtasks[0]['type'] == 'organize'
        assert subtasks[0]['inputs']['directory'] == '~/Downloads'
    
    def test_decompose_task_complex_scenario(self, task_planner):
        """测试复杂场景的任务分解"""
        task_understanding = {
            'intent': '完整的工作流',
            'original_input': '整理下载文件夹，然后读取邮件，分析数据并生成报告',
            'required_agents': ['file', 'email', 'data'],
            'entities': {
                'directory': ['下载文件夹'],
                'data_type': ['销售数据']
            }
        }
        
        subtasks = task_planner.decompose_task(task_understanding)
        
        assert len(subtasks) == 3
        
        # 验证每个任务的agent_type正确
        agent_types = [task['agent_type'] for task in subtasks]
        assert 'file' in agent_types
        assert 'email' in agent_types
        assert 'data' in agent_types
        
        # 验证任务类型推断正确
        file_task = next(t for t in subtasks if t['agent_type'] == 'file')
        assert file_task['type'] == 'organize'
        
        email_task = next(t for t in subtasks if t['agent_type'] == 'email')
        assert email_task['type'] == 'read_emails'
        
        data_task = next(t for t in subtasks if t['agent_type'] == 'data')
        assert data_task['type'] == 'analyze'
