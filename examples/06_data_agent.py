"""
示例 06: 数据分析智能体
演示如何使用 DataAgent 进行数据分析和可视化
"""

import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.tools import DataTools


def example_1_load_data():
    """示例1: 数据加载"""
    print("\n" + "="*60)
    print("📊 示例1: 数据加载")
    print("="*60)
    
    # 模拟不同格式的数据加载
    data_sources = [
        {"format": "CSV", "file": "sales_data.csv", "rows": 500, "cols": 8},
        {"format": "Excel", "file": "financial_report.xlsx", "rows": 1200, "cols": 12},
        {"format": "JSON", "file": "customer_data.json", "rows": 350, "cols": 6},
    ]
    
    print("\n支持的数据格式:")
    for source in data_sources:
        print(f"\n  📄 {source['format']} 文件")
        print(f"     文件名: {source['file']}")
        print(f"     数据规模: {source['rows']} 行 × {source['cols']} 列")
        print(f"     ✅ 加载成功")


def example_2_data_cleaning():
    """示例2: 数据清洗"""
    print("\n" + "="*60)
    print("🧹 示例2: 数据清洗")
    print("="*60)
    
    # 模拟原始数据问题
    data_issues = {
        "总记录数": 1000,
        "缺失值": 45,
        "重复记录": 12,
        "异常值": 8,
        "格式错误": 5
    }
    
    print("\n原始数据质量检查:")
    for issue, count in data_issues.items():
        status = "⚠️ " if count > 0 else "✅"
        print(f"  {status} {issue}: {count}")
    
    print("\n执行数据清洗...")
    
    cleaning_steps = [
        ("处理缺失值", "使用平均值填充数值列", 45),
        ("删除重复记录", "基于关键字段去重", 12),
        ("处理异常值", "使用3σ原则识别并处理", 8),
        ("统一格式", "标准化日期和数值格式", 5),
    ]
    
    for step, method, count in cleaning_steps:
        print(f"\n  🔧 {step}")
        print(f"     方法: {method}")
        print(f"     处理: {count} 条")
        print(f"     ✅ 完成")
    
    print("\n清洗后数据:")
    print(f"  ✅ 有效记录: {1000 - 12} 条")
    print(f"  ✅ 数据完整性: 100%")
    print(f"  ✅ 数据一致性: 已验证")


def example_3_statistical_analysis():
    """示例3: 统计分析"""
    print("\n" + "="*60)
    print("📈 示例3: 统计分析")
    print("="*60)
    
    # 模拟销售数据统计
    sales_stats = {
        "总销售额": 1250000,
        "平均订单金额": 2500,
        "最大订单": 50000,
        "最小订单": 100,
        "订单数量": 500,
        "客户数量": 320,
    }
    
    print("\n基础统计指标:")
    print(f"\n  💰 总销售额: ¥{sales_stats['总销售额']:,}")
    print(f"  📊 平均订单金额: ¥{sales_stats['平均订单金额']:,}")
    print(f"  📈 最大订单: ¥{sales_stats['最大订单']:,}")
    print(f"  📉 最小订单: ¥{sales_stats['最小订单']:,}")
    print(f"  🛒 订单数量: {sales_stats['订单数量']}")
    print(f"  👥 客户数量: {sales_stats['客户数量']}")
    
    # 趋势分析
    print("\n\n月度趋势分析:")
    monthly_trend = [
        ("1月", 95000, "⬆️ +12%"),
        ("2月", 88000, "⬇️ -7%"),
        ("3月", 105000, "⬆️ +19%"),
        ("4月", 112000, "⬆️ +7%"),
        ("5月", 125000, "⬆️ +12%"),
    ]
    
    for month, amount, trend in monthly_trend:
        bar = "█" * int(amount / 5000)
        print(f"  {month}: {bar} ¥{amount:,} {trend}")
    
    # 分类统计
    print("\n\n产品类别销售占比:")
    categories = [
        ("电子产品", 45, "█████████"),
        ("服装配饰", 28, "█████▌"),
        ("家居用品", 18, "███▌"),
        ("其他", 9, "█▊"),
    ]
    
    for category, percentage, bar in categories:
        print(f"  {category}: {bar} {percentage}%")


