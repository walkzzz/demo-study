# 示例集合

本目录包含日常办公超级智能体系统的各种使用示例，帮助您快速上手。

## 📁 示例列表

### 基础示例
- **[01_basic_usage.py](01_basic_usage.py)** - ✅ 基础使用入门 (已创建并测试)
- **[02_model_manager.py](02_model_manager.py)** - ✅ 模型管理器使用示例 (已创建)
- **[03_memory_system.py](03_memory_system.py)** - ✅ 记忆系统使用示例 (已创建)

### 智能体示例
- **[04_file_agent.py](04_file_agent.py)** - ✅ 文件管理智能体示例 (已创建)
- **[05_email_agent.py](05_email_agent.py)** - ✅ 邮件处理智能体示例 (已创建并测试)
- **[06_data_agent.py](06_data_agent.py)** - ✅ 数据分析智能体示例 (已创建)
- **[07_doc_agent.py](07_doc_agent.py)** - ✅ 文档处理智能体示例 (已创建)
- **[08_knowledge_agent.py](08_knowledge_agent.py)** - ✅ 知识问答智能体示例 (已创建)

### 高级示例
- **[09_multi_agent_workflow.py](09_multi_agent_workflow.py)** - ✅ 多智能体协作示例 (已创建)
- **[10_custom_tools.py](10_custom_tools.py)** - ✅ 自定义工具开发示例 (已创建并测试)

## 🚀 运行示例

### 前提条件
1. 确保已安装所有依赖: `pip install -r ../requirements.txt`
2. 启动 Ollama 服务
3. 配置文件已正确设置

### 运行方式

```bash
# 切换到项目根目录
cd d:\workspace\Qoder\study

# 运行基础示例
python examples/01_basic_usage.py

# 运行特定智能体示例
python examples/04_file_agent.py

# 运行多智能体协作示例
python examples/09_multi_agent_workflow.py
```

## 📝 示例说明

每个示例都是独立的，可以单独运行。示例中包含详细的注释，说明每个步骤的作用。

## ⚙️ 配置要求

大多数示例可以在不需要 Ollama 服务的情况下运行（仅演示功能）。
如需完整体验智能推理功能，请确保 Ollama 服务正在运行。

## 💡 提示

- 从基础示例开始，逐步了解系统功能
- 查看示例中的注释，理解每个功能的用法
- 尝试修改示例代码，探索更多可能性
- 遇到问题请查看主项目的 [QUICKSTART.md](../QUICKSTART.md)
