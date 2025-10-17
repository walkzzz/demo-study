# 状态管理器使用指南

## 📋 概述

[`StateManager`](../src/orchestrator/state_manager.py) 是日常办公超级智能体系统中的核心组件，负责管理任务执行过程中的状态流转和数据维护。它基于 LangGraph 的状态管理理念，为多智能体协作提供统一的状态存储和更新机制。

## 🎯 核心功能

### 1. 任务状态管理
- 创建任务状态
- 更新任务进度
- 查询任务信息
- 删除完成的任务

### 2. 状态流转
支持以下任务状态流转：

```
PENDING (待处理)
    ↓
RUNNING (执行中)
    ↓
SUCCESS (成功) / FAILED (失败) / RETRY (重试)
```

### 3. 状态持久化
- 内存存储当前活跃任务
- 维护任务执行历史
- 追踪当前执行步骤

## 📊 任务状态枚举

### TaskStatus

| 状态 | 值 | 说明 |
|------|-----|------|
| PENDING | "pending" | 任务已创建，等待执行 |
| RUNNING | "running" | 任务正在执行中 |
| SUCCESS | "success" | 任务执行成功 |
| FAILED | "failed" | 任务执行失败 |
| RETRY | "retry" | 任务需要重试 |

## 🔧 API 参考

### 类: StateManager

#### 初始化

```python
from src.orchestrator.state_manager import StateManager

# 创建状态管理器实例
state_manager = StateManager()
```

#### 方法

##### 1. create_state()

创建新的任务状态。

**签名**:
```python
def create_state(
    self,
    task_id: str,
    initial_data: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

**参数**:
- `task_id` (str): 唯一的任务标识符
- `initial_data` (Optional[Dict]): 初始任务数据，默认为空字典

**返回**:
- `Dict[str, Any]`: 创建的状态对象

**状态对象结构**:
```python
{
    "task_id": str,           # 任务ID
    "status": str,            # 当前状态 (TaskStatus枚举值)
    "data": Dict[str, Any],   # 任务数据
    "history": List,          # 执行历史记录
    "current_step": Optional[str]  # 当前执行步骤
}
```

**示例**:
```python
# 创建简单任务
state = state_manager.create_state(
    task_id="task_001"
)

# 创建带初始数据的任务
state = state_manager.create_state(
    task_id="email_processing_001",
    initial_data={
        "user_input": "处理今天的邮件",
        "agent_type": "email",
        "priority": "high"
    }
)
```

##### 2. update_state()

更新已存在任务的状态。

**签名**:
```python
def update_state(
    self,
    task_id: str,
    updates: Dict[str, Any]
) -> None
```

**参数**:
- `task_id` (str): 任务标识符
- `updates` (Dict): 要更新的字段和值

**示例**:
```python
# 更新任务状态
state_manager.update_state(
    task_id="task_001",
    updates={"status": TaskStatus.RUNNING.value}
)

# 更新多个字段
state_manager.update_state(
    task_id="task_001",
    updates={
        "status": TaskStatus.SUCCESS.value,
        "current_step": "邮件分类完成",
        "data": {
            "processed_count": 42,
            "important_count": 5
        }
    }
)

# 追加历史记录
current_state = state_manager.get_state("task_001")
current_state["history"].append({
    "timestamp": "2025-10-17T10:30:00",
    "action": "邮件分类",
    "result": "成功"
})
state_manager.update_state(
    task_id="task_001",
    updates={"history": current_state["history"]}
)
```

##### 3. get_state()

获取任务的当前状态。

**签名**:
```python
def get_state(
    self,
    task_id: str
) -> Optional[Dict[str, Any]]
```

**参数**:
- `task_id` (str): 任务标识符

**返回**:
- `Optional[Dict]`: 状态对象，如果任务不存在则返回 None

**示例**:
```python
# 查询任务状态
state = state_manager.get_state("task_001")

if state:
    print(f"任务状态: {state['status']}")
    print(f"当前步骤: {state['current_step']}")
    print(f"任务数据: {state['data']}")
else:
    print("任务不存在")