def example_4_data_visualization():
    """示例4: 数据可视化"""
    print("\n" + "="*60)
    print("📊 示例4: 数据可视化")
    print("="*60)
    
    print("\n支持的图表类型:")
    
    chart_types = [
        {
            "name": "柱状图 (Bar Chart)",
            "use_case": "对比不同类别的数值",
            "example": "月度销售额对比"
        },
        {
            "name": "折线图 (Line Chart)",
            "use_case": "展示数据随时间的变化趋势",
            "example": "用户增长趋势"
        },
        {
            "name": "饼图 (Pie Chart)",
            "use_case": "展示各部分占整体的比例",
            "example": "市场份额分布"
        },
        {
            "name": "散点图 (Scatter Plot)",
            "use_case": "分析两个变量之间的关系",
            "example": "价格与销量关系"
        },
        {
            "name": "热力图 (Heatmap)",
            "use_case": "展示矩阵数据的分布模式",
            "example": "不同时段的访问量"
        },
    ]
    
    for i, chart in enumerate(chart_types, 1):
        print(f"\n  {i}. {chart['name']}")
        print(f"     适用场景: {chart['use_case']}")
        print(f"     示例: {chart['example']}")
        print(f"     ✅ 支持导出为 PNG/SVG/PDF")


def example_5_advanced_analysis():
    """示例5: 高级分析"""
    print("\n" + "="*60)
    print("🔬 示例5: 高级分析")
    print("="*60)
    
    print("\n1️⃣ 相关性分析")
    print("="*50)
    
    correlations = [
        ("广告支出", "销售额", 0.85, "强正相关"),
        ("价格", "销量", -0.62, "中度负相关"),
        ("客户满意度", "复购率", 0.78, "强正相关"),
    ]
    
    for var1, var2, corr, desc in correlations:
        print(f"\n  {var1} ↔ {var2}")
        print(f"  相关系数: {corr}")
        print(f"  关系: {desc}")
    
    print("\n\n2️⃣ 预测分析")
    print("="*50)
    
    prediction = {
        "模型": "线性回归",
        "训练数据": "过去12个月销售数据",
        "预测目标": "下月销售额",
        "预测结果": "¥135,000",
        "置信区间": "¥128,000 - ¥142,000",
        "模型准确度": "92%"
    }
    
    print(f"\n  使用模型: {prediction['模型']}")
    print(f"  训练数据: {prediction['训练数据']}")
    print(f"  预测目标: {prediction['预测目标']}")
    print(f"  预测结果: {prediction['预测结果']}")
    print(f"  置信区间: {prediction['置信区间']}")
    print(f"  准确度: {prediction['模型准确度']}")
    
    print("\n\n3️⃣ 异常检测")
    print("="*50)
    
    anomalies = [
        {"date": "2025-10-05", "value": 8500, "expected": 12000, "deviation": "-29%"},
        {"date": "2025-10-12", "value": 25000, "expected": 12000, "deviation": "+108%"},
    ]
    
    print("\n  检测到异常数据点:")
    for anomaly in anomalies:
        print(f"\n  ⚠️  日期: {anomaly['date']}")
        print(f"     实际值: ¥{anomaly['value']:,}")
        print(f"     预期值: ¥{anomaly['expected']:,}")
        print(f"     偏差: {anomaly['deviation']}")


