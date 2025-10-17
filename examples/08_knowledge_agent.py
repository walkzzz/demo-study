"""
示例 08: 知识问答智能体
演示如何使用 KnowledgeAgent 进行知识管理和智能问答
"""

import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 本示例不需要导入实际的VectorDB,仅作演示


def example_1_knowledge_indexing():
    """示例1: 知识索引建立"""
    print("\n" + "="*60)
    print("📚 示例1: 知识索引建立")
    print("="*60)
    
    # 模拟知识文档
    documents = [
        {
            "title": "Python基础教程",
            "content": "Python是一种高级编程语言,语法简洁,易于学习。支持面向对象、函数式等多种编程范式。",
            "category": "编程语言",
            "tags": ["Python", "编程", "教程"]
        },
        {
            "title": "机器学习入门",
            "content": "机器学习是人工智能的核心技术,通过算法让计算机从数据中学习规律。常见算法包括线性回归、决策树等。",
            "category": "人工智能",
            "tags": ["机器学习", "AI", "算法"]
        },
        {
            "title": "数据库设计原则",
            "content": "良好的数据库设计应遵循规范化原则,减少数据冗余。常用的关系型数据库包括MySQL、PostgreSQL等。",
            "category": "数据库",
            "tags": ["数据库", "设计", "SQL"]
        },
        {
            "title": "敏捷开发方法",
            "content": "敏捷开发强调快速迭代、持续交付。Scrum是最流行的敏捷框架,包括Sprint、每日站会等实践。",
            "category": "项目管理",
            "tags": ["敏捷", "Scrum", "开发"]
        }
    ]
    
    print("\n正在建立知识索引...")
    print(f"  文档总数: {len(documents)}")
    
    for i, doc in enumerate(documents, 1):
        print(f"\n  {i}. 索引文档: {doc['title']}")
        print(f"     分类: {doc['category']}")
        print(f"     标签: {', '.join(doc['tags'])}")
        print(f"     ✅ 已索引")
    
    print("\n✅ 知识库索引建立完成!")
    print(f"   总计 {len(documents)} 个文档")
    print(f"   覆盖 {len(set(d['category'] for d in documents))} 个分类")


def example_2_semantic_search():
    """示例2: 语义搜索"""
    print("\n" + "="*60)
    print("🔍 示例2: 语义搜索")
    print("="*60)
    
    # 用户查询
    queries = [
        "如何学习编程?",
        "什么是AI技术?",
        "如何管理软件项目?"
    ]
    
    # 模拟搜索结果
    search_results = {
        "如何学习编程?": [
            {"doc": "Python基础教程", "score": 0.92, "snippet": "Python语法简洁,易于学习..."},
            {"doc": "编程思维培养", "score": 0.78, "snippet": "培养逻辑思维是学习编程的关键..."},
        ],
        "什么是AI技术?": [
            {"doc": "机器学习入门", "score": 0.95, "snippet": "机器学习是人工智能的核心技术..."},
            {"doc": "深度学习概述", "score": 0.88, "snippet": "深度学习是AI领域的重要突破..."},
        ],
        "如何管理软件项目?": [
            {"doc": "敏捷开发方法", "score": 0.91, "snippet": "敏捷开发强调快速迭代、持续交付..."},
            {"doc": "项目管理实践", "score": 0.84, "snippet": "有效的项目管理需要明确目标..."},
        ]
    }
    
    for query in queries:
        print(f"\n查询: '{query}'")
        print("="*55)
        
        results = search_results.get(query, [])
        for i, result in enumerate(results, 1):
            print(f"\n  {i}. {result['doc']} (相似度: {result['score']:.0%})")
            print(f"     {result['snippet']}")


def example_3_qa_system():
    """示例3: 智能问答"""
    print("\n" + "="*60)
    print("💬 示例3: 智能问答系统")
    print("="*60)
    
    # 问答对话
    qa_examples = [
        {
            "question": "Python有哪些优点?",
            "context": "Python是一种高级编程语言,语法简洁,易于学习。支持多种编程范式,拥有丰富的第三方库。",
            "answer": """Python的主要优点包括:

1. **语法简洁**: 代码易读易写,学习曲线平缓
2. **功能强大**: 支持面向对象、函数式等多种编程范式
3. **生态丰富**: 拥有大量优秀的第三方库和框架
4. **应用广泛**: 可用于Web开发、数据分析、AI等多个领域
5. **社区活跃**: 有庞大的开发者社区提供支持

这些特点使Python成为最受欢迎的编程语言之一。"""
        },
        {
            "question": "什么是Scrum?",
            "context": "Scrum是最流行的敏捷开发框架,强调团队协作和迭代开发。包括Sprint、每日站会、回顾会议等核心实践。",
            "answer": """Scrum是一个敏捷项目管理框架,主要特点包括:

**核心概念**:
- Sprint: 固定时长的迭代周期(通常2-4周)
- Product Backlog: 产品待办事项列表
- Sprint Backlog: 当前Sprint的任务清单

**关键角色**:
- Product Owner: 产品负责人
- Scrum Master: 流程协调者
- Development Team: 开发团队

**核心会议**:
- Sprint Planning: 迭代规划会
- Daily Standup: 每日站会
- Sprint Review: 迭代评审
- Sprint Retrospective: 回顾会议

Scrum通过这些实践确保项目的透明度、检视和适应性。"""
        }
    ]
    
    for i, qa in enumerate(qa_examples, 1):
        print(f"\n问题 {i}: {qa['question']}")
        print("-"*55)
        print(f"\n参考上下文:\n{qa['context']}")
        print(f"\n{'='*55}")
        print(f"AI回答:\n{qa['answer']}")
        print("="*55)