```

##### 4. delete_state()

删除已完成的任务状态。

**签名**:
```python
def delete_state(
    self,
    task_id: str
) -> None
```

**参数**:
- `task_id` (str): 任务标识符

**示例**:
```python
# 删除任务
state_manager.delete_state("task_001")
```

## 💡 使用场景

### 场景 1: 单个智能体任务

```python
from src.orchestrator.state_manager import StateManager, TaskStatus

# 初始化
state_manager = StateManager()

# 1. 创建任务
task_id = "email_urgent_001"
state = state_manager.create_state(
    task_id=task_id,
    initial_data={
        "user_input": "处理紧急邮件",
        "agent": "EmailAgent"
    }
)

# 2. 开始执行
state_manager.update_state(
    task_id=task_id,
    updates={
        "status": TaskStatus.RUNNING.value,
        "current_step": "读取邮件列表"
    }
)

# 3. 更新进度
state_manager.update_state(
    task_id=task_id,
    updates={
        "current_step": "分类邮件",
        "data": {"emails_found": 15}
    }
)

# 4. 完成任务
state_manager.update_state(
    task_id=task_id,
    updates={
        "status": TaskStatus.SUCCESS.value,
        "current_step": "任务完成",
        "data": {
            "emails_found": 15,
            "urgent_count": 3,
            "processed": True
        }
    }
)

# 5. 查询最终状态
final_state = state_manager.get_state(task_id)
print(f"处理结果: {final_state['data']}")

# 6. 清理
state_manager.delete_state(task_id)
```

### 场景 2: 多智能体协作

```python
from src.orchestrator.state_manager import StateManager, TaskStatus
import uuid

state_manager = StateManager()

# 主任务
main_task_id = f"workflow_{uuid.uuid4().hex[:8]}"
main_state = state_manager.create_state(
    task_id=main_task_id,
    initial_data={
        "user_input": "分析本月销售数据并生成报告",
        "workflow": "data_analysis_report",
        "sub_tasks": []
    }
)

# 子任务1: 数据加载
sub_task1_id = f"data_load_{uuid.uuid4().hex[:8]}"
state_manager.create_state(
    task_id=sub_task1_id,
    initial_data={
        "parent_task": main_task_id,
        "agent": "DataAgent",
        "action": "load_data"
    }
)

# 子任务2: 数据分析
sub_task2_id = f"data_analyze_{uuid.uuid4().hex[:8]}"
state_manager.create_state(
    task_id=sub_task2_id,
    initial_data={
        "parent_task": main_task_id,
        "agent": "DataAgent",
        "action": "analyze"
    }
)

# 子任务3: 报告生成
sub_task3_id = f"report_gen_{uuid.uuid4().hex[:8]}"
state_manager.create_state(
    task_id=sub_task3_id,
    initial_data={
        "parent_task": main_task_id,
        "agent": "DocAgent",
        "action": "generate_report"
    }
)

# 更新主任务的子任务列表
main_state["data"]["sub_tasks"] = [
    sub_task1_id,
    sub_task2_id,
    sub_task3_id
]
state_manager.update_state(
    task_id=main_task_id,
    updates={"data": main_state["data"]}
)

# 执行子任务并更新状态
for sub_task_id in [sub_task1_id, sub_task2_id, sub_task3_id]:
    state_manager.update_state(
        task_id=sub_task_id,
        updates={"status": TaskStatus.RUNNING.value}
    )
    
    # ... 执行任务逻辑 ...
    
    state_manager.update_state(
        task_id=sub_task_id,
        updates={"status": TaskStatus.SUCCESS.value}
    )

# 所有子任务完成后，更新主任务
state_manager.update_state(
    task_id=main_task_id,
    updates={"status": TaskStatus.SUCCESS.value}
)
```

### 场景 3: 错误处理和重试

```python
from src.orchestrator.state_manager import StateManager, TaskStatus

state_manager = StateManager()

task_id = "file_process_001"
state_manager.create_state(
    task_id=task_id,
    initial_data={"file_path": "/path/to/file.pdf"}
)

try:
    # 开始处理
    state_manager.update_state(
        task_id=task_id,
        updates={"status": TaskStatus.RUNNING.value}
    )
    
    # 模拟处理逻辑
    # ... 发生错误 ...
    raise Exception("文件格式不支持")
    
