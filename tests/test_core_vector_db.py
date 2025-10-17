"""VectorDBManager 单元测试"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
from src.core.vector_db import VectorDBManager


class TestVectorDBManager:
    """测试向量数据库管理器"""
    
    def test_init_with_default_config(self, temp_config_file):
        """测试使用默认配置初始化"""
        manager = VectorDBManager(temp_config_file)
        
        assert manager is not None
        assert manager.config is not None
        assert manager.persist_directory is not None
        assert manager.collection_name is not None
        assert manager.embedding_model is not None
    
    def test_load_config_error_handling(self):
        """测试配置加载错误处理"""
        manager = VectorDBManager("nonexistent_config.yaml")
        
        # 应该使用默认配置
        assert manager.config == {}
        assert manager.persist_directory == "./data/vectordb"
    
    def test_lazy_initialization(self, temp_config_file):
        """测试延迟初始化"""
        manager = VectorDBManager(temp_config_file)
        
        # 初始化时不应该创建连接
        assert manager.client is None
        assert manager.collection is None
        assert manager.embeddings is None
    
    @patch('chromadb.PersistentClient')
    @patch('langchain_community.embeddings.OllamaEmbeddings')
    def test_init_db(self, mock_embeddings, mock_chromadb, temp_config_file):
        """测试初始化数据库连接"""
        # 设置Mock
        mock_client = Mock()
        mock_collection = Mock()
        
        mock_chromadb.return_value = mock_client
        mock_client.get_or_create_collection.return_value = mock_collection
        
        manager = VectorDBManager(temp_config_file)
        manager._init_db()
        
        # 验证初始化调用
        assert mock_chromadb.called
        assert mock_client.get_or_create_collection.called
        
        assert manager.client is not None
        assert manager.collection is not None
        assert manager.embeddings is not None
    
    @patch('chromadb.PersistentClient')
    @patch('langchain_community.embeddings.OllamaEmbeddings')
    def test_add_documents(self, mock_embeddings_class, mock_chromadb, temp_config_file):
        """测试添加文档"""
        # 设置Mock
        mock_client = Mock()
        mock_collection = Mock()
        mock_embeddings = Mock()
        
        mock_chromadb.return_value = mock_client
        mock_client.get_or_create_collection.return_value = mock_collection
        mock_embeddings_class.return_value = mock_embeddings
        
        # Mock embedding结果
        mock_embeddings.embed_documents.return_value = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
        
        manager = VectorDBManager(temp_config_file)
        
        documents = ["文档1", "文档2"]
        metadatas = [{"source": "test1"}, {"source": "test2"}]
        
        result = manager.add_documents(documents, metadatas)
        
        # 验证调用
        mock_embeddings.embed_documents.assert_called_once_with(documents)
        mock_collection.add.assert_called_once()
        
        # 验证返回的ID
        assert len(result) == 2
        assert all(isinstance(id, str) for id in result)
    
    @patch('chromadb.PersistentClient')
    @patch('langchain_community.embeddings.OllamaEmbeddings')
    def test_semantic_search(self, mock_embeddings_class, mock_chromadb, temp_config_file):
        """测试语义搜索"""
        mock_client = Mock()
        mock_collection = Mock()
        mock_embeddings = Mock()
        
        mock_chromadb.return_value = mock_client
        mock_client.get_or_create_collection.return_value = mock_collection
        mock_embeddings_class.return_value = mock_embeddings
        
        # Mock查询向量
        mock_embeddings.embed_query.return_value = [0.1, 0.2, 0.3]
        
        # Mock搜索结果
        mock_collection.query.return_value = {
            'ids': [['doc1', 'doc2']],
            'documents': [['文档1内容', '文档2内容']],
            'metadatas': [[{'source': 'test1'}, {'source': 'test2'}]],
            'distances': [[0.1, 0.2]]
        }
        
        manager = VectorDBManager(temp_config_file)
        
        results = manager.semantic_search("测试查询", top_k=2)
        
        # 验证调用
        mock_embeddings.embed_query.assert_called_once_with("测试查询")
        mock_collection.query.assert_called_once()
        
        # 验证结果格式
        assert len(results) == 2
        assert results[0]['id'] == 'doc1'
        assert results[0]['document'] == '文档1内容'
        assert results[0]['metadata'] == {'source': 'test1'}
        assert results[0]['distance'] == 0.1
    
    @patch('chromadb.PersistentClient')
    @patch('langchain_community.embeddings.OllamaEmbeddings')
    def test_get_document(self, mock_embeddings_class, mock_chromadb, temp_config_file):
        """测试获取文档"""
        mock_client = Mock()
        mock_collection = Mock()
        mock_embeddings = Mock()
        
        mock_chromadb.return_value = mock_client
        mock_client.get_or_create_collection.return_value = mock_collection
        mock_embeddings_class.return_value = mock_embeddings
        
        # Mock get结果
        mock_collection.get.return_value = {
            'ids': ['doc1'],
            'documents': ['文档内容'],
            'metadatas': [{'source': 'test'}]
        }
        
        manager = VectorDBManager(temp_config_file)
        
        result = manager.get_document('doc1')
        
        # 验证调用
        mock_collection.get.assert_called_once_with(ids=['doc1'])
        
        # 验证结果
        assert result is not None
        assert result['id'] == 'doc1'
        assert result['document'] == '文档内容'
        assert result['metadata'] == {'source': 'test'}
    
    @patch('chromadb.PersistentClient')
    @patch('langchain_community.embeddings.OllamaEmbeddings')
    def test_delete_document(self, mock_embeddings_class, mock_chromadb, temp_config_file):
        """测试删除文档"""
        mock_client = Mock()
        mock_collection = Mock()
        mock_embeddings = Mock()
        
        mock_chromadb.return_value = mock_client
        mock_client.get_or_create_collection.return_value = mock_collection
        mock_embeddings_class.return_value = mock_embeddings
        
        manager = VectorDBManager(temp_config_file)
        
        manager.delete_document('doc1')
        
        # 验证调用
        mock_collection.delete.assert_called_once_with(ids=['doc1'])
    
    @patch('chromadb.PersistentClient')
    @patch('langchain_community.embeddings.OllamaEmbeddings')
    def test_get_collection_stats(self, mock_embeddings_class, mock_chromadb, temp_config_file):
        """测试获取集合统计信息"""
        mock_client = Mock()
        mock_collection = Mock()
        mock_embeddings = Mock()
        
        mock_chromadb.return_value = mock_client
        mock_client.get_or_create_collection.return_value = mock_collection
        mock_embeddings_class.return_value = mock_embeddings
        
        mock_collection.count.return_value = 100
        
        manager = VectorDBManager(temp_config_file)
        
        stats = manager.get_collection_stats()
        
        assert stats['collection_name'] == manager.collection_name
        assert stats['document_count'] == 100
        assert stats['persist_directory'] == manager.persist_directory
