"""BaseAgent单元测试"""

import pytest
from unittest.mock import Mock, MagicMock
from src.agents.base_agent import BaseAgent


class TestAgent(BaseAgent):
    """测试用的具体Agent实现"""
    
    def execute(self, task):
        """简单的execute实现"""
        return {
            "status": "success",
            "result": f"Executed: {task.get('description', 'unknown')}"
        }


class TestBaseAgent:
    """BaseAgent测试类"""
    
    def test_init(self, mock_model_manager, mock_prompt_engine, mock_memory_manager):
        """测试初始化"""
        config = {
            "model_name": "test_model",
            "temperature": 0.5,
            "max_iterations": 5,
            "memory_enabled": True,
            "reflection_enabled": False
        }
        
        agent = TestAgent(
            name="TestAgent",
            model_manager=mock_model_manager,
            prompt_engine=mock_prompt_engine,
            memory_manager=mock_memory_manager,
            tools=Mock(),
            config=config
        )
        
        assert agent.name == "TestAgent"
        assert agent.model_name == "test_model"
        assert agent.temperature == 0.5
        assert agent.max_iterations == 5
        assert agent.memory_enabled is True
        assert agent.reflection_enabled is False
    
    def test_init_default_config(self, mock_model_manager, mock_prompt_engine, mock_memory_manager):
        """测试使用默认配置初始化"""
        agent = TestAgent(
            name="TestAgent",
            model_manager=mock_model_manager,
            prompt_engine=mock_prompt_engine,
            memory_manager=mock_memory_manager,
            tools=Mock()
        )
        
        assert agent.model_name == "llama3:8b"
        assert agent.temperature == 0.7
        assert agent.max_iterations == 10
        assert agent.memory_enabled is True
        assert agent.reflection_enabled is True
    
    def test_execute_task(self, mock_model_manager, mock_prompt_engine, mock_memory_manager):
        """测试执行任务"""
        agent = TestAgent(
            name="TestAgent",
            model_manager=mock_model_manager,
            prompt_engine=mock_prompt_engine,
            memory_manager=mock_memory_manager,
            tools=Mock()
        )
        
        task = {"description": "Test task"}
        result = agent.execute(task)
        
        assert result["status"] == "success"
        assert "Executed" in result["result"]
    
    def test_plan(self, mock_model_manager, mock_prompt_engine, mock_memory_manager):
        """测试任务规划"""
        mock_model_manager.invoke.return_value = "1. Step one\n2. Step two\n3. Step three"
        
        agent = TestAgent(
            name="TestAgent",
            model_manager=mock_model_manager,
            prompt_engine=mock_prompt_engine,
            memory_manager=mock_memory_manager,
            tools=Mock()
        )
        
        task = {"description": "Complex task"}
        steps = agent.plan(task)
        
        assert len(steps) == 3
        assert all("description" in step for step in steps)
        assert all(step["status"] == "pending" for step in steps)
        mock_model_manager.invoke.assert_called_once()
    
    def test_select_tool(self, mock_model_manager, mock_prompt_engine, mock_memory_manager):
        """测试工具选择"""
        mock_prompt_engine.render_tool_selection.return_value = "Tool selection prompt"
        mock_model_manager.invoke.return_value = "Selected tool: file_reader"
        
        agent = TestAgent(
            name="TestAgent",
            model_manager=mock_model_manager,
            prompt_engine=mock_prompt_engine,
            memory_manager=mock_memory_manager,
            tools=Mock()
        )
        
        available_tools = [
            {"name": "file_reader", "description": "Read files"},
            {"name": "file_writer", "description": "Write files"}
        ]
        
        result = agent.select_tool("Read a file", available_tools)
        
        assert "tool_name" in result
        mock_prompt_engine.render_tool_selection.assert_called_once()
        mock_model_manager.invoke.assert_called()
    
    def test_reflect_enabled(self, mock_model_manager, mock_prompt_engine, mock_memory_manager):
        """测试启用反思功能"""
        mock_prompt_engine.render_reflection.return_value = "Reflection prompt"
        mock_model_manager.invoke.return_value = "Good quality"
        
        config = {"reflection_enabled": True}
        agent = TestAgent(
            name="TestAgent",
            model_manager=mock_model_manager,
            prompt_engine=mock_prompt_engine,
            memory_manager=mock_memory_manager,
            tools=Mock(),
            config=config
        )
        
        result = agent.reflect("task", ["step1", "step2"], "result")
        
        assert "quality_score" in result
        assert "meets_goal" in result
        assert "should_retry" in result
        mock_prompt_engine.render_reflection.assert_called_once()
    
    def test_reflect_disabled(self, mock_model_manager, mock_prompt_engine, mock_memory_manager):
        """测试禁用反思功能"""
        config = {"reflection_enabled": False}
        agent = TestAgent(
            name="TestAgent",
            model_manager=mock_model_manager,
            prompt_engine=mock_prompt_engine,
            memory_manager=mock_memory_manager,
            tools=Mock(),
            config=config
        )
        
        result = agent.reflect("task", ["step1"], "result")
        
        assert result == {"should_retry": False}
        mock_prompt_engine.render_reflection.assert_not_called()
    
    def test_save_memory_enabled(self, mock_model_manager, mock_prompt_engine, mock_memory_manager):
        """测试保存记忆（启用）"""
        config = {"memory_enabled": True}
        agent = TestAgent(
            name="TestAgent",
            model_manager=mock_model_manager,
            prompt_engine=mock_prompt_engine,
            memory_manager=mock_memory_manager,
            tools=Mock(),
            config=config
        )
        
        agent.save_memory("test_key", "test_value")
        
        mock_memory_manager.save_knowledge.assert_called_once_with(
            "test_key", "test_value", category="testagent"
        )
    
    def test_save_memory_disabled(self, mock_model_manager, mock_prompt_engine, mock_memory_manager):
        """测试保存记忆（禁用）"""
        config = {"memory_enabled": False}
        agent = TestAgent(
            name="TestAgent",
            model_manager=mock_model_manager,
            prompt_engine=mock_prompt_engine,
            memory_manager=mock_memory_manager,
            tools=Mock(),
            config=config
        )
        
        agent.save_memory("test_key", "test_value")
        
        mock_memory_manager.save_knowledge.assert_not_called()
    
    def test_get_memory_enabled(self, mock_model_manager, mock_prompt_engine, mock_memory_manager):
        """测试获取记忆（启用）"""
        mock_memory_manager.get_knowledge.return_value = "retrieved_value"
        config = {"memory_enabled": True}
        agent = TestAgent(
            name="TestAgent",
            model_manager=mock_model_manager,
            prompt_engine=mock_prompt_engine,
            memory_manager=mock_memory_manager,
            tools=Mock(),
            config=config
        )
        
        result = agent.get_memory("test_key")
        
        assert result == "retrieved_value"
        mock_memory_manager.get_knowledge.assert_called_once()
    
    def test_get_memory_disabled(self, mock_model_manager, mock_prompt_engine, mock_memory_manager):
        """测试获取记忆（禁用）"""
        config = {"memory_enabled": False}
        agent = TestAgent(
            name="TestAgent",
            model_manager=mock_model_manager,
            prompt_engine=mock_prompt_engine,
            memory_manager=mock_memory_manager,
            tools=Mock(),
            config=config
        )
        
        result = agent.get_memory("test_key")
        
        assert result is None
        mock_memory_manager.get_knowledge.assert_not_called()
