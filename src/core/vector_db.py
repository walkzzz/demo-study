"""向量数据库管理器

基于 ChromaDB 实现知识库的向量化存储和语义检索
"""

import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
import yaml

logger = logging.getLogger(__name__)


class VectorDBManager:
    """向量数据库管理器"""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        """初始化向量数据库管理器
        
        Args:
            config_path: 配置文件路径
        """
        self.config = self._load_config(config_path)
        self.db_config = self.config.get("vector_db", {})
        
        self.persist_directory = self.db_config.get("persist_directory", "./data/vectordb")
        self.collection_name = self.db_config.get("collection_name", "office_knowledge")
        self.embedding_model = self.db_config.get("embedding_model", "nomic-embed-text")
        
        # 确保持久化目录存在
        Path(self.persist_directory).mkdir(parents=True, exist_ok=True)
        
        # 延迟初始化 ChromaDB (需要时才导入和初始化)
        self.client = None
        self.collection = None
        self.embeddings = None
        
        logger.info(f"向量数据库管理器初始化完成，存储路径: {self.persist_directory}")
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """加载配置文件"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"加载配置文件失败: {e}")
            return {}
    
    def _init_db(self):
        """初始化数据库连接"""
        if self.client is not None:
            return
        
        try:
            import chromadb
            from langchain_community.embeddings import OllamaEmbeddings
            
            # 初始化 ChromaDB 客户端
            self.client = chromadb.PersistentClient(path=self.persist_directory)
            
            # 获取或创建集合
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"description": "Office knowledge base"}
            )
            
            # 初始化 Embedding 模型
            ollama_config = self.config.get("ollama", {})
            base_url = ollama_config.get("base_url", "http://localhost:11434")
            
            self.embeddings = OllamaEmbeddings(
                base_url=base_url,
                model=self.embedding_model
            )
            
            logger.info("ChromaDB 初始化完成")
            
        except Exception as e:
            logger.error(f"初始化向量数据库失败: {e}")
            raise
    
    def add_documents(
        self,
        documents: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None
    ) -> List[str]:
        """添加文档到向量数据库
        
        Args:
            documents: 文档内容列表
            metadatas: 元数据列表
            ids: 文档ID列表，如果不提供则自动生成
            
        Returns:
            文档ID列表
        """
        self._init_db()
        
        try:
            # 生成 embeddings
            embeddings = self.embeddings.embed_documents(documents)
            
            # 生成ID
            if ids is None:
                import uuid
                ids = [str(uuid.uuid4()) for _ in documents]
            
            # 添加到集合
            self.collection.add(
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas or [{} for _ in documents],
                ids=ids
            )
            
            logger.info(f"成功添加 {len(documents)} 个文档到向量数据库")
            return ids
            
        except Exception as e:
            logger.error(f"添加文档失败: {e}")
            raise
    
    def semantic_search(
        self,
        query: str,
        top_k: int = 5,
        filter_dict: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """语义搜索
        
        Args:
            query: 查询文本
            top_k: 返回结果数量
            filter_dict: 元数据过滤条件
            
        Returns:
            搜索结果列表，每个结果包含 {id, document, metadata, distance}
        """
        self._init_db()
        
        try:
            # 生成查询向量
            query_embedding = self.embeddings.embed_query(query)
            
            # 执行搜索
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                where=filter_dict
            )
            
            # 格式化结果
            formatted_results = []
            if results['ids'] and len(results['ids'][0]) > 0:
                for i in range(len(results['ids'][0])):
                    formatted_results.append({
                        "id": results['ids'][0][i],
                        "document": results['documents'][0][i],
                        "metadata": results['metadatas'][0][i] if results['metadatas'] else {},
                        "distance": results['distances'][0][i] if 'distances' in results else None
                    })
            
            logger.debug(f"语义搜索返回 {len(formatted_results)} 个结果")
            return formatted_results
            
        except Exception as e:
            logger.error(f"语义搜索失败: {e}")
            raise
    
    def get_document(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """根据ID获取文档
        
        Args:
            doc_id: 文档ID
            
        Returns:
            文档信息，如果不存在返回None
        """
        self._init_db()
        
        try:
            results = self.collection.get(ids=[doc_id])
            
            if results['ids'] and len(results['ids']) > 0:
                return {
                    "id": results['ids'][0],
                    "document": results['documents'][0],
                    "metadata": results['metadatas'][0] if results['metadatas'] else {}
                }
            
            return None
            
        except Exception as e:
            logger.error(f"获取文档失败: {e}")
            return None
    
    def update_document(
        self,
        doc_id: str,
        document: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """更新文档
        
        Args:
            doc_id: 文档ID
            document: 新的文档内容
            metadata: 新的元数据
        """
        self._init_db()
        
        try:
            update_data = {"ids": [doc_id]}
            
            if document is not None:
                embedding = self.embeddings.embed_documents([document])[0]
                update_data["embeddings"] = [embedding]
                update_data["documents"] = [document]
            
            if metadata is not None:
                update_data["metadatas"] = [metadata]
            
            self.collection.update(**update_data)
            logger.info(f"文档已更新: {doc_id}")
            
        except Exception as e:
            logger.error(f"更新文档失败: {e}")
            raise
    
    def delete_document(self, doc_id: str):
        """删除文档
        
        Args:
            doc_id: 文档ID
        """
        self._init_db()
        
        try:
            self.collection.delete(ids=[doc_id])
            logger.info(f"文档已删除: {doc_id}")
        except Exception as e:
            logger.error(f"删除文档失败: {e}")
            raise
    
    def delete_by_metadata(self, filter_dict: Dict[str, Any]):
        """根据元数据删除文档
        
        Args:
            filter_dict: 元数据过滤条件
        """
        self._init_db()
        
        try:
            self.collection.delete(where=filter_dict)
            logger.info(f"已删除符合条件的文档: {filter_dict}")
        except Exception as e:
            logger.error(f"批量删除文档失败: {e}")
            raise
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """获取集合统计信息
        
        Returns:
            统计信息字典
        """
        self._init_db()
        
        try:
            count = self.collection.count()
            return {
                "collection_name": self.collection_name,
                "document_count": count,
                "persist_directory": self.persist_directory
            }
        except Exception as e:
            logger.error(f"获取统计信息失败: {e}")
            return {}
    
    def clear_collection(self):
        """清空集合"""
        self._init_db()
        
        try:
            # 删除并重建集合
            self.client.delete_collection(name=self.collection_name)
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "Office knowledge base"}
            )
            logger.warning("向量数据库集合已清空")
        except Exception as e:
            logger.error(f"清空集合失败: {e}")
            raise

