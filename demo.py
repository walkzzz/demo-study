"""演示脚本 - 展示系统核心功能"""

import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.core import ModelManager, PromptEngine, MemoryManager
from src.tools import FileSystemTools
import json


def demo_file_system_tools():
    """演示文件系统工具"""
    print("\n" + "="*60)
    print("📁 文件系统工具演示")
    print("="*60)
    
    # 初始化工具
    config = {
        "backup_directory": "./data/backups",
        "file_classification_rules": "config/file_rules.json"
    }
    tools = FileSystemTools(config)
    
    # 演示1: 扫描当前目录
    print("\n1️⃣ 扫描当前目录...")
    result = None
    try:
        result = tools.scan_directory(".", max_depth=1, file_types=['.py', '.md', '.yaml', '.json'])
        print(f"   ✅ 找到 {result['total_files']} 个文件")
        print(f"   📊 总大小: {result['total_size'] / 1024:.2f} KB")
        print(f"   📋 文件类型分布:")
        for ext, count in result['file_type_stats'].items():
            print(f"      {ext}: {count}个")
    except Exception as e:
        print(f"   ❌ 错误: {e}")
    
    # 演示2: 文件分类
    print("\n2️⃣ 文件智能分类...")
    try:
        if result is not None and 'files' in result:
            files = result['files'][:10]  # 取前10个文件演示
            classified = tools.classify_files(files)
            print(f"   ✅ 分类完成")
            for category, file_list in classified.items():
                print(f"      {category}: {len(file_list)}个")
        else:
            print(f"   ⚠️  跳过: 无可用文件数据")
    except Exception as e:
        print(f"   ❌ 错误: {e}")
    
    # 演示3: 磁盘空间分析
    print("\n3️⃣ 磁盘空间分析...")
    try:
        report = tools.analyze_storage(".")
        print(f"   ✅ 分析完成")
        print(f"   📊 文件总数: {report['total_files']}")
        print(f"   💾 总大小: {report['total_size_mb']:.2f} MB")
        if report['largest_files']:
            print(f"   📈 最大文件: {report['largest_files'][0]['name']} ({report['largest_files'][0]['size'] / 1024:.2f} KB)")
    except Exception as e:
        print(f"   ❌ 错误: {e}")


def demo_prompt_engine():
    """演示提示词引擎"""
    print("\n" + "="*60)
    print("💬 提示词引擎演示")
    print("="*60)
    
    engine = PromptEngine()
    
    # 演示1: 任务理解提示词
    print("\n1️⃣ 任务理解提示词")
    prompt = engine.render_task_understanding("整理我的下载文件夹")
    print(f"   ✅ 生成提示词长度: {len(prompt)} 字符")
    print(f"   预览: {prompt[:100]}...")
    
    # 演示2: 文件整理策略提示词
    print("\n2️⃣ 文件整理策略提示词")
    file_types = {'.py': 150, '.md': 50, '.yaml': 10}
    prompt = engine.render_file_organize("./downloads", 210, file_types)
    print(f"   ✅ 生成提示词长度: {len(prompt)} 字符")
    print(f"   预览: {prompt[:100]}...")


def demo_memory_manager():
    """演示记忆管理器"""
    print("\n" + "="*60)
    print("🧠 记忆管理器演示")
    print("="*60)
    
    memory = MemoryManager()
    
    # 演示1: 短期记忆
    print("\n1️⃣ 短期记忆 (对话上下文)")
    memory.add_message("user", "帮我整理文件")
    memory.add_message("assistant", "好的，我会帮您整理文件")
    recent = memory.get_recent_messages(2)
    print(f"   ✅ 保存 {len(recent)} 条消息")
    
    # 演示2: 长期记忆
    print("\n2️⃣ 长期记忆 (知识库)")
    memory.save_knowledge("user_preference", "喜欢按类型整理文件", category="file_agent")
    preference = memory.get_knowledge("user_preference", category="file_agent")
    print(f"   ✅ 保存并检索知识: {preference}")
    
    # 演示3: 工作记忆
    print("\n3️⃣ 工作记忆 (任务状态)")
    memory.set_task_state("task_001", {"status": "running", "progress": 0.5})
    state = memory.get_task_state("task_001")
    print(f"   ✅ 任务状态: {state}")
    
    # 演示4: 统计信息
    print("\n4️⃣ 记忆统计")
    stats = memory.get_memory_stats()
    print(f"   ✅ 统计信息:")
    for key, value in stats.items():
        print(f"      {key}: {value}")


def demo_configuration():
    """演示配置系统"""
    print("\n" + "="*60)
    print("⚙️  配置系统演示")
    print("="*60)
    
    try:
        import yaml
    except ImportError:
        print("   ❌ 错误: yaml模块未安装，请运行: pip install pyyaml")
        return
    
    # 演示1: 主配置
    print("\n1️⃣ 主配置 (config/config.yaml)")
    try:
        with open("config/config.yaml", 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        print(f"   ✅ Ollama地址: {config['ollama']['base_url']}")
        print(f"   ✅ 默认模型: {config['ollama']['default_model']}")
        print(f"   ✅ 向量数据库: {config['vector_db']['type']}")
    except Exception as e:
        print(f"   ❌ 错误: {e}")
    
    # 演示2: 智能体配置
    print("\n2️⃣ 智能体配置 (config/agents.yaml)")
    try:
        with open("config/agents.yaml", 'r', encoding='utf-8') as f:
            agents_config = yaml.safe_load(f)
        agents = agents_config['agents']
        print(f"   ✅ 智能体数量: {len(agents)}")
        for name in agents.keys():
            print(f"      - {name}")
    except Exception as e:
        print(f"   ❌ 错误: {e}")
    
    # 演示3: 文件分类规则
    print("\n3️⃣ 文件分类规则 (config/file_rules.json)")
    try:
        with open("config/file_rules.json", 'r', encoding='utf-8') as f:
            rules = json.load(f)
        categories = rules['file_classification_rules']
        print(f"   ✅ 分类类别数: {len(categories)}")
        for category in list(categories.keys())[:5]:
            print(f"      - {category}")
    except Exception as e:
        print(f"   ❌ 错误: {e}")


def main():
    """主函数"""
    print("\n🤖 日常办公超级智能体 - 系统演示")
    print("="*60)
    print("\n本演示展示系统的核心功能 (不需要Ollama运行)\n")
    
    try:
        # 1. 配置系统
        demo_configuration()
        
        # 2. 提示词引擎
        demo_prompt_engine()
        
        # 3. 记忆管理器
        demo_memory_manager()
        
        # 4. 文件系统工具
        demo_file_system_tools()
        
        print("\n" + "="*60)
        print("✅ 演示完成!")
        print("="*60)
        print("\n💡 提示:")
        print("   - 启动Ollama后可以运行完整系统: python src/cli/main.py")
        print("   - 启动API服务: python src/api/main.py")
        print("   - 查看文档: README.md, QUICKSTART.md, ARCHITECTURE.md")
        print()
        
    except Exception as e:
        print(f"\n❌ 演示过程中发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
