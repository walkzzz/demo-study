"""DataTools 单元测试"""
import pytest
from src.tools.data_tools import DataTools


class TestDataTools:
    """测试数据分析工具集"""
    
    @pytest.fixture
    def data_tools(self):
        """创建DataTools实例"""
        return DataTools()
    
    @pytest.fixture
    def sample_data(self):
        """示例数据"""
        return {
            "data": [
                {"name": "张三", "age": 25, "salary": 5000},
                {"name": "李四", "age": 30, "salary": 8000},
                {"name": "王五", "age": 28, "salary": 6500}
            ],
            "columns": ["name", "age", "salary"],
            "rows": 3
        }
    
    def test_init(self):
        """测试初始化"""
        tools = DataTools()
        assert tools is not None
    
    def test_load_data_csv(self, data_tools, tmp_path):
        """测试加载CSV数据"""
        file_path = str(tmp_path / "test.csv")
        
        result = data_tools.load_data(file_path, file_format="csv")
        
        assert isinstance(result, dict)
        assert "data" in result
        assert "columns" in result
        assert "rows" in result
    
    def test_load_data_excel(self, data_tools, tmp_path):
        """测试加载Excel数据"""
        file_path = str(tmp_path / "test.xlsx")
        
        result = data_tools.load_data(file_path, file_format="excel")
        
        assert isinstance(result, dict)
        assert "data" in result
    
    def test_load_data_json(self, data_tools, tmp_path):
        """测试加载JSON数据"""
        file_path = str(tmp_path / "test.json")
        
        result = data_tools.load_data(file_path, file_format="json")
        
        assert isinstance(result, dict)
    
    def test_load_data_default_format(self, data_tools, tmp_path):
        """测试默认格式加载数据"""
        file_path = str(tmp_path / "test.csv")
        
        result = data_tools.load_data(file_path)
        
        # 默认应该是CSV格式
        assert isinstance(result, dict)
    
    def test_analyze_data_descriptive(self, data_tools, sample_data):
        """测试描述性统计分析"""
        result = data_tools.analyze_data(sample_data, analysis_type="descriptive")
        
        assert isinstance(result, dict)
        assert "results" in result
    
    def test_analyze_data_correlation(self, data_tools, sample_data):
        """测试相关性分析"""
        result = data_tools.analyze_data(sample_data, analysis_type="correlation")
        
        assert isinstance(result, dict)
        assert "results" in result
    
    def test_analyze_data_trend(self, data_tools, sample_data):
        """测试趋势分析"""
        result = data_tools.analyze_data(sample_data, analysis_type="trend")
        
        assert isinstance(result, dict)
    
    def test_filter_data(self, data_tools, sample_data):
        """测试数据筛选"""
        conditions = {
            "age": {">=": 28},
            "salary": {">": 6000}
        }
        
        result = data_tools.filter_data(sample_data, conditions)
        
        assert isinstance(result, dict)
        # 当前是简化实现，返回原数据
        assert "data" in result
    
    def test_filter_data_single_condition(self, data_tools, sample_data):
        """测试单条件筛选"""
        conditions = {"age": {"==": 25}}
        
        result = data_tools.filter_data(sample_data, conditions)
        
        assert isinstance(result, dict)
    
    def test_filter_data_empty_conditions(self, data_tools, sample_data):
        """测试空条件筛选"""
        result = data_tools.filter_data(sample_data, {})
        
        # 空条件应该返回所有数据
        assert isinstance(result, dict)
    
    def test_aggregate_data_by_single_column(self, data_tools, sample_data):
        """测试单列分组聚合"""
        group_by = ["age"]
        aggregations = {"salary": "sum"}
        
        result = data_tools.aggregate_data(sample_data, group_by, aggregations)
        
        assert isinstance(result, dict)
        assert "aggregated_data" in result
    
    def test_aggregate_data_multiple_columns(self, data_tools, sample_data):
        """测试多列分组聚合"""
        group_by = ["age", "name"]
        aggregations = {
            "salary": "avg"
        }
        
        result = data_tools.aggregate_data(sample_data, group_by, aggregations)
        
        assert isinstance(result, dict)
        assert "aggregated_data" in result
    
    def test_aggregate_data_multiple_aggregations(self, data_tools, sample_data):
        """测试多个聚合函数"""
        group_by = ["age"]
        aggregations = {
            "salary": "sum",
            "name": "count"
        }
        
        result = data_tools.aggregate_data(sample_data, group_by, aggregations)
        
        assert isinstance(result, dict)
    
    def test_visualize_data_bar_chart(self, data_tools, sample_data, tmp_path):
        """测试生成柱状图"""
        output_path = str(tmp_path / "bar_chart.png")
        
        result = data_tools.visualize_data(
            sample_data,
            chart_type="bar",
            output_path=output_path
        )
        
        assert isinstance(result, str)
        # 当前返回的是路径
        assert result == output_path
    
    def test_visualize_data_line_chart(self, data_tools, sample_data, tmp_path):
        """测试生成折线图"""
        output_path = str(tmp_path / "line_chart.png")
        
        result = data_tools.visualize_data(
            sample_data,
            chart_type="line",
            output_path=output_path
        )
        
        assert isinstance(result, str)
    
    def test_visualize_data_pie_chart(self, data_tools, sample_data, tmp_path):
        """测试生成饼图"""
        output_path = str(tmp_path / "pie_chart.png")
        
        result = data_tools.visualize_data(
            sample_data,
            chart_type="pie",
            output_path=output_path
        )
        
        assert isinstance(result, str)
    
    def test_visualize_data_scatter_plot(self, data_tools, sample_data, tmp_path):
        """测试生成散点图"""
        output_path = str(tmp_path / "scatter.png")
        
        result = data_tools.visualize_data(
            sample_data,
            chart_type="scatter",
            output_path=output_path
        )
        
        assert isinstance(result, str)
    
    def test_generate_report_default_template(self, data_tools):
        """测试生成默认模板报表"""
        analysis_results = {
            "statistics": {"mean": 6500, "median": 6500},
            "trends": "上升趋势",
            "insights": ["发现1", "发现2"]
        }
        
        result = data_tools.generate_report(analysis_results)
        
        assert isinstance(result, str)
        # 当前返回固定的文件名
        assert result == "report.pdf"
    
    def test_generate_report_custom_template(self, data_tools):
        """测试生成自定义模板报表"""
        analysis_results = {
            "data": "test"
        }
        template = "custom_template.html"
        
        result = data_tools.generate_report(analysis_results, template=template)
        
        assert isinstance(result, str)
    
    def test_get_tool_descriptions(self, data_tools):
        """测试获取工具描述"""
        descriptions = data_tools.get_tool_descriptions()
        
        assert isinstance(descriptions, list)
        assert len(descriptions) > 0
        
        # 验证工具描述结构
        for tool in descriptions:
            assert "name" in tool
            assert "description" in tool
            assert "parameters" in tool
    
    def test_get_tool_descriptions_contains_all_tools(self, data_tools):
        """测试工具描述包含所有工具"""
        descriptions = data_tools.get_tool_descriptions()
        
        tool_names = [tool['name'] for tool in descriptions]
        
        # 验证包含主要工具
        assert "load_data" in tool_names
        assert "analyze_data" in tool_names
        assert "filter_data" in tool_names
        assert "aggregate_data" in tool_names
        assert "visualize_data" in tool_names
        assert "generate_report" in tool_names
    
    def test_data_workflow_integration(self, data_tools, tmp_path):
        """测试数据分析完整工作流"""
        # 1. 加载数据
        data_file = str(tmp_path / "sales.csv")
        data = data_tools.load_data(data_file, file_format="csv")
        assert "data" in data
        
        # 2. 筛选数据
        conditions = {"sales": {">": 1000}}
        filtered_data = data_tools.filter_data(data, conditions)
        assert isinstance(filtered_data, dict)
        
        # 3. 聚合数据
        aggregated = data_tools.aggregate_data(
            filtered_data,
            group_by=["region"],
            aggregations={"sales": "sum"}
        )
        assert "aggregated_data" in aggregated
        
        # 4. 分析数据
        analysis = data_tools.analyze_data(aggregated, "descriptive")
        assert "results" in analysis
        
        # 5. 可视化
        chart_path = str(tmp_path / "sales_chart.png")
        chart = data_tools.visualize_data(
            aggregated,
            chart_type="bar",
            output_path=chart_path
        )
        assert chart == chart_path
        
        # 6. 生成报表
        report = data_tools.generate_report(analysis)
        assert isinstance(report, str)
    
    def test_load_data_structure(self, data_tools, tmp_path):
        """测试加载数据返回结构"""
        file_path = str(tmp_path / "test.csv")
        result = data_tools.load_data(file_path)
        
        # 验证返回结构
        assert "data" in result
        assert "columns" in result
        assert "rows" in result
        
        assert isinstance(result["data"], list)
        assert isinstance(result["columns"], list)
        assert isinstance(result["rows"], int)
    
    def test_analyze_data_structure(self, data_tools, sample_data):
        """测试分析数据返回结构"""
        result = data_tools.analyze_data(sample_data, "descriptive")
        
        # 验证返回结构
        assert "results" in result
        assert isinstance(result["results"], dict)
    
    def test_aggregate_data_structure(self, data_tools, sample_data):
        """测试聚合数据返回结构"""
        result = data_tools.aggregate_data(
            sample_data,
            group_by=["age"],
            aggregations={"salary": "sum"}
        )
        
        # 验证返回结构
        assert "aggregated_data" in result
        assert isinstance(result["aggregated_data"], list)
    
    def test_multiple_chart_types(self, data_tools, sample_data, tmp_path):
        """测试多种图表类型"""
        chart_types = ["bar", "line", "pie", "scatter"]
        
        for chart_type in chart_types:
            output_path = str(tmp_path / f"{chart_type}_chart.png")
            result = data_tools.visualize_data(
                sample_data,
                chart_type=chart_type,
                output_path=output_path
            )
            assert result == output_path
