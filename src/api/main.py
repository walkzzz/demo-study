"""FastAPI服务主程序"""

import sys
from pathlib import Path
from typing import Dict, Any

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging

from src.cli.main import OfficeSuperAgentCLI

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title="日常办公超级智能体API",
    description="基于LangChain和Ollama的智能办公助手",
    version="0.1.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局变量
agent_cli = None


class TaskRequest(BaseModel):
    """任务请求模型"""
    user_input: str
    context: Dict[str, Any] = {}


class TaskResponse(BaseModel):
    """任务响应模型"""
    status: str
    result: Any
    task_understanding: Dict[str, Any] = {}
    subtasks_count: int = 0


@app.on_event("startup")
async def startup_event():
    """启动事件"""
    global agent_cli
    logger.info("启动日常办公超级智能体服务...")
    try:
        agent_cli = OfficeSuperAgentCLI()
        logger.info("服务启动成功!")
    except Exception as e:
        logger.error(f"服务启动失败: {e}")
        raise


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "日常办公超级智能体API",
        "version": "0.1.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}


@app.post("/api/task", response_model=TaskResponse)
async def process_task(request: TaskRequest):
    """处理任务请求
    
    Args:
        request: 任务请求
        
    Returns:
        任务响应
    """
    try:
        logger.info(f"接收到任务: {request.user_input[:50]}...")
        
        result = agent_cli.super_agent.process_request(request.user_input)
        
        return TaskResponse(**result)
        
    except Exception as e:
        logger.error(f"处理任务失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/agents")
async def get_agents():
    """获取可用的智能体列表"""
    agents = list(agent_cli.agents.keys())
    return {
        "agents": agents,
        "count": len(agents)
    }


@app.get("/api/memory/stats")
async def get_memory_stats():
    """获取记忆统计"""
    stats = agent_cli.memory_manager.get_memory_stats()
    return stats


@app.get("/api/vector_db/stats")
async def get_vector_db_stats():
    """获取向量数据库统计"""
    stats = agent_cli.vector_db.get_collection_stats()
    return stats


if __name__ == "__main__":
    import uvicorn
    
    # 读取配置
    import yaml
    try:
        with open("config/config.yaml", 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            api_config = config.get('api', {})
            host = api_config.get('host', '0.0.0.0')
            port = api_config.get('port', 8000)
    except:
        host = '0.0.0.0'
        port = 8000
    
    print(f"\n🚀 启动API服务: http://{host}:{port}")
    print(f"📖 API文档: http://{host}:{port}/docs\n")
    
    uvicorn.run(app, host=host, port=port)
