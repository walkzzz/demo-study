"""
示例 02: 模型管理器详细使用
演示如何使用 ModelManager 进行模型调用和管理
"""

import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.core import ModelManager


def example_1_basic_invocation():
    """示例1: 基础模型调用"""
    print("\n" + "="*60)
    print("📞 示例1: 基础模型调用")
    print("="*60)
    
    model_manager = ModelManager()
    
    # 准备消息
    messages = [
        {"role": "system", "content": "你是一个专业的办公助手"},
        {"role": "user", "content": "请用一句话介绍你自己"}
    ]
    
    print("\n发送消息到模型...")
    print(f"System: {messages[0]['content']}")
    print(f"User: {messages[1]['content']}\n")
    
    try:
        response = model_manager.invoke(messages)
        print(f"✅ 模型响应:\n{response}\n")
    except Exception as e:
        print(f"❌ 调用失败: {e}")
        print("💡 请确保 Ollama 服务正在运行")


def example_2_task_specific_model():
    """示例2: 使用任务特定的模型"""
    print("\n" + "="*60)
    print("🎯 示例2: 使用任务特定的模型")
    print("="*60)
    
    model_manager = ModelManager()
    
    # 不同任务使用不同的模型策略
    tasks = [
        {
            "type": "task_understanding",
            "messages": [{"role": "user", "content": "帮我整理桌面文件"}],
            "description": "任务理解"
        },
        {
            "type": "document_summary",
            "messages": [{"role": "user", "content": "总结这段文字：人工智能正在改变世界..."}],
            "description": "文档摘要"
        }
    ]
    
    for task in tasks:
        print(f"\n📋 {task['description']}任务:")
        print(f"   任务类型: {task['type']}")
        
        try:
            response = model_manager.invoke(
                messages=task['messages'],
                task_type=task['type']
            )
            print(f"   ✅ 响应: {response[:100]}...")
        except Exception as e:
            print(f"   ❌ 失败: {e}")


def example_3_custom_parameters():
    """示例3: 自定义模型参数"""
    print("\n" + "="*60)
    print("⚙️  示例3: 自定义模型参数")
    print("="*60)
    
    model_manager = ModelManager()
    
    messages = [
        {"role": "user", "content": "给我讲一个创意故事"}
    ]
    
    # 测试不同的温度参数
    temperatures = [0.1, 0.7, 1.2]
    
    for temp in temperatures:
        print(f"\n🌡️  温度参数: {temp}")
        print("   (温度越高，输出越有创意和随机性)")
        
        try:
            response = model_manager.invoke(
                messages=messages,
                temperature=temp
            )
            print(f"   响应: {response[:80]}...")
        except Exception as e:
            print(f"   ❌ 失败: {e}")


def example_4_conversation_context():
    """示例4: 多轮对话上下文"""
    print("\n" + "="*60)
    print("💬 示例4: 多轮对话上下文")
    print("="*60)
    
    model_manager = ModelManager()
    
    # 模拟多轮对话
    conversation = [
        {"role": "system", "content": "你是一个有帮助的助手"},
        {"role": "user", "content": "我想学习Python"},
        {"role": "assistant", "content": "太好了！Python是一门很棒的编程语言。你想从哪里开始学习？"},
        {"role": "user", "content": "从基础语法开始"}
    ]
    
    print("\n对话历史:")
    for msg in conversation:
        role_name = {"system": "系统", "user": "用户", "assistant": "助手"}[msg["role"]]
        print(f"  {role_name}: {msg['content']}")
    
    print("\n正在生成响应...")
    
    try:
        response = model_manager.invoke(conversation)
        print(f"\n✅ 助手响应:\n{response}")
    except Exception as e:
        print(f"❌ 失败: {e}")


def example_5_model_comparison():
    """示例5: 不同模型对比"""
    print("\n" + "="*60)
    print("🔬 示例5: 不同模型对比")
    print("="*60)
    
    model_manager = ModelManager()
    
    # 同一个问题让不同模型回答
    question = "什么是人工智能？请用一句话回答。"
    models = ["llama3:8b", "qwen3:8b"]
    
    print(f"\n问题: {question}\n")
    
    for model_name in models:
        print(f"📌 模型: {model_name}")
        
        try:
            response = model_manager.invoke(
                messages=[{"role": "user", "content": question}],
                model_name=model_name,
                temperature=0.3  # 使用较低温度保证一致性
            )
            print(f"   响应: {response}")
        except Exception as e:
            print(f"   ❌ 该模型不可用: {e}")
        
        print()


def example_6_cache_management():
    """示例6: 模型缓存管理"""
    print("\n" + "="*60)
    print("💾 示例6: 模型缓存管理")
    print("="*60)
    
    model_manager = ModelManager()
    
    print("\n1️⃣ 创建模型实例 (第一次，会创建新实例):")
    model1 = model_manager.get_model(model_name="llama3:8b", temperature=0.7)
    print(f"   ✅ 创建成功: {type(model1).__name__}")
    
    print("\n2️⃣ 再次获取相同配置的模型 (从缓存获取):")
    model2 = model_manager.get_model(model_name="llama3:8b", temperature=0.7)
    print(f"   ✅ 获取成功: {type(model2).__name__}")
    print(f"   是否为同一实例: {model1 is model2}")
    
    print("\n3️⃣ 获取不同配置的模型 (创建新实例):")
    model3 = model_manager.get_model(model_name="llama3:8b", temperature=0.9)
    print(f"   ✅ 创建成功: {type(model3).__name__}")
    print(f"   是否为同一实例: {model1 is model3}")
    
    print("\n4️⃣ 清除缓存:")
    model_manager.clear_cache()
    print("   ✅ 缓存已清除")


def main():
    """主函数"""
    print("\n" + "="*70)
    print("🤖 模型管理器详细使用示例")
    print("="*70)
    
    print("\n⚠️  注意: 以下示例需要 Ollama 服务运行才能完整执行")
    print("如果 Ollama 未运行，部分示例会显示错误提示\n")
    
    try:
        # 运行示例 (某些需要Ollama)
        example_1_basic_invocation()
        example_2_task_specific_model()
        example_3_custom_parameters()
        example_4_conversation_context()
        example_5_model_comparison()
        example_6_cache_management()
        
        print("\n" + "="*70)
        print("✅ 所有示例运行完成!")
        print("="*70)
        
        print("\n💡 要点总结:")
        print("   1. ModelManager 支持多种任务类型的模型策略")
        print("   2. 可以自定义温度、top_p 等参数")
        print("   3. 支持多轮对话上下文")
        print("   4. 自动缓存模型实例提高性能")
        print("   5. 可以切换不同模型进行对比")
        print()
        
    except Exception as e:
        print(f"\n❌ 运行出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
