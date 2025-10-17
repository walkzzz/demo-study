"""
示例 03: 记忆系统详细使用
演示如何使用 MemoryManager 管理短期、长期和工作记忆
"""

import sys
from pathlib import Path
import time

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.core import MemoryManager


def example_1_short_term_memory():
    """示例1: 短期记忆 (对话上下文)"""
    print("\n" + "="*60)
    print("💭 示例1: 短期记忆 - 对话上下文管理")
    print("="*60)
    
    memory = MemoryManager()
    
    # 模拟一段对话
    print("\n模拟对话场景:")
    conversation = [
        ("user", "你好，我想整理我的文件"),
        ("assistant", "好的，我可以帮您整理文件。请问是哪个目录？"),
        ("user", "是我的桌面文件夹"),
        ("assistant", "明白了。您希望按什么方式整理？"),
        ("user", "按文件类型分类"),
    ]
    
    for role, content in conversation:
        memory.add_message(role, content)
        print(f"  {role}: {content}")
    
    # 获取最近的对话
    print("\n📋 获取最近3条对话:")
    recent = memory.get_recent_messages(3)
    for msg in recent:
        print(f"  {msg['role']}: {msg['content']}")
    
    # 获取完整对话历史
    print("\n📋 完整对话历史:")
    all_messages = memory.get_recent_messages(10)
    print(f"  共 {len(all_messages)} 条消息")


def example_2_long_term_memory():
    """示例2: 长期记忆 (知识存储)"""
    print("\n" + "="*60)
    print("🧠 示例2: 长期记忆 - 知识存储")
    print("="*60)
    
    memory = MemoryManager()
    
    # 保存用户偏好
    print("\n1️⃣ 保存用户偏好:")
    preferences = [
        ("file_organize_rule", "总是按照 文档/图片/代码/其他 四类整理", "file_agent"),
        ("email_priority", "优先处理来自领导和客户的邮件", "email_agent"),
        ("work_hours", "工作时间为周一到周五 9:00-18:00", "schedule_agent"),
    ]
    
    for key, value, category in preferences:
        memory.save_knowledge(key, value, category=category)
        print(f"  ✅ 保存: [{category}] {key}")
    
    # 检索知识
    print("\n2️⃣ 检索特定知识:")
    knowledge = memory.get_knowledge("file_organize_rule", category="file_agent")
    print(f"  📖 文件整理规则: {knowledge}")
    
    # 按分类检索
    print("\n3️⃣ 搜索某个智能体的相关知识:")
    email_knowledge = memory.search_knowledge(keyword="邮件", category="email_agent")
    if email_knowledge:
        print(f"  📧 邮件智能体知识: {email_knowledge[0]['value']}")
    else:
        print(f"  📧 未找到邮件相关知识")


def example_3_working_memory():
    """示例3: 工作记忆 (任务状态)"""
    print("\n" + "="*60)
    print("⚙️  示例3: 工作记忆 - 任务状态管理")
    print("="*60)
    
    memory = MemoryManager()
    
    # 创建任务
    print("\n1️⃣ 创建新任务:")
    task_id = "task_file_organize_001"
    initial_state = {
        "status": "pending",
        "task_name": "整理桌面文件",
        "progress": 0.0,
        "start_time": time.time(),
    }
    memory.set_task_state(task_id, initial_state)
    print(f"  ✅ 任务创建: {task_id}")
    print(f"  状态: {initial_state}")
    
    # 更新任务进度
    print("\n2️⃣ 更新任务进度:")
    stages = [
        ("扫描文件", 0.2),
        ("分析文件类型", 0.4),
        ("创建分类目录", 0.6),
        ("移动文件", 0.8),
        ("完成整理", 1.0),
    ]
    
    for stage, progress in stages:
        state = memory.get_task_state(task_id)
        if state is None:
            state = initial_state.copy()
        state["status"] = "running" if progress < 1.0 else "completed"
        state["progress"] = progress
        state["current_stage"] = stage
        memory.set_task_state(task_id, state)
        print(f"  🔄 [{int(progress*100)}%] {stage}")
        time.sleep(0.1)  # 模拟处理时间
    
    # 获取最终状态
    print("\n3️⃣ 任务完成状态:")
    final_state = memory.get_task_state(task_id)
    if final_state:
        print(f"  状态: {final_state['status']}")
        print(f"  进度: {final_state['progress']*100}%")
    else:
        print(f"  ⚠️  未找到任务状态")


