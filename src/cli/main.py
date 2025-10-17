"""命令行界面主程序"""

import sys
import logging
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core import ModelManager, PromptEngine, MemoryManager, VectorDBManager
from src.tools import (
    EmailTools, FileTools, CalendarTools,
    DataTools, WebTools, FileSystemTools
)
from src.agents import (
    EmailAgent, DocAgent, ScheduleAgent,
    DataAgent, KnowledgeAgent, FileAgent
)
from src.orchestrator import SuperAgent, TaskPlanner, StateManager
import yaml

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class OfficeSuperAgentCLI:
    """日常办公超级智能体CLI"""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        """初始化CLI"""
        logger.info("初始化日常办公超级智能体...")
        
        # 加载配置
        self.config = self._load_config(config_path)
        agents_config = self._load_config("config/agents.yaml")
        
        # 初始化核心组件
        self.model_manager = ModelManager(config_path)
        self.prompt_engine = PromptEngine()
        self.memory_manager = MemoryManager(config_path)
        self.vector_db = VectorDBManager(config_path)
        
        # 初始化工具
        email_config = self.config.get('email', {})
        filesystem_config = self.config.get('filesystem', {})
        
        self.email_tools = EmailTools(email_config)
        self.file_tools = FileTools()
        self.calendar_tools = CalendarTools()
        self.data_tools = DataTools()
        self.web_tools = WebTools()
        self.filesystem_tools = FileSystemTools(filesystem_config)
        
        # 初始化智能体
        self.agents = self._initialize_agents(agents_config)
        
        # 初始化编排层
        self.task_planner = TaskPlanner(self.model_manager, self.prompt_engine)
        self.state_manager = StateManager()
        self.super_agent = SuperAgent(
            self.model_manager,
            self.prompt_engine,
            self.memory_manager,
            self.task_planner,
            self.agents
        )
        
        logger.info("初始化完成!")
    
    def _load_config(self, config_path: str) -> dict:
        """加载配置文件"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"加载配置文件失败: {e}")
            return {}
    
    def _initialize_agents(self, agents_config: dict) -> dict:
        """初始化所有智能体"""
        agents = {}
        
        agents_def = agents_config.get('agents', {})
        
        # 邮件智能体
        if 'email_agent' in agents_def:
            agents['email'] = EmailAgent(
                name="EmailAgent",
                model_manager=self.model_manager,
                prompt_engine=self.prompt_engine,
                memory_manager=self.memory_manager,
                tools=self.email_tools,
                config=agents_def['email_agent']
            )
        
        # 文档智能体
        if 'doc_agent' in agents_def:
            agents['doc'] = DocAgent(
                name="DocAgent",
                model_manager=self.model_manager,
                prompt_engine=self.prompt_engine,
                memory_manager=self.memory_manager,
                tools=self.file_tools,
                config=agents_def['doc_agent']
            )
        
        # 日程智能体
        if 'schedule_agent' in agents_def:
            agents['schedule'] = ScheduleAgent(
                name="ScheduleAgent",
                model_manager=self.model_manager,
                prompt_engine=self.prompt_engine,
                memory_manager=self.memory_manager,
                tools=self.calendar_tools,
                config=agents_def['schedule_agent']
            )
        
        # 数据分析智能体
        if 'data_agent' in agents_def:
            agents['data'] = DataAgent(
                name="DataAgent",
                model_manager=self.model_manager,
                prompt_engine=self.prompt_engine,
                memory_manager=self.memory_manager,
                tools=self.data_tools,
                config=agents_def['data_agent']
            )
        
        # 知识问答智能体
        if 'knowledge_agent' in agents_def:
            agents['knowledge'] = KnowledgeAgent(
                name="KnowledgeAgent",
                model_manager=self.model_manager,
                prompt_engine=self.prompt_engine,
                memory_manager=self.memory_manager,
                tools=self.web_tools,
                vector_db=self.vector_db,
                config=agents_def['knowledge_agent']
            )
        
        # 文件系统智能体
        if 'file_agent' in agents_def:
            agents['file'] = FileAgent(
                name="FileAgent",
                model_manager=self.model_manager,
                prompt_engine=self.prompt_engine,
                memory_manager=self.memory_manager,
                tools=self.filesystem_tools,
                config=agents_def['file_agent']
            )
        
        logger.info(f"初始化了 {len(agents)} 个专业智能体")
        return agents
    
    def run(self):
        """运行CLI"""
        print("\n" + "="*60)
        print("🤖 日常办公超级智能体")
        print("="*60)
        print("\n欢迎使用!输入您的办公需求,我会帮您处理。")
        print("输入 'help' 查看帮助，输入 'exit' 退出。\n")
        
        while True:
            try:
                user_input = input("👤 您: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['exit', 'quit', '退出']:
                    print("\n再见!👋")
                    break
                
                if user_input.lower() == 'help':
                    self._show_help()
                    continue
                
                # 处理用户请求
                print("\n🤖 处理中...")
                result = self.super_agent.process_request(user_input)
                
                if result['status'] == 'success':
                    print(f"\n✅ {result['result']}\n")
                else:
                    print(f"\n❌ 错误: {result.get('message', '未知错误')}\n")
                
            except KeyboardInterrupt:
                print("\n\n再见!👋")
                break
            except Exception as e:
                logger.error(f"处理请求时发生错误: {e}")
                print(f"\n❌ 发生错误: {e}\n")
    
    def _show_help(self):
        """显示帮助信息"""
        help_text = """
使用示例:

📧 邮件管理:
  - "帮我处理今天的邮件"
  - "读取未读邮件并分类"

📄 文档处理:
  - "对比这两份合同的差异"
  - "生成会议纪要摘要"

📅 日程管理:
  - "安排明天下午2点的会议"
  - "查看本周日程"

📊 数据分析:
  - "分析销售数据并生成图表"
  - "统计本月的收入情况"

📁 文件管理:
  - "整理我的下载文件夹"
  - "检测并删除重复文件"
  - "分析磁盘空间使用情况"

❓ 知识问答:
  - "公司的报销流程是什么?"
  - "如何使用OA系统?"
"""
        print(help_text)


def main():
    """主函数"""
    try:
        cli = OfficeSuperAgentCLI()
        cli.run()
    except Exception as e:
        logger.error(f"程序启动失败: {e}")
        print(f"\n❌ 启动失败: {e}")
        print("\n请确保:")
        print("1. Ollama服务已启动 (http://localhost:11434)")
        print("2. 配置文件存在且正确 (config/config.yaml)")
        sys.exit(1)


if __name__ == "__main__":
    main()