except Exception as e:
    # 记录错误
    state = state_manager.get_state(task_id)
    state["data"]["error"] = str(e)
    state["data"]["retry_count"] = state["data"].get("retry_count", 0) + 1
    
    # 判断是否需要重试
    if state["data"]["retry_count"] < 3:
        state_manager.update_state(
            task_id=task_id,
            updates={
                "status": TaskStatus.RETRY.value,
                "data": state["data"]
            }
        )
        print(f"任务失败，将进行第 {state['data']['retry_count']} 次重试")
    else:
        state_manager.update_state(
            task_id=task_id,
            updates={
                "status": TaskStatus.FAILED.value,
                "data": state["data"]
            }
        )
        print("任务失败，已达到最大重试次数")
```

### 场景 4: 执行历史追踪

```python
from src.orchestrator.state_manager import StateManager, TaskStatus
from datetime import datetime

state_manager = StateManager()

task_id = "email_batch_001"
state = state_manager.create_state(
    task_id=task_id,
    initial_data={"batch_size": 100}
)

# 辅助函数：添加历史记录
def add_history(task_id: str, action: str, result: str, details: dict = None):
    state = state_manager.get_state(task_id)
    history_entry = {
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "result": result
    }
    if details:
        history_entry["details"] = details
    
    state["history"].append(history_entry)
    state_manager.update_state(
        task_id=task_id,
        updates={"history": state["history"]}
    )

# 执行任务并记录历史
state_manager.update_state(
    task_id=task_id,
    updates={"status": TaskStatus.RUNNING.value}
)

add_history(task_id, "开始处理", "成功", {"batch_size": 100})

add_history(task_id, "邮件读取", "成功", {"count": 100})

add_history(task_id, "垃圾邮件过滤", "成功", {"filtered": 15})

add_history(task_id, "分类邮件", "成功", {
    "work": 50,
    "personal": 20,
    "important": 15
})

state_manager.update_state(
    task_id=task_id,
    updates={"status": TaskStatus.SUCCESS.value}
)

# 查看完整历史
final_state = state_manager.get_state(task_id)
print("任务执行历史:")
for i, entry in enumerate(final_state["history"], 1):
    print(f"{i}. [{entry['timestamp']}] {entry['action']}: {entry['result']}")
    if "details" in entry:
        print(f"   详情: {entry['details']}")
```

## 🔗 与其他组件的集成

### 与 SuperAgent 集成

[`SuperAgent`](../src/orchestrator/super_agent.py) 使用 StateManager 管理任务生命周期：

```python
from src.orchestrator.super_agent import SuperAgent

# SuperAgent 内部使用 StateManager
super_agent = SuperAgent()

# 处理任务时自动创建和管理状态
result = super_agent.process_task("整理下载文件夹")
```

### 与 TaskPlanner 集成

[`TaskPlanner`](../src/orchestrator/task_planner.py) 创建任务计划时使用 StateManager：

```python
from src.orchestrator.task_planner import TaskPlanner
from src.orchestrator.state_manager import StateManager

planner = TaskPlanner()
state_manager = StateManager()

# 创建任务
task_id = "complex_task_001"
state = state_manager.create_state(task_id)

# 规划任务
plan = planner.plan_task("分析销售数据并生成月报")

# 更新状态为计划
state_manager.update_state(
    task_id=task_id,
    updates={"data": {"plan": plan}}
)
```

### 与智能体集成

专业智能体使用 StateManager 报告进度：

```python
from src.agents.email_agent import EmailAgent
from src.orchestrator.state_manager import StateManager, TaskStatus

email_agent = EmailAgent()
state_manager = StateManager()

task_id = "email_task_001"
state_manager.create_state(task_id)

# 智能体执行前
state_manager.update_state(
    task_id=task_id,
    updates={
        "status": TaskStatus.RUNNING.value,
        "current_step": "EmailAgent 处理中"
    }
)

# 执行
result = email_agent.process("读取今天的邮件")

# 智能体执行后
state_manager.update_state(
    task_id=task_id,
    updates={
        "status": TaskStatus.SUCCESS.value,
        "data": {"result": result}
    }
)
```

## 📈 最佳实践

### 1. 任务ID命名规范

使用有意义的任务ID：

```python
# ✅ 推荐
task_id = f"{agent_type}_{action}_{timestamp}"
# 例如: "email_urgent_20251017_103000"

