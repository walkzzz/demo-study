"""ModelManager单元测试"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.core.model_manager import ModelManager


class TestModelManager:
    """ModelManager测试类"""
    
    def test_init_with_config(self, temp_config_file):
        """测试使用配置文件初始化"""
        manager = ModelManager(temp_config_file)
        
        assert manager.config is not None
        assert "ollama" in manager.config
        assert manager.ollama_config["base_url"] == "http://localhost:11434"
        assert manager.ollama_config["default_model"] == "llama3:8b"
    
    def test_init_with_invalid_config(self):
        """测试使用无效配置文件初始化"""
        manager = ModelManager("non_existent_config.yaml")
        
        # 应该返回空配置但不抛出异常
        assert manager.config == {}
        assert manager.ollama_config == {}
    
    def test_load_config_success(self, temp_config_file):
        """测试成功加载配置"""
        manager = ModelManager(temp_config_file)
        config = manager._load_config(temp_config_file)
        
        assert config is not None
        assert "ollama" in config
        assert "model_strategy" in config
    
    def test_load_config_failure(self):
        """测试加载配置失败"""
        manager = ModelManager()
        config = manager._load_config("invalid_path.yaml")
        
        assert config == {}
    
    @patch('src.core.model_manager.ChatOllama')
    def test_get_model_with_model_name(self, mock_ollama, temp_config_file):
        """测试使用指定模型名称获取模型"""
        manager = ModelManager(temp_config_file)
        mock_instance = Mock()
        mock_ollama.return_value = mock_instance
        
        model = manager.get_model(model_name="test_model")
        
        assert model is not None
        mock_ollama.assert_called_once()
        call_kwargs = mock_ollama.call_args[1]
        assert call_kwargs["model"] == "test_model"
    
    @patch('src.core.model_manager.ChatOllama')
    def test_get_model_with_task_type(self, mock_ollama, temp_config_file):
        """测试使用任务类型获取模型"""
        manager = ModelManager(temp_config_file)
        mock_instance = Mock()
        mock_ollama.return_value = mock_instance
        
        model = manager.get_model(task_type="task_understanding")
        
        assert model is not None
        call_kwargs = mock_ollama.call_args[1]
        assert call_kwargs["model"] == "qwen3:8b"
        assert call_kwargs["temperature"] == 0.3
    
    @patch('src.core.model_manager.ChatOllama')
    def test_get_model_default(self, mock_ollama, temp_config_file):
        """测试获取默认模型"""
        manager = ModelManager(temp_config_file)
        mock_instance = Mock()
        mock_ollama.return_value = mock_instance
        
        model = manager.get_model()
        
        assert model is not None
        call_kwargs = mock_ollama.call_args[1]
        assert call_kwargs["model"] == "llama3:8b"
    
    @patch('src.core.model_manager.ChatOllama')
    def test_get_model_caching(self, mock_ollama, temp_config_file):
        """测试模型缓存机制"""
        manager = ModelManager(temp_config_file)
        mock_instance = Mock()
        mock_ollama.return_value = mock_instance
        
        # 第一次调用
        model1 = manager.get_model(model_name="test_model", temperature=0.5)
        # 第二次调用相同配置
        model2 = manager.get_model(model_name="test_model", temperature=0.5)
        
        # 应该只创建一次模型实例
        assert mock_ollama.call_count == 1
        assert model1 is model2
    
    @patch('src.core.model_manager.ChatOllama')
    def test_get_model_no_caching_different_params(self, mock_ollama, temp_config_file):
        """测试不同参数不使用缓存"""
        manager = ModelManager(temp_config_file)
        mock_ollama.return_value = Mock()
        
        # 不同温度参数
        model1 = manager.get_model(model_name="test_model", temperature=0.5)
        model2 = manager.get_model(model_name="test_model", temperature=0.7)
        
        # 应该创建两次
        assert mock_ollama.call_count == 2
    
    @patch('src.core.model_manager.ChatOllama')
    def test_invoke_success(self, mock_ollama, temp_config_file, sample_messages):
        """测试成功调用模型"""
        manager = ModelManager(temp_config_file)
        mock_model = Mock()
        mock_response = Mock()
        mock_response.content = "Test response"
        mock_model.invoke.return_value = mock_response
        mock_ollama.return_value = mock_model
        
        result = manager.invoke(sample_messages)
        
        assert result == "Test response"
        mock_model.invoke.assert_called_once()
    
    @patch('src.core.model_manager.ChatOllama')
    def test_invoke_with_task_type(self, mock_ollama, temp_config_file):
        """测试使用任务类型调用"""
        manager = ModelManager(temp_config_file)
        mock_model = Mock()
        mock_response = Mock()
        mock_response.content = "Email response"
        mock_model.invoke.return_value = mock_response
        mock_ollama.return_value = mock_model
        
        messages = [{"role": "user", "content": "Write an email"}]
        result = manager.invoke(messages, task_type="email_reply")
        
        assert result == "Email response"
        # 验证使用了正确的模型配置
        call_kwargs = mock_ollama.call_args[1]
        assert call_kwargs["model"] == "llama3:8b"
        assert call_kwargs["temperature"] == 0.7
    
    @patch('src.core.model_manager.ChatOllama')
    def test_invoke_message_conversion(self, mock_ollama, temp_config_file):
        """测试消息格式转换"""
        manager = ModelManager(temp_config_file)
        mock_model = Mock()
        mock_response = Mock()
        mock_response.content = "Response"
        mock_model.invoke.return_value = mock_response
        mock_ollama.return_value = mock_model
        
        messages = [
            {"role": "system", "content": "System msg"},
            {"role": "user", "content": "User msg"},
            {"role": "assistant", "content": "Assistant msg"}
        ]
        
        manager.invoke(messages)
        
        # 验证调用了invoke方法
        mock_model.invoke.assert_called_once()
        call_args = mock_model.invoke.call_args[0][0]
        assert len(call_args) == 3
    
    @patch('src.core.model_manager.ChatOllama')
    def test_invoke_error_handling(self, mock_ollama, temp_config_file):
        """测试调用错误处理"""
        manager = ModelManager(temp_config_file)
        mock_model = Mock()
        mock_model.invoke.side_effect = Exception("Model error")
        mock_ollama.return_value = mock_model
        
        messages = [{"role": "user", "content": "Test"}]
        
        with pytest.raises(Exception) as exc_info:
            manager.invoke(messages)
        
        assert "Model error" in str(exc_info.value)
    
    @pytest.mark.asyncio
    @patch('src.core.model_manager.ChatOllama')
    async def test_ainvoke_success(self, mock_ollama, temp_config_file):
        """测试异步调用成功"""
        manager = ModelManager(temp_config_file)
        mock_model = Mock()
        mock_response = Mock()
        mock_response.content = "Async response"
        mock_model.ainvoke = Mock(return_value=mock_response)
        mock_ollama.return_value = mock_model
        
        messages = [{"role": "user", "content": "Test"}]
        result = await manager.ainvoke(messages)
        
        assert result == "Async response"
        mock_model.ainvoke.assert_called_once()
    
    def test_clear_cache(self, temp_config_file):
        """测试清除模型缓存"""
        manager = ModelManager(temp_config_file)
        
        # 添加一些缓存
        manager.models["test_key"] = Mock()
        assert len(manager.models) == 1
        
        manager.clear_cache()
        
        assert len(manager.models) == 0
    
    @patch('src.core.model_manager.ChatOllama')
    def test_custom_parameters(self, mock_ollama, temp_config_file):
        """测试自定义参数传递"""
        manager = ModelManager(temp_config_file)
        mock_ollama.return_value = Mock()
        
        manager.get_model(
            model_name="custom_model",
            temperature=0.9,
            top_p=0.95,
            max_tokens=3000
        )
        
        call_kwargs = mock_ollama.call_args[1]
        assert call_kwargs["temperature"] == 0.9
        assert call_kwargs["top_p"] == 0.95
        assert call_kwargs["num_predict"] == 3000
