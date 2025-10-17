# 模型配置说明

## 本地 Ollama 模型列表

根据 2025-10-17 更新，本地已安装以下模型：

| 模型名称 | 版本 | 大小 | 最后更新 | 用途 |
|---------|------|------|---------|------|
| llama3:8b | 365c0bd3c000 | 4.7 GB | 已更新 | 通用对话、邮件回复、文件分类 |
| qwen3:8b | 500a1f067a9f | 5.2 GB | 已更新 | 文档理解、数据分析、知识问答 |
| minicpm-v:latest | c92bfad01205 | 5.5 GB | 已更新 | 视觉理解（多模态） |
| nomic-embed-text:latest | 0a109f422b47 | 274 MB | 已更新 | 文本向量化（嵌入模型） |

## 模型分配策略

### 1. llama3:8b
**特点**: Meta开发，对话能力强，英文和多语言支持好

**适用场景**:
- ✅ 邮件回复生成 (email_reply)
- ✅ 文件智能分类 (file_classification)
- ✅ 日程规划 (schedule_planning)
- ✅ 通用对话任务

**配置位置**:
- `config/config.yaml`: 默认模型
- `config/agents.yaml`: EmailAgent, ScheduleAgent, DataAgent, FileAgent

### 2. qwen3:8b
**特点**: 阿里开发，中文理解能力强，推理能力优秀

**适用场景**:
- ✅ 任务理解 (task_understanding)
- ✅ 文档摘要提取 (document_summary)
- ✅ 数据分析 (data_analysis)
- ✅ 知识问答 (knowledge_qa)

**配置位置**:
- `config/agents.yaml`: DocAgent, KnowledgeAgent

### 3. minicpm-v:latest
**特点**: 多模态模型，支持图像理解

**适用场景**:
- ✅ 视觉理解任务 (vision_understanding)
- ✅ 图像内容分析
- ✅ OCR文档识别

**配置位置**:
- `config/config.yaml`: vision_understanding 策略

### 4. nomic-embed-text:latest
**特点**: 专用嵌入模型，高质量文本向量化

**适用场景**:
- ✅ 文档向量化
- ✅ 语义搜索
- ✅ 知识库检索

**配置位置**:
- `config/config.yaml`: embedding_model

## 配置文件结构

### config/config.yaml
主配置文件，包含：
- Ollama 服务地址和默认模型
- 模型策略（按任务类型分配模型）
- 向量数据库配置
- 系统性能参数

### config/agents.yaml
智能体配置文件，包含：
- 6个专业智能体的模型配置
- 每个智能体的温度参数
- 工具列表和能力配置

## 模型调用优先级

1. **显式指定模型名**: 代码中直接指定 `model_name` 参数
2. **任务类型策略**: 根据 `task_type` 从 `model_strategy` 中查找
3. **智能体默认模型**: 使用智能体配置中的 `model_name`
4. **系统默认模型**: 使用 `ollama.default_model` (llama3:8b)

## 性能建议

### Temperature 参数说明
- **0.1-0.3**: 低创造性，适合数据分析、精确任务
- **0.5-0.7**: 中等创造性，适合文档摘要、邮件回复
- **0.7-0.9**: 高创造性，适合内容生成、头脑风暴

### 模型选择建议
- **中文任务优先**: qwen3:8b
- **英文任务优先**: llama3:8b
- **需要视觉能力**: minicpm-v:latest
- **向量化/检索**: nomic-embed-text:latest

## 更新记录

### 2025-10-17
- ✅ 创建 config/config.yaml 主配置文件
- ✅ 更新 config/agents.yaml 模型配置
- ✅ 将 mistral:7b 替换为 llama3:8b
- ✅ 将 qwen:7b 替换为 qwen3:8b
- ✅ 配置多模态模型 minicpm-v
- ✅ 配置嵌入模型 nomic-embed-text

## 未来扩展

如需添加新模型，执行：
```bash
# 查看可用模型
ollama list

# 拉取新模型
ollama pull <model-name>

# 更新配置文件
# 编辑 config/config.yaml 或 config/agents.yaml
```

## 故障排查

### 模型未找到
```bash
# 检查模型是否已安装
ollama list

# 重新拉取模型
ollama pull llama3:8b
ollama pull qwen3:8b
```

### Ollama 服务未启动
```bash
# 检查服务状态
curl http://localhost:11434/api/tags

# 如果失败，启动 Ollama 服务
```

### 配置文件错误
- 检查 YAML 格式是否正确
- 确认模型名称与 ollama list 输出一致
- 查看日志 `logs/app.log` 获取详细错误信息
