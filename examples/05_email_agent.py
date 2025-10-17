"""
示例 05: 邮件处理智能体
演示如何使用 EmailAgent 处理邮件相关任务
"""

import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.tools import EmailTools


def example_1_read_emails():
    """示例1: 读取邮件"""
    print("\n" + "="*60)
    print("📧 示例1: 读取邮件")
    print("="*60)
    
    print("\n模拟邮件读取功能...")
    
    # 模拟邮件数据
    mock_emails = [
        {
            "id": "email_001",
            "from": "boss@company.com",
            "to": "me@company.com",
            "subject": "本周工作汇报",
            "date": "2025-10-17 09:30",
            "body": "请准备本周工作汇报，周五前提交。",
            "has_attachment": False
        },
        {
            "id": "email_002",
            "from": "client@partner.com",
            "to": "me@company.com",
            "subject": "项目合作咨询",
            "date": "2025-10-17 10:15",
            "body": "您好，想咨询贵公司的AI解决方案...",
            "has_attachment": True
        },
        {
            "id": "email_003",
            "from": "hr@company.com",
            "to": "all@company.com",
            "subject": "团建活动通知",
            "date": "2025-10-17 11:00",
            "body": "本月团建活动定于下周六举行...",
            "has_attachment": False
        }
    ]
    
    print(f"\n✅ 读取到 {len(mock_emails)} 封邮件:\n")
    for email in mock_emails:
        attachment = "📎" if email['has_attachment'] else ""
        print(f"  [{email['date']}] {attachment}")
        print(f"  发件人: {email['from']}")
        print(f"  主题: {email['subject']}")
        print(f"  预览: {email['body'][:30]}...")
        print()


def example_2_classify_emails():
    """示例2: 邮件智能分类"""
    print("\n" + "="*60)
    print("🏷️  示例2: 邮件智能分类")
    print("="*60)
    
    # 模拟邮件分类
    emails = [
        {"subject": "紧急：服务器宕机", "from": "ops@company.com", "priority": "高"},
        {"subject": "本周工作汇报", "from": "boss@company.com", "priority": "高"},
        {"subject": "项目合作咨询", "from": "client@partner.com", "priority": "中"},
        {"subject": "团建活动通知", "from": "hr@company.com", "priority": "低"},
        {"subject": "系统升级通知", "from": "it@company.com", "priority": "中"},
    ]
    
    print("\n基于规则的邮件分类:")
    
    # 分类规则
    categories = {
        "紧急事务": [],
        "工作任务": [],
        "商务咨询": [],
        "通知公告": []
    }
    
    for email in emails:
        subject = email['subject']
        if "紧急" in subject:
            categories["紧急事务"].append(email)
        elif "汇报" in subject or "任务" in subject:
            categories["工作任务"].append(email)
        elif "咨询" in subject or "合作" in subject:
            categories["商务咨询"].append(email)
        else:
            categories["通知公告"].append(email)
    
    print()
    for category, email_list in categories.items():
        if email_list:
            print(f"📁 {category} ({len(email_list)} 封):")
            for email in email_list:
                print(f"   - [{email['priority']}] {email['subject']}")
            print()


def example_3_generate_reply():
    """示例3: 智能回复生成"""
    print("\n" + "="*60)
    print("✍️  示例3: 智能回复生成")
    print("="*60)
    
    original_email = {
        "from": "client@partner.com",
        "subject": "项目合作咨询",
        "body": """您好，

我们公司对贵公司的AI智能体解决方案很感兴趣，
希望能够了解更多技术细节和商务合作方式。

期待您的回复。

李明
合作伙伴公司"""
    }
    
    print("\n原始邮件:")
    print(f"  发件人: {original_email['from']}")
    print(f"  主题: {original_email['subject']}")
    print(f"  内容:\n{original_email['body']}")
    
    # 模拟AI生成的回复
    reply_draft = """李明先生，您好！

感谢您对我们AI智能体解决方案的关注。

我们的解决方案具有以下特点：
1. 基于大语言模型的智能对话能力
2. 多智能体协作处理复杂任务
3. 完全本地化部署，保护数据隐私
4. 支持灵活定制和二次开发

关于商务合作，我们提供以下方式：
- 技术咨询服务
- 定制化开发
- 技术授权

我会安排专人与您进一步沟通，请问您方便的时间是？

期待与您的合作！

最诚挚的问候
AI解决方案团队"""

    print("\n" + "="*50)
    print("💡 AI生成的回复草稿:")
    print("="*50)
    print(reply_draft)
    
    print("\n✅ 回复建议:")
    print("   - 语气专业友好 ✓")
    print("   - 包含关键信息 ✓")
    print("   - 引导下一步沟通 ✓")