def example_4_knowledge_graph():
    """示例4: 知识图谱"""
    print("\n" + "="*60)
    print("🕸️  示例4: 知识图谱展示")
    print("="*60)
    
    # 模拟知识图谱关系
    knowledge_graph = {
        "Python": {
            "类型": "编程语言",
            "相关技术": ["Django", "Flask", "NumPy", "Pandas"],
            "应用领域": ["Web开发", "数据分析", "人工智能"],
            "学习资源": ["官方文档", "在线课程", "开源项目"]
        },
        "机器学习": {
            "类型": "技术领域",
            "子领域": ["监督学习", "无监督学习", "强化学习"],
            "常用算法": ["线性回归", "决策树", "神经网络"],
            "工具框架": ["TensorFlow", "PyTorch", "Scikit-learn"]
        }
    }
    
    print("\n知识图谱结构:")
    for entity, relations in knowledge_graph.items():
        print(f"\n📌 {entity}")
        for relation_type, items in relations.items():
            print(f"   {relation_type}:")
            if isinstance(items, list):
                for item in items:
                    print(f"     • {item}")
            else:
                print(f"     • {items}")


def example_5_context_retrieval():
    """示例5: 上下文检索增强"""
    print("\n" + "="*60)
    print("🎯 示例5: 上下文检索增强 (RAG)")
    print("="*60)
    
    print("\nRAG工作流程演示:")
    
    user_query = "如何在Python中进行数据分析?"
    
    print(f"\n用户问题: '{user_query}'")
    
    # 步骤1: 检索相关文档
    print("\n步骤1: 从知识库检索相关文档")
    retrieved_docs = [
        {"title": "Python数据分析入门", "relevance": 0.95},
        {"title": "Pandas使用指南", "relevance": 0.89},
        {"title": "数据可视化教程", "relevance": 0.82},
    ]
    
    for doc in retrieved_docs:
        print(f"  ✓ {doc['title']} (相关度: {doc['relevance']:.0%})")
    
    # 步骤2: 构建上下文
    print("\n步骤2: 整合检索到的上下文")
    context = """
    Python提供了强大的数据分析工具:
    - Pandas: 数据处理和分析库
    - NumPy: 数值计算库
    - Matplotlib/Seaborn: 数据可视化
    - Jupyter: 交互式开发环境
    """
    print(f"  上下文长度: {len(context)} 字符")
    
    # 步骤3: 生成回答
    print("\n步骤3: 基于上下文生成回答")
    answer = """在Python中进行数据分析,推荐使用以下工具组合:

1. **Pandas**: 用于数据读取、清洗和处理
   ```python
   import pandas as pd
   df = pd.read_csv('data.csv')
   ```

2. **NumPy**: 用于数值计算和数组操作
   ```python
   import numpy as np
   arr = np.array([1, 2, 3])
   ```

3. **Matplotlib/Seaborn**: 用于数据可视化
   ```python
   import matplotlib.pyplot as plt
   df.plot()
   ```

4. **Jupyter Notebook**: 推荐的交互式开发环境

这些工具构成了Python数据分析的核心生态系统。"""
    
    print(f"  ✅ 回答已生成")
    print(f"\n最终回答:\n{answer}")


def example_6_knowledge_update():
    """示例6: 知识库更新"""
    print("\n" + "="*60)
    print("🔄 示例6: 知识库动态更新")
    print("="*60)
    
    print("\n知识库管理操作:")
    
    operations = [
        ("添加", "新增文档: 'LangChain开发指南'", "成功"),
        ("更新", "更新文档: 'Python基础教程' (版本3.12)", "成功"),
        ("删除", "删除过时文档: '旧版API文档'", "成功"),
        ("索引重建", "重建向量索引以优化检索", "成功"),
    ]
    
    for op_type, description, status in operations:
        print(f"\n  [{op_type}] {description}")
        print(f"  状态: {status} ✓")
    
    # 知识库统计
    print("\n\n知识库统计信息:")
    stats = {
        "文档总数": 156,
        "分类数量": 12,
        "索引大小": "45 MB",
        "最后更新": "2025-10-17 14:30",
        "平均查询响应时间": "0.3 秒"
    }
    
    for key, value in stats.items():
        print(f"  {key}: {value}")


