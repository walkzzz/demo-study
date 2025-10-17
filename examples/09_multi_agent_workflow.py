"""
示例 09: 多智能体协作工作流
演示如何使用超级智能体协调多个专业智能体完成复杂任务
"""

import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.core import ModelManager, MemoryManager, PromptEngine
from src.tools import FileSystemTools


def scenario_1_email_and_file():
    """场景1: 邮件处理 + 文件整理"""
    print("\n" + "="*60)
    print("📧 场景1: 处理邮件附件并整理")
    print("="*60)
    
    print("\n用户请求: '下载今天的邮件附件并整理到对应文件夹'")
    print("\n任务分解:")
    print("  1️⃣ EmailAgent: 获取今天的邮件")
    print("  2️⃣ EmailAgent: 下载附件")
    print("  3️⃣ FileAgent: 扫描下载目录")
    print("  4️⃣ FileAgent: 按类型分类文件")
    print("  5️⃣ FileAgent: 移动文件到对应文件夹")
    
    print("\n执行流程:")
    steps = [
        ("EmailAgent", "连接邮件服务器", "成功"),
        ("EmailAgent", "筛选今天的邮件", "找到 15 封"),
        ("EmailAgent", "下载附件", "下载 8 个文件"),
        ("FileAgent", "扫描下载目录", "发现 8 个新文件"),
        ("FileAgent", "文件分类", "文档3个，图片4个，压缩包1个"),
        ("FileAgent", "创建目标目录", "成功"),
        ("FileAgent", "移动文件", "全部移动完成"),
    ]
    
    for agent, action, result in steps:
        print(f"  [{agent}] {action}... {result}")
    
    print("\n✅ 任务完成!")
    print("   - 处理邮件: 15 封")
    print("   - 下载附件: 8 个")
    print("   - 整理文件: 3 类")


def scenario_2_data_and_doc():
    """场景2: 数据分析 + 报告生成"""
    print("\n" + "="*60)
    print("📊 场景2: 分析销售数据并生成报告")
    print("="*60)
    
    print("\n用户请求: '分析本月销售数据并生成PPT报告'")
    print("\n任务分解:")
    print("  1️⃣ DataAgent: 读取销售数据")
    print("  2️⃣ DataAgent: 数据清洗和统计")
    print("  3️⃣ DataAgent: 生成图表")
    print("  4️⃣ DocAgent: 创建PPT框架")
    print("  5️⃣ DocAgent: 插入图表和数据")
    print("  6️⃣ DocAgent: 添加分析结论")
    
    print("\n执行流程:")
    steps = [
        ("DataAgent", "加载数据", "成功加载 500 条记录"),
        ("DataAgent", "数据验证", "发现 5 条异常数据"),
        ("DataAgent", "数据清洗", "清洗完成"),
        ("DataAgent", "统计分析", "计算关键指标"),
        ("DataAgent", "生成图表", "创建 4 个图表"),
        ("DocAgent", "创建PPT", "使用默认模板"),
        ("DocAgent", "添加封面", "添加标题和日期"),
        ("DocAgent", "插入数据页", "添加 4 个图表"),
        ("DocAgent", "添加结论页", "基于分析结果"),
        ("DocAgent", "保存文件", "reports/sales_202510.pptx"),
    ]
    
    for agent, action, result in steps:
        print(f"  [{agent}] {action}... {result}")
    
    print("\n✅ 任务完成!")
    print("   - 分析数据: 500 条")
    print("   - 生成图表: 4 个")
    print("   - 创建PPT: 1 个")


def scenario_3_knowledge_and_schedule():
    """场景3: 知识检索 + 会议安排"""
    print("\n" + "="*60)
    print("📅 场景3: 准备会议资料并安排会议")
    print("="*60)
    
    print("\n用户请求: '准备下周产品评审会议，整理相关资料'")
    print("\n任务分解:")
    print("  1️⃣ ScheduleAgent: 检查下周空闲时间")
    print("  2️⃣ ScheduleAgent: 预定会议室")
    print("  3️⃣ KnowledgeAgent: 检索产品文档")
    print("  4️⃣ KnowledgeAgent: 整理评审要点")
    print("  5️⃣ EmailAgent: 发送会议通知")
    
    print("\n执行流程:")
    steps = [
        ("ScheduleAgent", "查询空闲时间", "周三下午2-4点可用"),
        ("ScheduleAgent", "检查参会人日程", "全员可参加"),
        ("ScheduleAgent", "预定会议室", "A301 已预定"),
        ("ScheduleAgent", "创建日程事件", "已添加到日历"),
        ("KnowledgeAgent", "搜索产品文档", "找到 12 个相关文档"),
        ("KnowledgeAgent", "提取关键信息", "整理 5 个评审要点"),
        ("KnowledgeAgent", "生成摘要", "创建评审清单"),
        ("EmailAgent", "准备通知", "包含时间地点和资料"),
        ("EmailAgent", "发送邮件", "已发送给 8 位参会人"),
    ]
    
    for agent, action, result in steps:
        print(f"  [{agent}] {action}... {result}")
    
    print("\n✅ 任务完成!")
    print("   - 会议时间: 周三 14:00-16:00")
    print("   - 会议室: A301")
    print("   - 通知发送: 8 人")


