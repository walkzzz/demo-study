"""验证模型配置脚本

用于检查 config.yaml 和 agents.yaml 配置是否正确
以及本地 Ollama 模型是否可用
"""

import yaml
import requests
import sys
from pathlib import Path


def load_config(config_path: str):
    """加载配置文件"""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"❌ 加载配置文件失败 {config_path}: {e}")
        return None


def check_ollama_service(base_url: str):
    """检查 Ollama 服务是否运行"""
    try:
        response = requests.get(f"{base_url}/api/tags", timeout=5)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, None
    except Exception as e:
        return False, str(e)


def verify_model_availability(models_data, required_models):
    """验证所需模型是否已安装"""
    if not models_data:
        return []
    
    installed_models = []
    if 'models' in models_data:
        for model in models_data['models']:
            installed_models.append(model['name'])
    
    results = []
    for model_name in required_models:
        # 检查完整匹配或部分匹配（处理版本号）
        found = False
        for installed in installed_models:
            if model_name in installed or installed.startswith(model_name.split(':')[0]):
                found = True
                break
        results.append((model_name, found))
    
    return results


def main():
    """主验证流程"""
    print("=" * 60)
    print("模型配置验证工具")
    print("=" * 60)
    print()
    
    # 1. 检查配置文件是否存在
    print("📋 步骤 1: 检查配置文件")
    config_path = Path("config/config.yaml")
    agents_path = Path("config/agents.yaml")
    
    if not config_path.exists():
        print(f"❌ 配置文件不存在: {config_path}")
        return False
    else:
        print(f"✅ 主配置文件存在: {config_path}")
    
    if not agents_path.exists():
        print(f"❌ 智能体配置文件不存在: {agents_path}")
        return False
    else:
        print(f"✅ 智能体配置文件存在: {agents_path}")
    
    print()
    
    # 2. 加载并解析配置
    print("📋 步骤 2: 解析配置文件")
    config = load_config(str(config_path))
    agents_config = load_config(str(agents_path))
    
    if not config:
        print("❌ 主配置文件解析失败")
        return False
    else:
        print("✅ 主配置文件解析成功")
    
    if not agents_config:
        print("❌ 智能体配置文件解析失败")
        return False
    else:
        print("✅ 智能体配置文件解析成功")
    
    print()
    
    # 3. 提取配置信息
    print("📋 步骤 3: 读取模型配置")
    ollama_config = config.get('ollama', {})
    base_url = ollama_config.get('base_url', 'http://localhost:11434')
    default_model = ollama_config.get('default_model', 'llama3:8b')
    embedding_model = ollama_config.get('embedding_model', 'nomic-embed-text:latest')
    
    print(f"   Ollama 地址: {base_url}")
    print(f"   默认模型: {default_model}")
    print(f"   嵌入模型: {embedding_model}")
    print()
    
    # 4. 收集所有需要的模型
    required_models = set()
    required_models.add(default_model)
    required_models.add(embedding_model)
    
    # 从 model_strategy 中收集
    model_strategy = config.get('model_strategy', {})
    for task_type, strategy in model_strategy.items():
        if 'model' in strategy:
            required_models.add(strategy['model'])
    
    # 从 agents 中收集
    agents = agents_config.get('agents', {})
    for agent_name, agent_config in agents.items():
        if 'model_name' in agent_config:
            required_models.add(agent_config['model_name'])
    
    print(f"📋 步骤 4: 需要的模型清单 (共 {len(required_models)} 个)")
    for model in sorted(required_models):
        print(f"   - {model}")
    print()
    
    # 5. 检查 Ollama 服务
    print("📋 步骤 5: 检查 Ollama 服务")
    service_running, models_data = check_ollama_service(base_url)
    
    if not service_running:
        print(f"❌ Ollama 服务未运行: {models_data}")
        print(f"   请确保 Ollama 服务已启动: {base_url}")
        return False
    else:
        print(f"✅ Ollama 服务运行正常")
    
    print()
    
    # 6. 验证模型可用性
    print("📋 步骤 6: 验证模型安装状态")
    model_results = verify_model_availability(models_data, required_models)
    
    all_available = True
    for model_name, available in model_results:
        if available:
            print(f"   ✅ {model_name}")
        else:
            print(f"   ❌ {model_name} - 未安装")
            all_available = False
    
    print()
    
    # 7. 显示智能体配置摘要
    print("📋 步骤 7: 智能体配置摘要")
    for agent_name, agent_config in agents.items():
        model = agent_config.get('model_name', 'N/A')
        temp = agent_config.get('temperature', 'N/A')
        desc = agent_config.get('description', 'N/A')
        print(f"   {agent_name}:")
        print(f"      模型: {model}")
        print(f"      温度: {temp}")
        print(f"      描述: {desc}")
    
    print()
    print("=" * 60)
    
    # 8. 最终结果
    if all_available:
        print("✅ 配置验证通过！所有模型均可用")
        print("   可以运行: python demo.py")
        print("   或启动系统: python src/cli/main.py")
        return True
    else:
        print("⚠️  配置验证部分通过，但有模型缺失")
        print("   请运行以下命令安装缺失的模型：")
        for model_name, available in model_results:
            if not available:
                print(f"   ollama pull {model_name}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