# ❌ 不推荐
task_id = "task1"
```

### 2. 及时清理已完成任务

```python
# 定期清理
def cleanup_completed_tasks(state_manager: StateManager):
    for task_id, state in list(state_manager.states.items()):
        if state["status"] in [TaskStatus.SUCCESS.value, TaskStatus.FAILED.value]:
            # 可选：保存到持久化存储
            # save_to_database(state)
            
            # 删除内存中的状态
            state_manager.delete_state(task_id)
```

### 3. 状态数据结构化

保持状态数据的一致性：

```python
# ✅ 结构化的数据
initial_data = {
    "input": {...},
    "config": {...},
    "metrics": {
        "start_time": None,
        "end_time": None,
        "duration": None
    },
    "result": None
}

# ❌ 混乱的数据
initial_data = {
    "some_field": "value",
    "random_data": 123
}
```

### 4. 错误信息记录

完整记录错误信息：

```python
try:
    # 任务执行
    pass
except Exception as e:
    state_manager.update_state(
        task_id=task_id,
        updates={
            "status": TaskStatus.FAILED.value,
            "data": {
                "error_type": type(e).__name__,
                "error_message": str(e),
                "error_traceback": traceback.format_exc()
            }
        }
    )
```

### 5. 状态查询优化

避免频繁查询：

```python
# ✅ 缓存状态对象
state = state_manager.get_state(task_id)
if state:
    status = state["status"]
    data = state["data"]
    # ... 使用状态 ...

# ❌ 重复查询
status = state_manager.get_state(task_id)["status"]
data = state_manager.get_state(task_id)["data"]  # 重复查询
```

## 🐛 常见问题

### Q1: 状态数据过大怎么办？

**A**: 只在状态中保存必要的元数据，大数据存储在外部：

```python
# 不要直接保存大数据
state_manager.update_state(
    task_id=task_id,
    updates={
        "data": {
            "result_path": "/path/to/large/result.pkl",  # 保存路径
            "result_summary": {...}  # 保存摘要
        }
    }
)
```

### Q2: 如何实现状态持久化？

**A**: 扩展 StateManager 添加持久化功能：

```python
import json
from pathlib import Path

class PersistentStateManager(StateManager):
    def __init__(self, storage_path: str = "./data/states"):
        super().__init__()
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
    
    def create_state(self, task_id: str, initial_data=None):
        state = super().create_state(task_id, initial_data)
        self._save_to_disk(task_id)
        return state
    
    def update_state(self, task_id: str, updates: dict):
        super().update_state(task_id, updates)
        self._save_to_disk(task_id)
    
    def _save_to_disk(self, task_id: str):
        state = self.states.get(task_id)
        if state:
            file_path = self.storage_path / f"{task_id}.json"
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(state, f, ensure_ascii=False, indent=2)
```

### Q3: 多线程环境下如何保证状态一致性？

**A**: 添加线程锁：

```python
import threading

class ThreadSafeStateManager(StateManager):
    def __init__(self):
        super().__init__()
        self._lock = threading.Lock()
    
    def update_state(self, task_id: str, updates: dict):
        with self._lock:
            super().update_state(task_id, updates)
    
    def get_state(self, task_id: str):
        with self._lock:
            return super().get_state(task_id)
```

## 📚 相关文档

- [系统架构说明](../ARCHITECTURE.md)
- [SuperAgent 使用指南](./SUPER_AGENT_GUIDE.md) *(待创建)*
- [TaskPlanner 使用指南](./TASK_PLANNER_GUIDE.md) *(待创建)*
- [智能体开发指南](./AGENT_DEVELOPMENT_GUIDE.md) *(待创建)*

## 🔄 更新日志

### v0.2.0 (2025-10-17)
- ✅ 初始版本
- ✅ 基础状态管理功能
- ✅ 5种任务状态支持
- ✅ 历史记录追踪
- ✅ 完整文档和示例

---

**提示**: 如有任何问题或建议，请查阅 [项目文档](../README.md) 或提交 Issue。
