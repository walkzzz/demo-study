# 日常办公超级智能体 - 快速开始指南

## 系统要求

- Python 3.10+
- Ollama 服务
- 16GB+ 内存 (推荐 32GB)
- Windows 10/11, macOS 12+, 或 Ubuntu 20.04+

## 安装步骤

### 1. 安装 Ollama

访问 [Ollama官网](https://ollama.ai) 下载并安装。

启动 Ollama 并下载模型:

```bash
ollama pull llama3:8b
ollama pull qwen:7b
ollama pull nomic-embed-text
```

验证 Ollama 服务:
```bash
curl http://localhost:11434/api/tags
```

### 2. 克隆项目并安装依赖

```bash
# 进入项目目录
cd office-super-agent

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 3. 配置系统

复制示例配置文件:
```bash
cp config/config.yaml.example config/config.yaml
```

编辑 `config/config.yaml`，根据需要修改配置。

### 4. 启动系统

#### 命令行模式

```bash
python src/cli/main.py
```

#### API服务模式

```bash
python src/api/main.py
```

API文档访问: http://localhost:8000/docs

## 使用示例

### 命令行交互

```bash
👤 您: 整理我的下载文件夹，删除重复文件

🤖 处理中...
✅ 任务执行完成:
整理计划:
1. 扫描文件: 1000个文件
2. 按类型分类: 文档350个, 图片200个, 视频150个...
3. 检测到50组重复文件
是否确认执行? (y/n)
```

### API调用

```bash
curl -X POST http://localhost:8000/api/task \
  -H "Content-Type: application/json" \
  -d '{"user_input": "分析本月销售数据"}'
```

## Docker部署

### 使用 Docker Compose

```bash
# 构建并启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f app

# 停止服务
docker-compose down
```

### 服务访问

- API服务: http://localhost:8000
- Ollama: http://localhost:11434
- ChromaDB: http://localhost:8001

## 常见问题

### 1. Ollama连接失败

检查Ollama服务状态:
```bash
curl http://localhost:11434/api/tags
```

确保 `config/config.yaml` 中的 `ollama.base_url` 配置正确。

### 2. 模型下载慢

可以配置Ollama镜像源或手动下载模型文件。

### 3. 内存不足

- 使用量化模型 (如 `llama3:8b-q4_0`)
- 减少并发任务数量
- 增加系统虚拟内存

### 4. 向量数据库初始化失败

确保 `data/vectordb` 目录存在且有写入权限:
```bash
mkdir -p data/vectordb
chmod 755 data/vectordb
```

## 进阶配置

### 配置多个模型

编辑 `config/config.yaml`:

```yaml
model_strategy:
  task_understanding:
    model: "llama3:8b"
    temperature: 0.3
  
  email_reply:
    model: "mistral:7b"
    temperature: 0.7
```

### 自定义文件分类规则

编辑 `config/file_rules.json`:

```json
{
  "file_classification_rules": {
    "MyCategory": {
      "extensions": [".custom"],
      "description": "自定义文件类型"
    }
  }
}
```

### 启用邮件功能

在 `config/config.yaml` 中配置:

```yaml
email:
  protocol: "IMAP"
  imap_server: "imap.gmail.com"
  imap_port: 993
  smtp_server: "smtp.gmail.com"
  smtp_port: 587
```

设置环境变量:
```bash
export EMAIL_ACCOUNT="your@email.com"
export EMAIL_PASSWORD="your_app_password"
```

## 性能优化

### 1. 启用缓存

```yaml
cache:
  enable: true
  ttl: 3600
```

### 2. 使用量化模型

```bash
ollama pull llama3:8b-q4_0
```

### 3. 调整并发数

```yaml
performance:
  max_concurrent_tasks: 5
```

## 开发指南

### 添加新的智能体

1. 在 `src/agents/` 创建新的智能体类
2. 继承 `BaseAgent`
3. 实现 `execute()` 方法
4. 在 `config/agents.yaml` 添加配置
5. 在 `src/cli/main.py` 中注册

### 添加新的工具

1. 在 `src/tools/` 创建新的工具类
2. 实现工具方法
3. 提供 `get_tool_descriptions()` 方法
4. 在对应的智能体中集成

## 故障排除

### 启用调试日志

编辑 `config/config.yaml`:

```yaml
logging:
  level: "DEBUG"
```

### 查看日志

```bash
tail -f logs/app.log
```

### 清理缓存

```bash
rm -rf data/cache/*
rm -rf data/vectordb/*
```

## 更新日志

### v0.1.0 (2025-10-17)

- ✨ 初始版本发布
- 🤖 支持6个专业智能体
- 📁 完整的文件系统管理功能
- 🔧 基于Ollama的本地部署

## 贡献

欢迎提交Issue和Pull Request!

## 许可证

MIT License

## 联系方式

- 项目主页: https://github.com/yourusername/office-super-agent
- 问题反馈: https://github.com/yourusername/office-super-agent/issues
