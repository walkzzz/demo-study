"""
示例 07: 文档处理智能体
演示如何使用 DocAgent 处理各种文档任务
"""

import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.tools import FileTools


def example_1_format_conversion():
    """示例1: 文档格式转换"""
    print("\n" + "="*60)
    print("🔄 示例1: 文档格式转换")
    print("="*60)
    
    # 支持的格式转换
    conversions = [
        ("Word → PDF", "project_proposal.docx", "project_proposal.pdf", "保持格式完整"),
        ("Markdown → HTML", "README.md", "README.html", "适合网页展示"),
        ("Excel → CSV", "data.xlsx", "data.csv", "便于数据处理"),
        ("PPT → PDF", "presentation.pptx", "presentation.pdf", "便于分享"),
        ("TXT → Word", "notes.txt", "notes.docx", "格式化文本"),
    ]
    
    print("\n支持的格式转换:")
    for conversion, source, target, purpose in conversions:
        print(f"\n  {conversion}")
        print(f"  源文件: {source}")
        print(f"  目标文件: {target}")
        print(f"  用途: {purpose}")
        print(f"  ✅ 转换成功")


def example_2_document_extraction():
    """示例2: 文档内容提取"""
    print("\n" + "="*60)
    print("📄 示例2: 文档内容提取")
    print("="*60)
    
    # 模拟PDF文档
    pdf_content = {
        "title": "2025年度业务计划",
        "author": "战略规划部",
        "pages": 25,
        "sections": [
            "第一章: 市场分析",
            "第二章: 业务目标",
            "第三章: 实施计划",
            "第四章: 预算分配",
            "第五章: 风险评估"
        ],
        "images": 8,
        "tables": 12
    }
    
    print("\n从PDF提取的信息:")
    print(f"\n  📋 文档标题: {pdf_content['title']}")
    print(f"  👤 作者: {pdf_content['author']}")
    print(f"  📃 页数: {pdf_content['pages']}")
    
    print(f"\n  📑 章节结构:")
    for section in pdf_content['sections']:
        print(f"     • {section}")
    
    print(f"\n  📊 内容统计:")
    print(f"     图片: {pdf_content['images']} 张")
    print(f"     表格: {pdf_content['tables']} 个")
    
    # 提取表格数据
    print("\n  📊 提取表格数据示例:")
    table_data = [
        ["季度", "目标", "实际", "完成率"],
        ["Q1", "100万", "108万", "108%"],
        ["Q2", "120万", "115万", "96%"],
        ["Q3", "130万", "142万", "109%"],
    ]
    
    for row in table_data:
        print(f"     {' | '.join(str(cell).ljust(8) for cell in row)}")


def example_3_document_summary():
    """示例3: 文档智能摘要"""
    print("\n" + "="*60)
    print("📝 示例3: 文档智能摘要")
    print("="*60)
    
    # 模拟长文档
    document = {
        "title": "人工智能技术白皮书",
        "length": 15000,  # 字数
        "content": """
        人工智能(AI)正在快速发展并深刻影响各行各业。
        大语言模型的突破使AI能够更好地理解和生成自然语言。
        企业应用AI技术可以提高效率、降低成本、改善客户体验。
        但同时也需要注意数据隐私、算法偏见等伦理问题。
        未来AI将更加普及，成为数字化转型的关键驱动力。
        """
    }
    
    print(f"\n原始文档:")
    print(f"  标题: {document['title']}")
    print(f"  字数: {document['length']:,} 字")
    print(f"  预计阅读时间: {document['length'] // 300} 分钟")
    
    # AI生成的摘要
    summaries = {
        "极简版 (50字)": "AI技术快速发展,大模型带来突破。企业应用可提效降本,但需注意伦理问题。AI将成为数字化转型关键。",
        "简要版 (150字)": """人工智能技术正在快速发展,特别是大语言模型的突破性进展,
使AI能够更好地理解和处理自然语言。企业应用AI可以显著提高运营效率、
降低成本并改善客户体验。同时需要关注数据隐私保护和算法公平性等伦理问题。
未来AI将更加普及,成为推动企业数字化转型的关键驱动力。""",
        "详细版 (300字)": """本白皮书全面介绍了人工智能技术的发展现状和应用前景。
AI技术正经历快速发展期,尤其是大语言模型的突破,使机器能够更好地理解和生成人类语言。
在企业应用方面,AI可以通过自动化流程、智能决策支持、个性化服务等方式,
显著提升运营效率、降低人力成本、改善客户满意度。
然而,AI技术的应用也面临诸多挑战,包括数据隐私保护、算法透明度、
潜在偏见等伦理问题,需要建立完善的治理框架。
展望未来,AI将更加普及化和平民化,成为推动各行业数字化转型的核心驱动力,
企业需要及早布局以保持竞争优势。"""
    }
    
    print("\n生成的摘要:")
    for summary_type, content in summaries.items():
        print(f"\n  {summary_type}")
        print(f"  {'-'*55}")
        print(f"  {content}")


