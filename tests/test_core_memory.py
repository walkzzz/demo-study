"""MemoryManager单元测试"""

import pytest
import json
import os
from pathlib import Path
from datetime import datetime
from src.core.memory import MemoryManager


class TestMemoryManager:
    """MemoryManager测试类"""
    
    def test_init_creates_directories(self, temp_config_file, tmp_path):
        """测试初始化创建目录"""
        manager = MemoryManager(temp_config_file)
        
        assert manager.store_path.exists()
        assert manager.store_path.is_dir()
    
    def test_init_loads_config(self, temp_config_file):
        """测试初始化加载配置"""
        manager = MemoryManager(temp_config_file)
        
        assert manager.config is not None
        assert "memory" in manager.config
        assert manager.max_short_term == 50
    
    def test_add_message(self, temp_config_file):
        """测试添加消息到短期记忆"""
        manager = MemoryManager(temp_config_file)
        
        manager.add_message("user", "Hello")
        
        assert len(manager.short_term_memory) == 1
        assert manager.short_term_memory[0]["role"] == "user"
        assert manager.short_term_memory[0]["content"] == "Hello"
        assert "timestamp" in manager.short_term_memory[0]
    
    def test_add_message_with_metadata(self, temp_config_file):
        """测试添加带元数据的消息"""
        manager = MemoryManager(temp_config_file)
        metadata = {"source": "test", "priority": "high"}
        
        manager.add_message("assistant", "Response", metadata=metadata)
        
        assert manager.short_term_memory[0]["metadata"] == metadata
    
    def test_add_message_limit(self, temp_config_file):
        """测试短期记忆大小限制"""
        manager = MemoryManager(temp_config_file)
        manager.max_short_term = 5
        
        # 添加超过限制的消息
        for i in range(10):
            manager.add_message("user", f"Message {i}")
        
        assert len(manager.short_term_memory) == 5
        # 应该保留最新的5条
        assert manager.short_term_memory[0]["content"] == "Message 5"
        assert manager.short_term_memory[4]["content"] == "Message 9"
    
    def test_get_recent_messages(self, temp_config_file):
        """测试获取最近的消息"""
        manager = MemoryManager(temp_config_file)
        
        for i in range(10):
            manager.add_message("user", f"Message {i}")
        
        recent = manager.get_recent_messages(3)
        
        assert len(recent) == 3
        assert recent[0]["content"] == "Message 7"
        assert recent[2]["content"] == "Message 9"
    
    def test_get_conversation_history(self, temp_config_file):
        """测试获取对话历史"""
        manager = MemoryManager(temp_config_file)
        
        manager.add_message("system", "System msg")
        manager.add_message("user", "User msg")
        manager.add_message("assistant", "Assistant msg")
        
        history = manager.get_conversation_history()
        
        assert len(history) == 3
        assert history[0] == {"role": "system", "content": "System msg"}
        assert history[1] == {"role": "user", "content": "User msg"}
        assert history[2] == {"role": "assistant", "content": "Assistant msg"}
    
    def test_clear_short_term(self, temp_config_file):
        """测试清除短期记忆"""
        manager = MemoryManager(temp_config_file)
        
        manager.add_message("user", "Test")
        assert len(manager.short_term_memory) > 0
        
        manager.clear_short_term()
        
        assert len(manager.short_term_memory) == 0
    
    def test_save_knowledge(self, temp_config_file):
        """测试保存知识到长期记忆"""
        manager = MemoryManager(temp_config_file)
        
        manager.save_knowledge("user_preference", "dark_mode", category="settings")
        
        assert "settings" in manager.long_term_memory
        assert "user_preference" in manager.long_term_memory["settings"]
        assert manager.long_term_memory["settings"]["user_preference"]["value"] == "dark_mode"
    
    def test_get_knowledge(self, temp_config_file):
        """测试从长期记忆获取知识"""
        manager = MemoryManager(temp_config_file)
        
        manager.save_knowledge("test_key", "test_value", category="test")
        result = manager.get_knowledge("test_key", category="test")
        
        assert result == "test_value"
    
    def test_get_knowledge_not_found(self, temp_config_file):
        """测试获取不存在的知识"""
        manager = MemoryManager(temp_config_file)
        
        result = manager.get_knowledge("non_existent", category="test")
        
        assert result is None
    
    def test_search_knowledge(self, temp_config_file):
        """测试搜索长期记忆"""
        manager = MemoryManager(temp_config_file)
        
        manager.save_knowledge("file_path", "/home/user/docs", category="paths")
        manager.save_knowledge("download_path", "/home/user/downloads", category="paths")
        manager.save_knowledge("theme", "dark", category="settings")
        
        # 搜索包含"path"的知识
        results = manager.search_knowledge("path")
        
        assert len(results) >= 2
        assert any(r["key"] == "file_path" for r in results)
        assert any(r["key"] == "download_path" for r in results)
    
    def test_search_knowledge_in_category(self, temp_config_file):
        """测试在特定分类中搜索"""
        manager = MemoryManager(temp_config_file)
        
        manager.save_knowledge("key1", "value1", category="cat1")
        manager.save_knowledge("key2", "value2", category="cat2")
        
        results = manager.search_knowledge("key", category="cat1")
        
        assert len(results) == 1
        assert results[0]["category"] == "cat1"
    
    def test_delete_knowledge(self, temp_config_file):
        """测试删除知识"""
        manager = MemoryManager(temp_config_file)
        
        manager.save_knowledge("to_delete", "value", category="test")
        assert manager.get_knowledge("to_delete", category="test") == "value"
        
        manager.delete_knowledge("to_delete", category="test")
        
        assert manager.get_knowledge("to_delete", category="test") is None
    
    def test_long_term_memory_persistence(self, temp_config_file):
        """测试长期记忆持久化"""
        # 创建第一个实例并保存数据
        manager1 = MemoryManager(temp_config_file)
        manager1.save_knowledge("persistent_key", "persistent_value", category="test")
        
        # 创建第二个实例，应该加载之前的数据
        manager2 = MemoryManager(temp_config_file)
        result = manager2.get_knowledge("persistent_key", category="test")
        
        assert result == "persistent_value"
    
    def test_set_task_state(self, temp_config_file):
        """测试设置任务状态"""
        manager = MemoryManager(temp_config_file)
        
        task_id = "task_001"
        task_state = {"status": "running", "progress": 0.5}
        
        manager.set_task_state(task_id, task_state)
        
        assert task_id in manager.working_memory
        assert manager.working_memory[task_id]["state"] == task_state
    
    def test_get_task_state(self, temp_config_file):
        """测试获取任务状态"""
        manager = MemoryManager(temp_config_file)
        
        task_id = "task_002"
        task_state = {"status": "completed"}
        manager.set_task_state(task_id, task_state)
        
        result = manager.get_task_state(task_id)
        
        assert result == task_state
    
    def test_get_task_state_not_found(self, temp_config_file):
        """测试获取不存在的任务状态"""
        manager = MemoryManager(temp_config_file)
        
        result = manager.get_task_state("non_existent")
        
        assert result is None
    
    def test_clear_task_state(self, temp_config_file):
        """测试清除任务状态"""
        manager = MemoryManager(temp_config_file)
        
        manager.set_task_state("task1", {"status": "running"})
        manager.set_task_state("task2", {"status": "pending"})
        
        manager.clear_task_state("task1")
        
        assert "task1" not in manager.working_memory
        assert "task2" in manager.working_memory
    
    def test_get_memory_stats(self, temp_config_file):
        """测试获取记忆统计"""
        manager = MemoryManager(temp_config_file)
        
        manager.add_message("user", "Hello")
        manager.save_knowledge("key1", "value1", category="cat1")
        manager.save_knowledge("key2", "value2", category="cat2")
        manager.set_task_state("task1", {"status": "running"})
        
        stats = manager.get_memory_stats()
        
        assert stats["short_term_messages"] == 1
        assert stats["long_term_knowledge"] == 2
        assert stats["working_tasks"] == 1
        assert "cat1" in stats["categories"]
        assert "cat2" in stats["categories"]
    
    def test_export_memory(self, temp_config_file, tmp_path):
        """测试导出记忆"""
        manager = MemoryManager(temp_config_file)
        
        manager.add_message("user", "Test message")
        manager.save_knowledge("test_key", "test_value", category="test")
        
        export_file = tmp_path / "memory_export.json"
        manager.export_memory(str(export_file))
        
        assert export_file.exists()
        with open(export_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        assert "short_term" in data
        assert "long_term" in data
    
    def test_update_task_state(self, temp_config_file):
        """测试更新任务状态"""
        manager = MemoryManager(temp_config_file)
        
        task_id = "task_003"
        initial_state = {"status": "running", "progress": 0.3}
        manager.set_task_state(task_id, initial_state)
        
        # 更新状态
        manager.update_task_state(task_id, {"progress": 0.7})
        
        updated_state = manager.get_task_state(task_id)
        assert updated_state is not None
        assert updated_state["status"] == "running"
        assert updated_state["progress"] == 0.7
