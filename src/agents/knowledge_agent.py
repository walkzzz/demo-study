"""知识问答智能体 - 处理知识库问答任务"""
import logging
from typing import Dict, Any
from .base_agent import BaseAgent

logger = logging.getLogger(__name__)

class KnowledgeAgent(BaseAgent):
    """知识问答智能体"""
    
    def __init__(self, name, model_manager, prompt_engine, memory_manager, tools, vector_db, config=None):
        super().__init__(name, model_manager, prompt_engine, memory_manager, tools, config)
        self.vector_db = vector_db
    
    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """执行知识问答任务"""
        logger.info(f"{self.name} 执行任务: {task.get('description')}")
        
        task_type = task.get('type', 'qa')
        
        if task_type == 'qa':
            return self._answer_question(task)
        elif task_type == 'index':
            return self._index_document(task)
        else:
            return {"status": "error", "message": f"未知任务类型: {task_type}"}
    
    def _answer_question(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """回答问题"""
        question = task.get('question', '')
        
        # 语义搜索相关文档
        search_results = self.vector_db.semantic_search(question, top_k=5)
        
        # 构建上下文
        context = "\n\n".join([r["document"] for r in search_results])
        
        # 使用LLM生成答案
        prompt = self.prompt_engine.render_knowledge_qa(question, context)
        messages = [{"role": "user", "content": prompt}]
        
        answer = self.model_manager.invoke(
            messages,
            model_name=self.model_name,
            temperature=0.2
        )
        
        return {
            "status": "success",
            "answer": answer,
            "sources": search_results
        }
    
    def _index_document(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """索引文档到知识库"""
        content = task.get('content', '')
        metadata = task.get('metadata', {})
        
        doc_ids = self.vector_db.add_documents([content], [metadata])
        
        return {"status": "success", "document_ids": doc_ids}
