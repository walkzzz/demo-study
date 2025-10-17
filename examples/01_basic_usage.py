"""
示例 01: 基础使用入门
演示系统的基本功能和工作流程
"""

import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.core import ModelManager, PromptEngine, MemoryManager


def example_1_model_manager():
    """示例1: 使用模型管理器"""
    print("\n" + "="*60)
    print("📦 示例1: 模型管理器基础使用")
    print("="*60)
    
    # 创建模型管理器实例
    model_manager = ModelManager()
    
    # 查看配置信息
    print("\n1️⃣ 查看模型配置:")
    print(f"   Ollama 地址: {model_manager.ollama_config.get('base_url')}")
    print(f"   默认模型: {model_manager.ollama_config.get('default_model')}")
    print(f"   超时设置: {model_manager.ollama_config.get('timeout')}秒")
    
    # 获取模型实例
    print("\n2️⃣ 获取不同任务的模型实例:")
    try:
        # 获取默认模型
        model = model_manager.get_model()
        print(f"   ✅ 获取默认模型实例成功")
        
        # 获取特定任务的模型
        task_model = model_manager.get_model(task_type="task_understanding")
        print(f"   ✅ 获取任务理解模型实例成功")
        
    except Exception as e:
        print(f"   ⚠️  提示: {e}")
        print(f"   💡 请确保 Ollama 服务正在运行")


def example_2_prompt_engine():
    """示例2: 使用提示词引擎"""
    print("\n" + "="*60)
    print("💬 示例2: 提示词引擎使用")
    print("="*60)
    
    # 创建提示词引擎实例
    prompt_engine = PromptEngine()
    
    # 示例1: 任务理解提示词
    print("\n1️⃣ 生成任务理解提示词:")
    task = "帮我整理桌面文件，按照类型分类"
    prompt = prompt_engine.render_task_understanding(task)
    print(f"   原始任务: {task}")
    print(f"   生成提示词长度: {len(prompt)} 字符")
    print(f"   提示词预览:\n   {prompt[:150]}...\n")
    
    # 示例2: 文件整理策略提示词
    print("\n2️⃣ 生成文件整理策略提示词:")
    file_types = {
        '.pdf': 25,
        '.docx': 15,
        '.jpg': 50,
        '.py': 30
    }
    prompt = prompt_engine.render_file_organize("./Desktop", 120, file_types)
    print(f"   目标目录: ./Desktop")
    print(f"   文件总数: 120")
    print(f"   文件类型: {len(file_types)} 种")
    print(f"   生成提示词长度: {len(prompt)} 字符")


def example_3_memory_system():
    """示例3: 使用记忆系统"""
    print("\n" + "="*60)
    print("🧠 示例3: 记忆系统使用")
    print("="*60)
    
    # 创建记忆管理器实例
    memory = MemoryManager()
    
    # 示例1: 对话记忆
    print("\n1️⃣ 对话记忆 (短期记忆):")
    memory.add_message("user", "你好，我想整理文件")
    memory.add_message("assistant", "好的，我可以帮您整理文件。请问是哪个目录？")
    memory.add_message("user", "桌面的文件夹")
    
    recent_messages = memory.get_recent_messages(3)
    print(f"   保存了 {len(recent_messages)} 条对话")
    for msg in recent_messages:
        print(f"      {msg['role']}: {msg['content'][:30]}...")
    
    # 示例2: 知识存储
    print("\n2️⃣ 知识存储 (长期记忆):")
    memory.save_knowledge(
        "file_organize_preference",
        "用户喜欢按照 文档/图片/代码 三大类整理文件",
        category="file_agent"
    )
    
    knowledge = memory.get_knowledge("file_organize_preference", category="file_agent")
    print(f"   ✅ 存储知识: {knowledge}")
    
    # 示例3: 任务状态
    print("\n3️⃣ 任务状态 (工作记忆):")
    memory.set_task_state("task_organize_001", {
        "status": "processing",
        "progress": 0.6,
        "current_step": "分类文件中"
    })
    
    task_state = memory.get_task_state("task_organize_001")
    print(f"   任务状态: {task_state}")
    
    # 示例4: 记忆统计
    print("\n4️⃣ 记忆系统统计:")
    stats = memory.get_memory_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")


def example_4_complete_workflow():
    """示例4: 完整工作流程演示"""
    print("\n" + "="*60)
    print("🔄 示例4: 完整工作流程")
    print("="*60)
    
    print("\n这是一个典型的用户请求处理流程:\n")
    
    # 步骤1: 用户输入
    user_input = "帮我分析一下最近的销售数据"
    print(f"1️⃣ 用户输入: '{user_input}'")
    
    # 步骤2: 任务理解
    print("\n2️⃣ 系统分析:")
    print("   - 识别任务类型: 数据分析")
    print("   - 选择智能体: data_agent")
    print("   - 需要工具: 数据读取、统计分析、可视化")
    
    # 步骤3: 生成提示词
    prompt_engine = PromptEngine()
    prompt = prompt_engine.render_task_understanding(user_input)
    print(f"\n3️⃣ 生成提示词: {len(prompt)} 字符")
    
    # 步骤4: 记忆管理
    memory = MemoryManager()
    memory.add_message("user", user_input)
    print("\n4️⃣ 保存到对话历史")
    
    # 步骤5: 执行任务 (模拟)
    print("\n5️⃣ 执行任务流程:")
    steps = [
        "读取销售数据文件",
        "数据清洗和预处理",
        "计算关键指标",
        "生成可视化图表",
        "编写分析报告"
    ]
    for i, step in enumerate(steps, 1):
        print(f"   {i}. {step}")
    
    # 步骤6: 返回结果
    print("\n6️⃣ 返回结果给用户")
    print("   ✅ 任务完成!")


def main():
    """主函数"""
    print("\n" + "="*70)
    print("🎓 日常办公超级智能体系统 - 基础使用示例")
    print("="*70)
    
    print("\n本示例展示系统的基础组件和工作流程")
    print("无需 Ollama 运行即可查看功能演示\n")
    
    try:
        # 运行各个示例
        example_1_model_manager()
        example_2_prompt_engine()
        example_3_memory_system()
        example_4_complete_workflow()
        
        print("\n" + "="*70)
        print("✅ 所有示例运行完成!")
        print("="*70)
        
        print("\n💡 下一步:")
        print("   - 查看 02_model_manager.py 了解模型管理")
        print("   - 查看 03_memory_system.py 了解记忆系统")
        print("   - 查看 04_file_agent.py 了解智能体使用")
        print()
        
    except Exception as e:
        print(f"\n❌ 运行出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