def example_4_memory_stats():
    """示例4: 记忆统计信息"""
    print("\n" + "="*60)
    print("📊 示例4: 记忆系统统计")
    print("="*60)
    
    memory = MemoryManager()
    
    # 添加一些测试数据
    for i in range(10):
        memory.add_message("user", f"测试消息 {i}")
        memory.add_message("assistant", f"回复 {i}")
    
    for i in range(5):
        memory.save_knowledge(f"test_key_{i}", f"test_value_{i}", category="test")
    
    for i in range(3):
        memory.set_task_state(f"task_{i}", {"status": "running"})
    
    # 获取统计信息
    stats = memory.get_memory_stats()
    
    print("\n记忆系统统计:")
    print(f"  📝 短期记忆 (对话): {stats.get('short_term_count', 0)} 条")
    print(f"  🧠 长期记忆 (知识): {stats.get('long_term_count', 0)} 条")
    print(f"  ⚙️  工作记忆 (任务): {stats.get('working_memory_count', 0)} 条")
    print(f"  💾 总内存占用: {stats.get('total_size_kb', 0):.2f} KB")


def example_5_memory_cleanup():
    """示例5: 记忆清理和管理"""
    print("\n" + "="*60)
    print("🧹 示例5: 记忆清理和管理")
    print("="*60)
    
    memory = MemoryManager()
    
    # 添加大量消息
    print("\n1️⃣ 添加大量对话消息:")
    for i in range(100):
        memory.add_message("user", f"消息 {i}")
    
    stats_before = memory.get_memory_stats()
    print(f"  对话消息数: {stats_before.get('short_term_count', 0)}")
    
    # 清理旧对话
    print("\n2️⃣ 清理旧对话 (只保留最近20条):")
    recent = memory.get_recent_messages(20)
    # 这里实际应该调用清理方法，示例中简化处理
    print(f"  ✅ 保留最近 {len(recent)} 条消息")
    
    # 清理已完成的任务
    print("\n3️⃣ 清理已完成的任务:")
    memory.set_task_state("old_task_1", {"status": "completed"})
    memory.set_task_state("old_task_2", {"status": "completed"})
    print("  ✅ 标记旧任务为已完成")


def example_6_context_window():
    """示例6: 上下文窗口管理"""
    print("\n" + "="*60)
    print("🪟 示例6: 上下文窗口管理")
    print("="*60)
    
    memory = MemoryManager()
    
    # 模拟长对话
    print("\n模拟长对话场景:")
    for i in range(15):
        memory.add_message("user", f"这是第 {i+1} 轮对话的问题")
        memory.add_message("assistant", f"这是第 {i+1} 轮对话的回答")
    
    # 获取不同大小的上下文窗口
    window_sizes = [5, 10, 20]
    
    for size in window_sizes:
        messages = memory.get_recent_messages(size)
        print(f"\n  窗口大小 {size}: 获取到 {len(messages)} 条消息")
        if messages:
            print(f"    最早: {messages[0]['content']}")
            print(f"    最新: {messages[-1]['content']}")


def main():
    """主函数"""
    print("\n" + "="*70)
    print("🧠 记忆系统详细使用示例")
    print("="*70)
    
    print("\n本示例展示三种记忆类型:")
    print("  1. 短期记忆 - 对话上下文")
    print("  2. 长期记忆 - 知识存储")
    print("  3. 工作记忆 - 任务状态")
    print()
    
    try:
        example_1_short_term_memory()
        example_2_long_term_memory()
        example_3_working_memory()
        example_4_memory_stats()
        example_5_memory_cleanup()
        example_6_context_window()
        
        print("\n" + "="*70)
        print("✅ 所有示例运行完成!")
        print("="*70)
        
        print("\n💡 要点总结:")
        print("   1. 短期记忆用于保存对话历史")
        print("   2. 长期记忆用于存储用户偏好和知识")
        print("   3. 工作记忆用于跟踪任务状态")
        print("   4. 支持统计和清理功能")
        print("   5. 灵活的上下文窗口管理")
        print()
        
    except Exception as e:
        print(f"\n❌ 运行出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
