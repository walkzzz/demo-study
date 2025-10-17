"""pytest配置和共享fixture"""

import pytest
import os
import sys
import yaml
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, MagicMock

# 添加src到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


@pytest.fixture
def test_config():
    """测试配置fixture"""
    return {
        "ollama": {
            "base_url": "http://localhost:11434",
            "default_model": "llama3:8b",
            "timeout": 300,
            "embedding_model": "nomic-embed-text:latest"
        },
        "model_strategy": {
            "task_understanding": {
                "model": "qwen3:8b",
                "temperature": 0.3,
                "top_p": 0.9,
                "max_tokens": 2000
            },
            "email_reply": {
                "model": "llama3:8b",
                "temperature": 0.7,
                "top_p": 0.9,
                "max_tokens": 1000
            }
        },
        "memory": {
            "store_path": "./test_data/memory",
            "max_short_term_messages": 50
        },
        "vectordb": {
            "type": "chroma",
            "persist_directory": "./test_data/vectordb",
            "collection_name": "test_knowledge_base"
        }
    }


@pytest.fixture
def temp_config_file(test_config, tmp_path):
    """创建临时配置文件"""
    config_file = tmp_path / "config.yaml"
    with open(config_file, 'w', encoding='utf-8') as f:
        yaml.dump(test_config, f)
    return str(config_file)


@pytest.fixture
def temp_data_dir(tmp_path):
    """创建临时数据目录"""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    return data_dir


@pytest.fixture
def mock_model_manager():
    """Mock ModelManager"""
    mock_manager = Mock()
    mock_manager.invoke = Mock(return_value="Mock response")
    mock_manager.ainvoke = Mock(return_value="Mock async response")
    mock_manager.get_model = Mock()
    return mock_manager


@pytest.fixture
def mock_memory_manager():
    """Mock MemoryManager"""
    mock_manager = Mock()
    mock_manager.short_term_memory = []
    mock_manager.long_term_memory = {}
    mock_manager.working_memory = {}
    mock_manager.add_message = Mock()
    mock_manager.get_recent_messages = Mock(return_value=[])
    mock_manager.save_knowledge = Mock()
    mock_manager.get_knowledge = Mock(return_value=None)
    return mock_manager


@pytest.fixture
def mock_prompt_engine():
    """Mock PromptEngine"""
    mock_engine = Mock()
    mock_engine.render_task_understanding = Mock(return_value="Mock prompt")
    mock_engine.render_tool_selection = Mock(return_value="Mock tool selection prompt")
    mock_engine.render_reflection = Mock(return_value="Mock reflection prompt")
    return mock_engine


@pytest.fixture
def sample_messages():
    """示例消息列表"""
    return [
        {"role": "system", "content": "你是一个智能助手"},
        {"role": "user", "content": "帮我整理文件"},
        {"role": "assistant", "content": "好的，我会帮你整理文件"}
    ]


@pytest.fixture
def sample_task():
    """示例任务"""
    return {
        "id": "task_001",
        "type": "file_organization",
        "description": "整理下载文件夹中的文件",
        "priority": "high",
        "metadata": {
            "path": "./downloads",
            "category": "auto"
        }
    }


@pytest.fixture(autouse=True)
def cleanup_test_data():
    """测试后清理"""
    yield
    # 清理测试数据
    test_dirs = ["./test_data", "./temp_test"]
    for dir_path in test_dirs:
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