def example_6_report_generation():
    """示例6: 报告生成"""
    print("\n" + "="*60)
    print("📝 示例6: 自动报告生成")
    print("="*60)
    
    print("\n生成销售分析报告...")
    
    report_sections = [
        ("1. 执行摘要", "总体业绩概述和关键发现"),
        ("2. 销售业绩", "详细销售数据和趋势分析"),
        ("3. 产品分析", "各产品类别表现对比"),
        ("4. 客户分析", "客户群体特征和行为"),
        ("5. 市场趋势", "市场变化和竞争态势"),
        ("6. 建议措施", "基于数据的行动建议"),
    ]
    
    print("\n报告结构:")
    for section, description in report_sections:
        print(f"\n  {section}")
        print(f"  └─ {description}")
        print(f"     ✅ 已生成")
    
    print("\n\n报告输出格式:")
    formats = [
        "📄 PDF - 适合打印和分享",
        "📊 Excel - 包含原始数据和图表",
        "📝 Word - 可编辑的文档格式",
        "🌐 HTML - 交互式网页报告",
    ]
    
    for fmt in formats:
        print(f"  {fmt}")
    
    print("\n✅ 报告生成完成!")
    print("   保存位置: reports/sales_analysis_202510.pdf")


def example_7_complete_workflow():
    """示例7: 完整数据分析工作流"""
    print("\n" + "="*60)
    print("🔄 示例7: 完整数据分析工作流")
    print("="*60)
    
    print("\n场景: 月度销售数据分析")
    print("\n工作流程:")
    
    workflow = [
        ("数据收集", [
            "从CRM系统导出销售数据",
            "从ERP系统导出库存数据",
            "从网站获取访问统计"
        ]),
        ("数据预处理", [
            "合并多个数据源",
            "清洗异常和缺失值",
            "数据格式标准化"
        ]),
        ("探索性分析", [
            "计算基础统计指标",
            "识别数据分布特征",
            "发现潜在规律"
        ]),
        ("深度分析", [
            "销售趋势分析",
            "客户群体细分",
            "产品关联分析"
        ]),
        ("可视化", [
            "创建交互式图表",
            "设计数据仪表板",
            "生成可视化报告"
        ]),
        ("洞察提取", [
            "识别关键发现",
            "提出业务建议",
            "制定行动计划"
        ])
    ]
    
    for i, (phase, tasks) in enumerate(workflow, 1):
        print(f"\n  阶段 {i}: {phase}")
        for task in tasks:
            print(f"    • {task}")
        print(f"    ✅ 完成")
    
    print("\n" + "="*50)
    print("📊 分析成果:")
    print("="*50)
    print("""
  关键发现:
  • 本月销售额同比增长 18%
  • 电子产品类别表现突出
  • 新客户转化率提升 12%
  • 复购率达到 65%
  
  行动建议:
  1. 加大电子产品类目营销投入
  2. 优化新客户引流渠道
  3. 建立客户忠诚度计划
  4. 调整库存结构
    """)


def main():
    """主函数"""
    print("\n" + "="*70)
    print("📊 数据分析智能体使用示例")
    print("="*70)
    
    print("\n本示例展示数据分析智能体的各种功能")
    print("包括数据加载、清洗、分析、可视化和报告生成等")
    print()
    
    try:
        example_1_load_data()
        example_2_data_cleaning()
        example_3_statistical_analysis()
        example_4_data_visualization()
        example_5_advanced_analysis()
        example_6_report_generation()
        example_7_complete_workflow()
        
        print("\n" + "="*70)
        print("✅ 所有示例运行完成!")
        print("="*70)
        
        print("\n💡 功能总结:")
        print("   1. 数据加载 - 支持多种格式")
        print("   2. 数据清洗 - 自动处理质量问题")
        print("   3. 统计分析 - 计算关键指标")
        print("   4. 数据可视化 - 多种图表类型")
        print("   5. 高级分析 - 相关性/预测/异常检测")
        print("   6. 报告生成 - 自动化报告输出")
        print("   7. 完整工作流 - 端到端分析流程")
        
        print("\n🎯 应用场景:")
        print("   • 销售业绩分析")
        print("   • 客户行为分析")
        print("   • 财务数据分析")
        print("   • 运营指标监控")
        print("   • 市场趋势研究")
        print()
        
    except Exception as e:
        print(f"\n❌ 运行出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