def example_4_filter_emails():
    """示例4: 邮件过滤和检索"""
    print("\n" + "="*60)
    print("🔍 示例4: 邮件过滤和检索")
    print("="*60)
    
    # 模拟邮件数据库
    all_emails = [
        {"id": 1, "subject": "项目A进度更新", "from": "pm@company.com", "date": "2025-10-15", "tags": ["项目", "工作"]},
        {"id": 2, "subject": "发票申请", "from": "finance@company.com", "date": "2025-10-16", "tags": ["财务"]},
        {"id": 3, "subject": "客户需求讨论", "from": "client@partner.com", "date": "2025-10-17", "tags": ["客户", "重要"]},
        {"id": 4, "subject": "周会纪要", "from": "admin@company.com", "date": "2025-10-17", "tags": ["会议"]},
        {"id": 5, "subject": "项目A技术方案", "from": "dev@company.com", "date": "2025-10-17", "tags": ["项目", "技术"]},
    ]
    
    # 过滤场景
    filters = [
        ("今天的邮件", lambda e: e['date'] == "2025-10-17"),
        ("包含'项目A'的邮件", lambda e: "项目A" in e['subject']),
        ("标记为'重要'的邮件", lambda e: "重要" in e['tags']),
    ]
    
    print("\n邮件过滤演示:")
    for filter_name, filter_func in filters:
        filtered = [e for e in all_emails if filter_func(e)]
        print(f"\n📌 {filter_name} ({len(filtered)} 封):")
        for email in filtered:
            print(f"   - {email['subject']} (来自: {email['from']})")


def example_5_batch_operations():
    """示例5: 批量操作"""
    print("\n" + "="*60)
    print("⚡ 示例5: 批量邮件操作")
    print("="*60)
    
    emails = [
        {"id": "e1", "subject": "广告推广", "category": "垃圾邮件"},
        {"id": "e2", "subject": "中奖通知", "category": "垃圾邮件"},
        {"id": "e3", "subject": "项目更新", "category": "工作"},
        {"id": "e4", "subject": "营销邮件", "category": "垃圾邮件"},
        {"id": "e5", "subject": "会议邀请", "category": "工作"},
    ]
    
    print("\n待处理邮件:")
    for email in emails:
        print(f"  [{email['category']}] {email['subject']}")
    
    # 批量删除垃圾邮件
    print("\n🗑️  批量删除垃圾邮件...")
    spam_emails = [e for e in emails if e['category'] == "垃圾邮件"]
    print(f"   删除 {len(spam_emails)} 封垃圾邮件")
    for email in spam_emails:
        print(f"   ✓ 已删除: {email['subject']}")
    
    # 批量标记工作邮件
    print("\n🏷️  批量标记工作邮件...")
    work_emails = [e for e in emails if e['category'] == "工作"]
    print(f"   标记 {len(work_emails)} 封工作邮件为'重要'")
    for email in work_emails:
        print(f"   ✓ 已标记: {email['subject']}")
    
    print("\n✅ 批量操作完成!")


def example_6_email_workflow():
    """示例6: 完整邮件处理工作流"""
    print("\n" + "="*60)
    print("🔄 示例6: 完整邮件处理工作流")
    print("="*60)
    
    print("\n场景: 每日邮件处理自动化")
    print("\n工作流程:")
    
    steps = [
        ("1. 连接邮箱", "连接到邮件服务器", "成功"),
        ("2. 读取新邮件", "获取今天的未读邮件", "找到 25 封"),
        ("3. 垃圾邮件过滤", "识别并移除垃圾邮件", "移除 8 封"),
        ("4. 智能分类", "将邮件分类到不同文件夹", "分为 4 类"),
        ("5. 优先级排序", "按重要性排序", "高优先级 5 封"),
        ("6. 自动回复", "对常见问题自动回复", "回复 3 封"),
        ("7. 生成摘要", "汇总重要邮件", "生成日报"),
        ("8. 发送通知", "提醒用户处理紧急邮件", "已通知"),
    ]
    
    for step_num, action, result in steps:
        print(f"\n  {step_num}")
        print(f"    操作: {action}")
        print(f"    结果: {result} ✓")
    
    print("\n" + "="*50)
    print("📊 处理结果汇总:")
    print("="*50)
    print("""
  总邮件数: 25 封
  垃圾邮件: 8 封 (已删除)
  工作邮件: 12 封
  个人邮件: 5 封
  
  高优先级: 5 封 (需立即处理)
  中优先级: 10 封
  低优先级: 2 封
  
  自动回复: 3 封
  待处理: 14 封
    """)
    
    print("💡 节省时间: 约 30 分钟")


def main():
    """主函数"""
    print("\n" + "="*70)
    print("📧 邮件处理智能体使用示例")
    print("="*70)
    
    print("\n本示例展示邮件智能体的各种功能")
    print("包括读取、分类、回复、过滤和批量操作等")
    print()
    
    try:
        example_1_read_emails()
        example_2_classify_emails()
        example_3_generate_reply()
        example_4_filter_emails()
        example_5_batch_operations()
        example_6_email_workflow()
        
        print("\n" + "="*70)
        print("✅ 所有示例运行完成!")
        print("="*70)
        
        print("\n💡 功能总结:")
        print("   1. 邮件读取 - 连接邮箱读取邮件")
        print("   2. 智能分类 - 基于规则和AI分类")
        print("   3. 自动回复 - AI生成专业回复")
        print("   4. 邮件过滤 - 多条件筛选检索")
        print("   5. 批量操作 - 提高处理效率")
        print("   6. 工作流自动化 - 完整处理流程")
        
        print("\n🎯 应用场景:")
        print("   • 每日邮件自动整理")
        print("   • 重要邮件优先提醒")
        print("   • 常见问题自动回复")
        print("   • 垃圾邮件智能过滤")
        print("   • 邮件归档和备份")
        print()
        
    except Exception as e:
        print(f"\n❌ 运行出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