def scenario_4_full_workflow():
    """场景4: 完整工作流演示"""
    print("\n" + "="*60)
    print("🔄 场景4: 周报准备完整流程")
    print("="*60)
    
    print("\n用户请求: '准备本周工作周报'")
    print("\n智能体协作流程:")
    
    # 任务规划
    print("\n【任务规划】SuperAgent 分析任务")
    print("  识别所需智能体:")
    print("    - DataAgent: 统计本周工作数据")
    print("    - EmailAgent: 回顾本周重要邮件")
    print("    - ScheduleAgent: 统计会议时间")
    print("    - DocAgent: 生成周报文档")
    
    # 并行执行
    print("\n【并行执行】多智能体同时工作")
    print("  [DataAgent]")
    print("    ├─ 读取项目进度数据")
    print("    ├─ 统计完成任务数: 8")
    print("    └─ 计算工作时长: 40小时")
    
    print("  [EmailAgent]")
    print("    ├─ 扫描本周邮件: 120封")
    print("    ├─ 筛选重要邮件: 15封")
    print("    └─ 提取关键事项: 5个")
    
    print("  [ScheduleAgent]")
    print("    ├─ 统计会议次数: 6次")
    print("    ├─ 计算会议时长: 8小时")
    print("    └─ 提取重要决议: 3条")
    
    # 结果汇总
    print("\n【结果汇总】DocAgent 整合信息")
    print("  [DocAgent]")
    print("    ├─ 创建Word文档")
    print("    ├─ 添加工作数据")
    print("    ├─ 添加邮件摘要")
    print("    ├─ 添加会议记录")
    print("    ├─ 生成工作计划")
    print("    └─ 保存: reports/weekly_202510_week3.docx")
    
    # 最终输出
    print("\n【任务完成】SuperAgent 总结")
    print("  ✅ 周报已生成")
    print("  📊 包含内容:")
    print("     - 完成任务: 8个")
    print("     - 工作时长: 40小时")
    print("     - 重要邮件: 15封")
    print("     - 会议记录: 6次")
    print("  📁 文件位置: reports/weekly_202510_week3.docx")


def scenario_5_error_handling():
    """场景5: 错误处理和恢复"""
    print("\n" + "="*60)
    print("⚠️  场景5: 错误处理演示")
    print("="*60)
    
    print("\n用户请求: '整理文件并发送邮件通知'")
    print("\n执行过程:")
    
    steps = [
        ("FileAgent", "扫描目录", "成功", "✅"),
        ("FileAgent", "文件分类", "成功", "✅"),
        ("FileAgent", "移动文件", "成功", "✅"),
        ("EmailAgent", "连接邮件服务器", "失败: 网络超时", "❌"),
    ]
    
    for agent, action, result, status in steps:
        print(f"  [{agent}] {action}... {result} {status}")
    
    print("\n【错误处理】SuperAgent 分析错误")
    print("  检测到: EmailAgent 网络连接失败")
    print("  决策: 重试发送邮件")
    
    print("\n【重试执行】")
    retry_steps = [
        ("EmailAgent", "等待 5 秒", "完成", "⏳"),
        ("EmailAgent", "重新连接", "成功", "✅"),
        ("EmailAgent", "发送通知", "成功", "✅"),
    ]
    
    for agent, action, result, status in retry_steps:
        print(f"  [{agent}] {action}... {result} {status}")
    
    print("\n✅ 任务最终完成!")
    print("   总计重试: 1 次")


def main():
    """主函数"""
    print("\n" + "="*70)
    print("🤖 多智能体协作工作流示例")
    print("="*70)
    
    print("\n本示例展示不同智能体如何协作完成复杂任务")
    print("这是一个演示流程，展示任务分解和协作模式")
    print()
    
    try:
        scenario_1_email_and_file()
        scenario_2_data_and_doc()
        scenario_3_knowledge_and_schedule()
        scenario_4_full_workflow()
        scenario_5_error_handling()
        
        print("\n" + "="*70)
        print("✅ 所有场景演示完成!")
        print("="*70)
        
        print("\n💡 协作模式总结:")
        print("   1. 任务分解 - SuperAgent 将复杂任务拆分")
        print("   2. 智能体选择 - 根据任务类型选择专业智能体")
        print("   3. 并行执行 - 多个智能体同时工作")
        print("   4. 结果汇总 - 整合各智能体的输出")
        print("   5. 错误处理 - 检测失败并自动重试")
        
        print("\n🎯 核心优势:")
        print("   • 专业分工 - 每个智能体专注特定领域")
        print("   • 高效协作 - 并行处理提升效率")
        print("   • 智能决策 - 自动选择最优执行路径")
        print("   • 容错能力 - 自动处理异常情况")
        print()
        
    except Exception as e:
        print(f"\n❌ 运行出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
