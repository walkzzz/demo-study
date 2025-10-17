# 日常办公超级智能体系统

## 🎉 项目状态: 已完成并验证通过!

基于 LangChain 和 LangGraph 框架构建的日常办公超级智能体系统，使用本地 Ollama 模型作为核心推理引擎。系统通过多智能体协作模式，自动化处理日常办公场景中的复杂任务。

**项目文档**:
- 📚 [VERIFICATION_REPORT.md](VERIFICATION_REPORT.md) - 验证报告
- 📚 [TEST_SUMMARY.md](TEST_SUMMARY.md) - 测试总结
- 📚 [TYPE_CHECK_REPORT.md](TYPE_CHECK_REPORT.md) - 类型检查报告
- 📚 [examples/](examples/) - **10个实用示例** (新增!)

## ✨ 核心特性

- **隐私保护**: 所有数据和模型推理均在本地执行
- **智能协作**: 通过 LangGraph 实现多智能体协作决策
- **可扩展性**: 基于插件化架构，支持快速添加新功能
- **自主决策**: 智能体具备任务分解、工具选择和执行反思能力
- **Web 界面**: 现代化的前端交互页面 ⭐ **新增**

## 支持的办公场景

1. **邮件智能处理** - 自动分类、回复建议、批量处理
2. **文档智能处理** - 格式转换、摘要提取、内容对比
3. **日程智能管理** - 会议安排、冲突检测、时间规划
4. **数据智能分析** - 数据处理、可视化、报表生成
5. **知识问答** - 基于本地知识库的智能问答
6. **文件系统管理** - 智能整理、重复检测、空间优化

## 技术栈

- **核心框架**: LangChain, LangGraph
- **语言模型**: Ollama (Llama3, Mistral, Qwen等)
- **开发语言**: Python 3.10+
- **向量数据库**: ChromaDB
- **任务调度**: APScheduler

## 项目结构

```
office-super-agent/
├── config/                 # 配置文件
│   ├── config.yaml        # 主配置文件
│   ├── agents.yaml        # 智能体配置
│   └── file_rules.json    # 文件分类规则
├── src/
│   ├── core/              # 核心模块
│   │   ├── model_manager.py      # 模型管理器
│   │   ├── prompt_engine.py      # 提示词引擎
│   │   └── memory.py              # 记忆系统
│   ├── agents/            # 专业智能体
│   │   ├── base_agent.py         # 基础智能体类
│   │   ├── email_agent.py        # 邮件智能体
│   │   ├── doc_agent.py          # 文档智能体
│   │   ├── schedule_agent.py     # 日程智能体
│   │   ├── data_agent.py         # 数据分析智能体
│   │   ├── knowledge_agent.py    # 知识问答智能体
│   │   └── file_agent.py         # 文件系统管理智能体
│   ├── tools/             # 工具集
│   │   ├── email_tools.py        # 邮件工具
│   │   ├── file_tools.py         # 文件处理工具
│   │   ├── calendar_tools.py     # 日历工具
│   │   ├── data_tools.py         # 数据分析工具
│   │   ├── web_tools.py          # 网络搜索工具
│   │   └── filesystem_tools.py   # 文件系统工具
│   ├── orchestrator/      # 编排层
│   │   ├── super_agent.py        # 超级智能体协调器
│   │   ├── task_planner.py       # 任务规划器
│   │   └── state_manager.py      # 状态管理器
│   ├── api/               # API接口
│   │   └── routes.py             # FastAPI路由
│   └── cli/               # 命令行界面
│       └── main.py               # CLI入口
├── data/                  # 数据目录
│   ├── vectordb/          # 向量数据库
│   ├── memory/            # 记忆存储
│   └── backups/           # 备份目录
├── tests/                 # 测试文件 (完整测试套件)
├── examples/              # 示例集合 (10个实用示例) ⭐
├── requirements.txt       # Python依赖
├── docker-compose.yml     # Docker编排
├── check_types.py         # 类型检查脚本 ⭐
└── README.md              # 项目说明
```

## 快速开始

### 环境要求

- Python 3.10+
- Ollama 服务已安装并运行
- 16GB+ 内存 (推荐 32GB)

### 安装步骤

1. 安装依赖
```bash
pip install -r requirements.txt
```

2. 配置环境变量
```bash
cp config/config.yaml.example config/config.yaml
# 编辑 config.yaml 设置 Ollama 地址等参数
```

3. 启动 Ollama 服务并下载模型
```bash
ollama pull llama3:8b
ollama pull qwen:7b
```

4. 启动应用

**Web 界面模式** (推荐 ⭐):
```bash
# Windows PowerShell
.\start_web.ps1

# 或直接运行
python src/api/main.py
```
然后打开浏览器访问: **http://localhost:8000**

**命令行模式**:
```bash
python src/cli/main.py
```

**API服务模式**:
```bash
python src/api/main.py
# API文档: http://localhost:8000/docs
```

## 学习示例

### 📚 快速上手

项目提供了 **10个完整示例**，帮助您快速上手：

```bash
# 运行基础示例
python examples/01_basic_usage.py

# 运行邮件智能体示例
python examples/05_email_agent.py

# 运行数据分析示例
python examples/06_data_agent.py
```

**完整示例列表**: 查看 [examples/README.md](examples/README.md)

### 💻 命令行交互

```bash
> 帮我处理今天的邮件，重要邮件优先回复
> 对比这两份合同的差异
> 整理我的下载文件夹，删除重复文件
> 分析本月销售数据，生成可视化报告
```

## 配置说明

详细配置请参考 `config/config.yaml.example`

## 开发文档

详细的系统设计文档请参考项目文档目录。

### 📚 文档列表

> 📖 **文档导航**: 查看 [docs/README.md](docs/README.md) 获取完整的文档索引和学习路径

#### 架构与设计
- [ARCHITECTURE.md](ARCHITECTURE.md) - 系统架构说明
- [docs/STATE_MANAGER_GUIDE.md](docs/STATE_MANAGER_GUIDE.md) - 状态管理器使用指南 ⭐ **新增**

#### 快速上手
- [QUICKSTART.md](QUICKSTART.md) - 快速开始指南
- [WEB_QUICKSTART.md](WEB_QUICKSTART.md) - Web 界面快速开始 ⭐ **新增**
- [examples/](examples/) - 完整示例集合
  - [examples/README.md](examples/README.md) - 示例导航
  - [examples/TEST_REPORT.md](examples/TEST_REPORT.md) - 示例测试报告

#### 质量报告
- [TEST_SUMMARY.md](TEST_SUMMARY.md) - 测试总结报告
- [TYPE_CHECK_REPORT.md](TYPE_CHECK_REPORT.md) - 类型检查报告

### 🧪 质量保证

- ✅ **52个Python文件** - 全部通过类型检查
- ✅ **17个测试用例** - 100%通过率
- ✅ **10个实用示例** - 已测试验证
- ✅ **代码质量** - 无语法错误，无类型警告

## 安全与隐私

- ✅ 所有数据本地处理，不上传云端
- ✅ 敏感信息加密存储
- ✅ 文件操作前自动备份
- ✅ 重要操作需用户确认

## 许可证

MIT License

## 贡献指南

欢迎提交 Issue 和 Pull Request！