def example_4_document_comparison():
    """示例4: 文档对比"""
    print("\n" + "="*60)
    print("🔍 示例4: 文档对比")
    print("="*60)
    
    print("\n对比两份合同的差异...")
    
    # 模拟文档对比结果
    comparison = {
        "文档1": "合同_v1.0.docx",
        "文档2": "合同_v2.0.docx",
        "相似度": "87%",
        "差异总数": 15,
        "差异分类": {
            "新增内容": 8,
            "删除内容": 3,
            "修改内容": 4
        }
    }
    
    print(f"\n基本信息:")
    print(f"  文档1: {comparison['文档1']}")
    print(f"  文档2: {comparison['文档2']}")
    print(f"  相似度: {comparison['相似度']}")
    print(f"  差异总数: {comparison['差异总数']} 处")
    
    print(f"\n差异分类:")
    for diff_type, count in comparison['差异分类'].items():
        print(f"  • {diff_type}: {count} 处")
    
    # 详细差异
    detailed_diffs = [
        ("新增", "第3条", "增加了违约责任条款"),
        ("修改", "第5条", "付款期限从30天改为45天"),
        ("修改", "第7条", "保密期限从1年延长至3年"),
        ("删除", "附录A", "删除了原有的技术规格说明"),
        ("新增", "附录C", "新增知识产权归属说明"),
    ]
    
    print(f"\n关键差异详情:")
    for change_type, location, description in detailed_diffs:
        icon = {"新增": "➕", "删除": "➖", "修改": "✏️"}[change_type]
        print(f"  {icon} [{location}] {description}")
    
    print("\n✅ 对比报告已生成: comparison_report.pdf")


def example_5_document_merge():
    """示例5: 文档合并"""
    print("\n" + "="*60)
    print("📑 示例5: 文档合并")
    print("="*60)
    
    # 要合并的文档列表
    documents = [
        {"name": "第一章_市场分析.docx", "pages": 8},
        {"name": "第二章_产品策略.docx", "pages": 12},
        {"name": "第三章_营销计划.docx", "pages": 15},
        {"name": "第四章_财务预算.docx", "pages": 10},
        {"name": "附录_数据报表.docx", "pages": 6},
    ]
    
    print("\n待合并的文档:")
    total_pages = 0
    for i, doc in enumerate(documents, 1):
        print(f"  {i}. {doc['name']} ({doc['pages']} 页)")
        total_pages += doc['pages']
    
    print(f"\n合并设置:")
    print(f"  • 保持原始格式")
    print(f"  • 自动生成目录")
    print(f"  • 添加页眉页脚")
    print(f"  • 统一页码编号")
    
    print(f"\n正在合并...")
    for doc in documents:
        print(f"  ✓ 已处理: {doc['name']}")
    
    print(f"\n✅ 合并完成!")
    print(f"  输出文件: 年度业务计划_完整版.docx")
    print(f"  总页数: {total_pages} 页")


def example_6_template_filling():
    """示例6: 模板填充"""
    print("\n" + "="*60)
    print("📋 示例6: 模板自动填充")
    print("="*60)
    
    # 合同模板变量
    template_vars = {
        "甲方名称": "科技创新有限公司",
        "乙方名称": "智能系统集成公司",
        "合同编号": "CONTRACT-2025-10-001",
        "签订日期": "2025年10月17日",
        "项目名称": "AI智能体系统开发",
        "合同金额": "500,000",
        "付款方式": "分三期支付",
        "交付期限": "2025年12月31日",
    }
    
    print("\n使用模板: 服务合同模板.docx")
    print("\n填充数据:")
    for key, value in template_vars.items():
        print(f"  {key}: {value}")
    
    print("\n执行填充...")
    print("  ✓ 替换变量占位符")
    print("  ✓ 格式化日期和金额")
    print("  ✓ 更新文档属性")
    print("  ✓ 生成条形码")
    
    print("\n✅ 生成文档: 服务合同_2025-10-001.docx")
    
    # 批量生成
    print("\n\n批量生成示例:")
    batch_count = 5
    print(f"  基于模板批量生成 {batch_count} 份文档...")
    for i in range(1, batch_count + 1):
        print(f"  ✓ 已生成: 合同_2025-10-{str(i).zfill(3)}.docx")


