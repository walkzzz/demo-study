"""系统集成测试

测试多个模块之间的集成
"""

import pytest
import os
import yaml
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from src.core.model_manager import ModelManager
from src.core.memory import MemoryManager
from src.core.prompt_engine import PromptEngine


class TestSystemIntegration:
    """系统集成测试"""
    
    @pytest.fixture
    def integrated_config(self, tmp_path):
        """创建集成测试配置"""
        config = {
            "ollama": {
                "base_url": "http://localhost:11434",
                "default_model": "llama3:8b",
                "timeout": 300
            },
            "model_strategy": {
                "test_task": {
                    "model": "test_model",
                    "temperature": 0.5
                }
            },
            "memory": {
                "store_path": str(tmp_path / "memory"),
                "max_short_term_messages": 10
            },
            "prompts": {
                "base_path": "config/prompts"
            }
        }
        
        config_file = tmp_path / "config.yaml"
        with open(config_file, 'w', encoding='utf-8') as f:
            yaml.dump(config, f)
        
        return str(config_file)
    
    def test_model_memory_integration(self, integrated_config):
        """测试模型管理器和记忆管理器的集成"""
        model_manager = ModelManager(integrated_config)
        memory_manager = MemoryManager(integrated_config)
        
        # 添加对话到记忆
        memory_manager.add_message("user", "Hello")
        memory_manager.add_message("assistant", "Hi there!")
        
        # 获取对话历史
        history = memory_manager.get_conversation_history()
        
        assert len(history) == 2
        assert history[0]["role"] == "user"
        assert history[1]["role"] == "assistant"
        
        # 验证模型管理器配置
        assert model_manager.ollama_config["default_model"] == "llama3:8b"
    
    @patch('src.core.model_manager.ChatOllama')
    def test_agent_workflow_integration(self, mock_ollama, integrated_config):
        """测试Agent工作流集成"""
        # 设置Mock
        mock_model = Mock()
        mock_response = Mock()
        mock_response.content = "Task completed successfully"
        mock_model.invoke.return_value = mock_response
        mock_ollama.return_value = mock_model
        
        model_manager = ModelManager(integrated_config)
        memory_manager = MemoryManager(integrated_config)
        
        # 模拟Agent工作流
        # 1. 接收任务
        task = {"description": "Organize files"}
        memory_manager.add_message("user", task["description"])
        
        # 2. 调用模型处理
        messages = memory_manager.get_conversation_history()
        response = model_manager.invoke(messages)
        
        # 3. 保存结果到记忆
        memory_manager.add_message("assistant", response)
        memory_manager.save_knowledge("last_task", task["description"], category="tasks")
        
        # 验证
        assert response == "Task completed successfully"
        assert len(memory_manager.short_term_memory) == 2
        assert memory_manager.get_knowledge("last_task", category="tasks") == task["description"]
    
    def test_memory_persistence_integration(self, integrated_config, tmp_path):
        """测试记忆持久化集成"""
        # 创建第一个实例并保存数据
        memory1 = MemoryManager(integrated_config)
        memory1.save_knowledge("api_key", "secret_key_123", category="credentials")
        memory1.save_knowledge("user_pref", "dark_mode", category="settings")
        
        # 创建第二个实例，测试数据加载
        memory2 = MemoryManager(integrated_config)
        
        assert memory2.get_knowledge("api_key", category="credentials") == "secret_key_123"
        assert memory2.get_knowledge("user_pref", category="settings") == "dark_mode"
    
    def test_multi_agent_memory_sharing(self, integrated_config):
        """测试多Agent共享记忆"""
        memory_manager = MemoryManager(integrated_config)
        
        # Agent1 保存知识
        memory_manager.save_knowledge("file_path", "/home/user/docs", category="file_agent")
        
        # Agent2 读取知识
        retrieved_path = memory_manager.get_knowledge("file_path", category="file_agent")
        
        assert retrieved_path == "/home/user/docs"
        
        # 搜索跨category的知识
        memory_manager.save_knowledge("email_template", "Hello {name}", category="email_agent")
        results = memory_manager.search_knowledge("template")
        
        assert len(results) > 0
        assert any(r["category"] == "email_agent" for r in results)
    
    @patch('src.core.model_manager.ChatOllama')
    def test_error_recovery_integration(self, mock_ollama, integrated_config):
        """测试错误恢复集成"""
        mock_model = Mock()
        # 第一次调用失败
        mock_model.invoke.side_effect = [
            Exception("Network error"),
            Mock(content="Retry successful")
        ]
        mock_ollama.return_value = mock_model
        
        model_manager = ModelManager(integrated_config)
        memory_manager = MemoryManager(integrated_config)
        
        messages = [{"role": "user", "content": "Test"}]
        
        # 第一次调用失败
        with pytest.raises(Exception):
            model_manager.invoke(messages)
        
        # 记录失败
        memory_manager.save_knowledge("last_error", "Network error", category="errors")
        
        # 重试成功
        result = model_manager.invoke(messages)
        assert result == "Retry successful"
    
    def test_task_state_tracking_integration(self, integrated_config):
        """测试任务状态跟踪集成"""
        memory_manager = MemoryManager(integrated_config)
        
        # 创建任务
        task_id = "task_001"
        initial_state = {
            "status": "pending",
            "description": "Process documents",
            "progress": 0.0
        }
        
        # 保存初始状态
        memory_manager.set_task_state(task_id, initial_state)
        
        # 更新进度
        memory_manager.update_task_state(task_id, {"status": "running", "progress": 0.3})
        memory_manager.update_task_state(task_id, {"progress": 0.6})
        memory_manager.update_task_state(task_id, {"status": "completed", "progress": 1.0})
        
        # 验证最终状态
        final_state = memory_manager.get_task_state(task_id)
        assert final_state is not None
        assert final_state["status"] == "completed"
        assert final_state["progress"] == 1.0
        
        # 归档任务
        memory_manager.archive_task(task_id)
        assert task_id not in memory_manager.working_memory
        assert memory_manager.get_knowledge(task_id, category="archived_tasks") is not None
    
    @patch('src.core.model_manager.ChatOllama')
    def test_conversation_context_integration(self, mock_ollama, integrated_config):
        """测试对话上下文集成"""
        mock_model = Mock()
        mock_model.invoke.return_value = Mock(content="Context aware response")
        mock_ollama.return_value = mock_model
        
        model_manager = ModelManager(integrated_config)
        memory_manager = MemoryManager(integrated_config)
        
        # 构建多轮对话
        memory_manager.add_message("user", "My name is Alice")
        memory_manager.add_message("assistant", "Nice to meet you, Alice!")
        memory_manager.add_message("user", "What's my name?")
        
        # 获取完整上下文
        context = memory_manager.get_conversation_history()
        assert len(context) == 3
        
        # 使用上下文调用模型
        response = model_manager.invoke(context)
        assert response == "Context aware response"
    
    def test_memory_stats_integration(self, integrated_config):
        """测试记忆统计集成"""
        memory_manager = MemoryManager(integrated_config)
        
        # 添加不同类型的记忆
        memory_manager.add_message("user", "Message 1")
        memory_manager.add_message("user", "Message 2")
        
        memory_manager.save_knowledge("k1", "v1", category="cat1")
        memory_manager.save_knowledge("k2", "v2", category="cat1")
        memory_manager.save_knowledge("k3", "v3", category="cat2")
        
        memory_manager.set_task_state("task1", {"status": "running"})
        memory_manager.set_task_state("task2", {"status": "pending"})
        
        # 获取统计
        stats = memory_manager.get_memory_stats()
        
        assert stats["short_term_messages"] == 2
        assert stats["long_term_knowledge"] == 3
        assert stats["working_tasks"] == 2
        assert "cat1" in stats["categories"]
        assert "cat2" in stats["categories"]
    
    def test_export_import_integration(self, integrated_config, tmp_path):
        """测试导出导入集成"""
        memory1 = MemoryManager(integrated_config)
        
        # 添加数据
        memory1.add_message("user", "Test message")
        memory1.save_knowledge("key1", "value1", category="test")
        memory1.set_task_state("task1", {"status": "completed"})
        
        # 导出
        export_file = tmp_path / "export.json"
        memory1.export_memory(str(export_file))
        
        assert export_file.exists()
        
        # 导入到新实例
        memory2 = MemoryManager(integrated_config)
        # 注意：需要实现import_memory方法
        # memory2.import_memory(str(export_file))