def example_7_multi_source_search():
    """示例7: 多源知识融合"""
    print("\n" + "="*60)
    print("🌐 示例7: 多源知识融合")
    print("="*60)
    
    query = "人工智能的应用前景"
    
    print(f"\n查询: '{query}'")
    print("\n从多个知识源检索:")
    
    # 不同来源的搜索结果
    sources = [
        {
            "name": "内部知识库",
            "results": 15,
            "top_doc": "AI技术白皮书",
            "confidence": 0.92
        },
        {
            "name": "外部文档",
            "results": 8,
            "top_doc": "行业研究报告",
            "confidence": 0.85
        },
        {
            "name": "网络资源",
            "results": 23,
            "top_doc": "AI发展趋势分析",
            "confidence": 0.78
        }
    ]
    
    for source in sources:
        print(f"\n  📚 {source['name']}")
        print(f"     找到: {source['results']} 个相关文档")
        print(f"     最佳匹配: {source['top_doc']}")
        print(f"     置信度: {source['confidence']:.0%}")
    
    # 融合答案
    print("\n\n融合多源信息生成综合答案:")
    print("="*55)
    integrated_answer = """基于多个知识源的分析,人工智能的应用前景广阔:

**当前应用**:
- 智能客服和对话系统 (内部知识库)
- 医疗影像诊断辅助 (行业报告)
- 自动驾驶技术 (网络资源)

**未来趋势**:
1. AI将更加普及到日常生活各个领域
2. 多模态AI(文本+图像+语音)将成为主流
3. AI伦理和监管将得到更多重视

**机遇与挑战**:
- 机遇: 提高效率、降低成本、创造新价值
- 挑战: 数据隐私、算法偏见、就业影响

综合判断,AI技术将持续快速发展并深刻改变社会。"""
    
    print(integrated_answer)


def example_8_complete_workflow():
    """示例8: 完整知识问答工作流"""
    print("\n" + "="*60)
    print("🔄 示例8: 完整知识问答工作流")
    print("="*60)
    
    print("\n场景: 企业内部知识问答系统")
    print("\n系统架构:")
    
    components = [
        ("知识采集", ["文档上传", "网页爬取", "API集成"]),
        ("数据处理", ["文本清洗", "分词标注", "实体识别"]),
        ("向量化", ["文本编码", "向量存储", "索引构建"]),
        ("检索服务", ["语义搜索", "关键词匹配", "混合检索"]),
        ("问答生成", ["上下文组装", "LLM推理", "答案优化"]),
        ("用户界面", ["Web端", "移动端", "API接口"])
    ]
    
    for component, features in components:
        print(f"\n  📦 {component}")
        for feature in features:
            print(f"     • {feature}")
    
    print("\n\n典型使用流程:")
    workflow = [
        "1. 用户提交问题",
        "2. 问题理解和改写",
        "3. 向量化查询",
        "4. 检索相关文档 (Top 5)",
        "5. 重排序优化",
        "6. 上下文构建",
        "7. LLM生成答案",
        "8. 答案验证和优化",
        "9. 返回结果给用户"
    ]
    
    for step in workflow:
        print(f"  {step}")
    
    print("\n\n性能指标:")
    metrics = {
        "平均响应时间": "1.2 秒",
        "准确率": "87%",
        "用户满意度": "4.3/5.0",
        "日查询量": "2,500+ 次"
    }
    
    for metric, value in metrics.items():
        print(f"  {metric}: {value}")


def main():
    """主函数"""
    print("\n" + "="*70)
    print("🧠 知识问答智能体使用示例")
    print("="*70)
    
    print("\n本示例展示知识问答智能体的各种功能")
    print("包括知识索引、语义搜索、智能问答、RAG等")
    print()
    
    try:
        example_1_knowledge_indexing()
        example_2_semantic_search()
        example_3_qa_system()
        example_4_knowledge_graph()
        example_5_context_retrieval()
        example_6_knowledge_update()
        example_7_multi_source_search()
        example_8_complete_workflow()
        
        print("\n" + "="*70)
        print("✅ 所有示例运行完成!")
        print("="*70)
        
        print("\n💡 功能总结:")
        print("   1. 知识索引 - 建立向量知识库")
        print("   2. 语义搜索 - 理解查询意图")
        print("   3. 智能问答 - 基于上下文回答")
        print("   4. 知识图谱 - 关系网络展示")
        print("   5. RAG增强 - 检索增强生成")
        print("   6. 动态更新 - 知识库维护")
        print("   7. 多源融合 - 整合多个来源")
        print("   8. 完整系统 - 端到端解决方案")
        
        print("\n🎯 应用场景:")
        print("   • 企业知识库问答")
        print("   • 客户服务支持")
        print("   • 技术文档助手")
        print("   • 教育学习平台")
        print("   • 研究辅助工具")
        print()
        
    except Exception as e:
        print(f"\n❌ 运行出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