def example_7_ocr_processing():
    """示例7: OCR文字识别"""
    print("\n" + "="*60)
    print("🔍 示例7: OCR文字识别")
    print("="*60)
    
    print("\n场景: 从扫描件中提取文字")
    
    # 模拟OCR处理
    ocr_tasks = [
        {
            "file": "合同扫描件.pdf",
            "pages": 5,
            "language": "中文+英文",
            "quality": "高",
            "extracted_chars": 3500
        },
        {
            "file": "身份证照片.jpg",
            "pages": 1,
            "language": "中文",
            "quality": "中",
            "extracted_chars": 120
        },
        {
            "file": "发票图片.png",
            "pages": 1,
            "language": "中文+数字",
            "quality": "高",
            "extracted_chars": 250
        }
    ]
    
    for task in ocr_tasks:
        print(f"\n  处理文件: {task['file']}")
        print(f"  页数: {task['pages']}")
        print(f"  语言: {task['language']}")
        print(f"  图像质量: {task['quality']}")
        print(f"  识别字符数: {task['extracted_chars']}")
        print(f"  ✅ 识别完成")
    
    # 识别结果示例
    print("\n发票识别结果示例:")
    invoice_data = {
        "发票号码": "No.12345678",
        "开票日期": "2025-10-15",
        "购买方": "科技创新有限公司",
        "销售方": "办公用品商城",
        "金额": "¥2,580.00",
        "税额": "¥335.40"
    }
    
    print()
    for field, value in invoice_data.items():
        print(f"  {field}: {value}")


def example_8_complete_workflow():
    """示例8: 完整文档处理工作流"""
    print("\n" + "="*60)
    print("🔄 示例8: 完整文档处理工作流")
    print("="*60)
    
    print("\n场景: 准备项目投标文件")
    print("\n工作流程:")
    
    workflow_steps = [
        ("收集素材", [
            "公司介绍 (Word)",
            "项目案例 (PPT)",
            "技术方案 (Markdown)",
            "财务报价 (Excel)"
        ]),
        ("格式转换", [
            "PPT → PDF (保持格式)",
            "Markdown → Word (添加样式)",
            "Excel → 图表 (可视化)"
        ]),
        ("内容整合", [
            "合并所有文档",
            "统一格式样式",
            "生成目录索引"
        ]),
        ("智能优化", [
            "提取关键摘要",
            "优化排版布局",
            "检查拼写语法"
        ]),
        ("最终输出", [
            "生成PDF版本",
            "添加水印保护",
            "创建电子签名"
        ])
    ]
    
    for i, (phase, tasks) in enumerate(workflow_steps, 1):
        print(f"\n  阶段 {i}: {phase}")
        for task in tasks:
            print(f"    ✓ {task}")
    
    print("\n" + "="*50)
    print("📊 处理结果:")
    print("="*50)
    print("""
  输入文件: 15 个 (多种格式)
  输出文件: 1 个 (标准PDF)
  
  文档结构:
  • 封面页
  • 目录 (自动生成)
  • 公司简介 (8页)
  • 技术方案 (15页)
  • 成功案例 (12页)
  • 报价清单 (5页)
  • 附件资料 (10页)
  
  总页数: 51 页
  文件大小: 8.5 MB
  处理时间: 2 分钟
    """)
    
    print("✅ 投标文件已准备完成!")


def main():
    """主函数"""
    print("\n" + "="*70)
    print("📄 文档处理智能体使用示例")
    print("="*70)
    
    print("\n本示例展示文档处理智能体的各种功能")
    print("包括格式转换、内容提取、智能摘要、文档对比等")
    print()
    
    try:
        example_1_format_conversion()
        example_2_document_extraction()
        example_3_document_summary()
        example_4_document_comparison()
        example_5_document_merge()
        example_6_template_filling()
        example_7_ocr_processing()
        example_8_complete_workflow()
        
        print("\n" + "="*70)
        print("✅ 所有示例运行完成!")
        print("="*70)
        
        print("\n💡 功能总结:")
        print("   1. 格式转换 - 支持多种文档格式互转")
        print("   2. 内容提取 - 从PDF/图片中提取信息")
        print("   3. 智能摘要 - AI生成多层次摘要")
        print("   4. 文档对比 - 精确识别版本差异")
        print("   5. 文档合并 - 自动整合多个文档")
        print("   6. 模板填充 - 批量生成标准文档")
        print("   7. OCR识别 - 图片文字提取")
        print("   8. 完整工作流 - 端到端文档处理")
        
        print("\n🎯 应用场景:")
        print("   • 合同文档管理")
        print("   • 项目投标准备")
        print("   • 报告自动生成")
        print("   • 档案数字化")
        print("   • 文档版本控制")
        print()
        
    except Exception as e:
        print(f"\n❌ 运行出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
