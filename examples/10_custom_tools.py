"""
示例 10: 自定义工具开发
演示如何创建自定义工具并集成到智能体系统
"""

import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

logger = logging.getLogger(__name__)


class WeatherTool:
    """天气查询工具 (示例)"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """初始化天气工具
        
        Args:
            config: 配置字典
        """
        self.config = config or {}
        self.api_key = self.config.get("api_key", "demo_key")
    
    def get_weather(self, city: str) -> Dict[str, Any]:
        """查询天气
        
        Args:
            city: 城市名称
            
        Returns:
            天气信息字典
        """
        # 模拟天气数据
        weather_data = {
            "北京": {"temp": 15, "condition": "晴", "humidity": 45},
            "上海": {"temp": 20, "condition": "多云", "humidity": 60},
            "深圳": {"temp": 25, "condition": "雨", "humidity": 75},
        }
        
        result = weather_data.get(city, {"temp": 18, "condition": "未知", "humidity": 50})
        
        logger.info(f"查询天气: {city}")
        return {
            "city": city,
            "temperature": result["temp"],
            "condition": result["condition"],
            "humidity": result["humidity"],
            "unit": "摄氏度"
        }
    
    def get_forecast(self, city: str, days: int = 3) -> List[Dict[str, Any]]:
        """查询天气预报
        
        Args:
            city: 城市名称
            days: 预报天数
            
        Returns:
            预报信息列表
        """
        # 模拟预报数据
        forecast = []
        for i in range(days):
            forecast.append({
                "day": f"第{i+1}天",
                "temp_high": 20 + i,
                "temp_low": 12 + i,
                "condition": ["晴", "多云", "雨"][i % 3]
            })
        
        logger.info(f"查询{days}天预报: {city}")
        return forecast


class TextAnalysisTool:
    """文本分析工具 (示例)"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """初始化文本分析工具
        
        Args:
            config: 配置字典
        """
        self.config = config or {}
    
    def word_count(self, text: str) -> Dict[str, int]:
        """统计词数
        
        Args:
            text: 输入文本
            
        Returns:
            统计结果
        """
        words = text.split()
        chars = len(text)
        lines = text.count('\n') + 1
        
        return {
            "words": len(words),
            "characters": chars,
            "lines": lines
        }
    
    def extract_keywords(self, text: str, top_k: int = 5) -> List[str]:
        """提取关键词 (简化版)
        
        Args:
            text: 输入文本
            top_k: 返回前k个关键词
            
        Returns:
            关键词列表
        """
        # 简单的词频统计
        words = text.split()
        word_freq = {}
        
        for word in words:
            if len(word) > 1:  # 忽略单字符
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # 排序并返回top_k
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, freq in sorted_words[:top_k]]
    
    def sentiment_analysis(self, text: str) -> Dict[str, Any]:
        """情感分析 (简化版)
        
        Args:
            text: 输入文本
            
        Returns:
            情感分析结果
        """
        # 简单的关键词匹配
        positive_words = ["好", "棒", "优秀", "喜欢", "开心", "满意"]
        negative_words = ["差", "糟糕", "失望", "讨厌", "难过", "不满"]
        
        pos_count = sum(1 for word in positive_words if word in text)
        neg_count = sum(1 for word in negative_words if word in text)
        
        if pos_count > neg_count:
            sentiment = "积极"
            score = 0.6 + (pos_count - neg_count) * 0.1
        elif neg_count > pos_count:
            sentiment = "消极"
            score = 0.4 - (neg_count - pos_count) * 0.1
        else:
            sentiment = "中性"
            score = 0.5
        
        return {
            "sentiment": sentiment,
            "score": min(max(score, 0), 1),
            "positive_count": pos_count,
            "negative_count": neg_count
        }


class DatabaseTool:
    """数据库工具 (示例)"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """初始化数据库工具
        
        Args:
            config: 配置字典
        """
        self.config = config or {}
        self.data_store = {}  # 模拟数据库
    
    def save(self, key: str, value: Any) -> bool:
        """保存数据
        
        Args:
            key: 键
            value: 值
            
        Returns:
            是否成功
        """
        self.data_store[key] = value
        logger.info(f"保存数据: {key}")
        return True
    
    def get(self, key: str) -> Any:
        """获取数据
        
        Args:
            key: 键
            
        Returns:
            数据值
        """
        return self.data_store.get(key)
    
    def query(self, filter_func=None) -> List[Any]:
        """查询数据
        
        Args:
            filter_func: 过滤函数
            
        Returns:
            查询结果列表
        """
        if filter_func is None:
            return list(self.data_store.values())
        
        return [v for v in self.data_store.values() if filter_func(v)]
    
    def delete(self, key: str) -> bool:
        """删除数据
        
        Args:
            key: 键
            
        Returns:
            是否成功
        """
        if key in self.data_store:
            del self.data_store[key]
            logger.info(f"删除数据: {key}")
            return True
        return False


def example_1_weather_tool():
    """示例1: 使用天气工具"""
    print("\n" + "="*60)
    print("🌤️  示例1: 天气查询工具")
    print("="*60)
    
    weather = WeatherTool()
    
    # 查询当前天气
    print("\n1️⃣ 查询当前天气:")
    cities = ["北京", "上海", "深圳"]
    for city in cities:
        info = weather.get_weather(city)
        print(f"   {city}: {info['temperature']}°C, {info['condition']}, 湿度{info['humidity']}%")
    
    # 查询天气预报
    print("\n2️⃣ 查询天气预报:")
    forecast = weather.get_forecast("北京", days=3)
    for day_info in forecast:
        print(f"   {day_info['day']}: {day_info['temp_low']}-{day_info['temp_high']}°C, {day_info['condition']}")


def example_2_text_analysis_tool():
    """示例2: 使用文本分析工具"""
    print("\n" + "="*60)
    print("📝 示例2: 文本分析工具")
    print("="*60)
    
    analyzer = TextAnalysisTool()
    
    sample_text = """
    这是一个非常好的产品。我很喜欢它的设计和功能。
    使用起来很方便，性能也很优秀。
    总体来说，我对这个产品非常满意。
    """
    
    # 词数统计
    print("\n1️⃣ 词数统计:")
    stats = analyzer.word_count(sample_text)
    print(f"   词数: {stats['words']}")
    print(f"   字符数: {stats['characters']}")
    print(f"   行数: {stats['lines']}")
    
    # 关键词提取
    print("\n2️⃣ 关键词提取:")
    keywords = analyzer.extract_keywords(sample_text, top_k=5)
    print(f"   关键词: {', '.join(keywords)}")
    
    # 情感分析
    print("\n3️⃣ 情感分析:")
    sentiment = analyzer.sentiment_analysis(sample_text)
    print(f"   情感倾向: {sentiment['sentiment']}")
    print(f"   情感分数: {sentiment['score']:.2f}")
    print(f"   积极词数: {sentiment['positive_count']}")
    print(f"   消极词数: {sentiment['negative_count']}")


def example_3_database_tool():
    """示例3: 使用数据库工具"""
    print("\n" + "="*60)
    print("💾 示例3: 数据库工具")
    print("="*60)
    
    db = DatabaseTool()
    
    # 保存数据
    print("\n1️⃣ 保存数据:")
    data_items = [
        ("user_1", {"name": "张三", "age": 25, "role": "开发"}),
        ("user_2", {"name": "李四", "age": 30, "role": "测试"}),
        ("user_3", {"name": "王五", "age": 28, "role": "开发"}),
    ]
    
    for key, value in data_items:
        db.save(key, value)
        print(f"   ✅ 保存: {key}")
    
    # 获取数据
    print("\n2️⃣ 获取数据:")
    user = db.get("user_1")
    print(f"   user_1: {user}")
    
    # 查询数据
    print("\n3️⃣ 查询数据 (开发人员):")
    developers = db.query(lambda x: isinstance(x, dict) and x.get("role") == "开发")
    for dev in developers:
        print(f"   - {dev['name']}, {dev['age']}岁")
    
    # 删除数据
    print("\n4️⃣ 删除数据:")
    db.delete("user_2")
    print("   ✅ 已删除 user_2")
    
    # 验证删除
    remaining = db.query()
    print(f"\n5️⃣ 剩余数据: {len(remaining)} 条")


def example_4_integration():
    """示例4: 工具集成演示"""
    print("\n" + "="*60)
    print("🔧 示例4: 工具集成到智能体")
    print("="*60)
    
    print("\n如何集成自定义工具:")
    print("""
    1. 创建工具类
       class MyTool:
           def __init__(self, config):
               pass
           
           def my_function(self, param):
               # 实现功能
               return result
    
    2. 在智能体中注册工具
       from src.agents import BaseAgent
       
       class MyAgent(BaseAgent):
           def __init__(self):
               super().__init__()
               self.my_tool = MyTool(config)
           
           def execute(self, task):
               result = self.my_tool.my_function(task)
               return result
    
    3. 配置工具参数
       # config/agents.yaml
       my_agent:
           tools:
               - my_tool
           config:
               api_key: "xxx"
    
    4. 使用工具
       agent = MyAgent()
       result = agent.execute(task)
    """)
    
    print("\n💡 工具开发最佳实践:")
    print("   1. 清晰的接口设计")
    print("   2. 完善的错误处理")
    print("   3. 详细的日志记录")
    print("   4. 支持配置参数")
    print("   5. 编写单元测试")


def main():
    """主函数"""
    print("\n" + "="*70)
    print("🔧 自定义工具开发示例")
    print("="*70)
    
    print("\n本示例展示如何开发和使用自定义工具")
    print("包括天气查询、文本分析、数据库操作等")
    print()
    
    try:
        example_1_weather_tool()
        example_2_text_analysis_tool()
        example_3_database_tool()
        example_4_integration()
        
        print("\n" + "="*70)
        print("✅ 所有示例运行完成!")
        print("="*70)
        
        print("\n📚 扩展建议:")
        print("   1. 集成真实的API服务")
        print("   2. 添加缓存机制提升性能")
        print("   3. 实现异步调用支持")
        print("   4. 添加重试和容错逻辑")
        print("   5. 编写完整的文档和测试")
        print()
        
    except Exception as e:
        print(f"\n❌ 运行出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
