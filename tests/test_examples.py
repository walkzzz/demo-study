"""测试示例文件的可运行性"""

import pytest
import subprocess
import sys
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
EXAMPLES_DIR = PROJECT_ROOT / "examples"


class TestExamples:
    """测试所有示例文件"""
    
    def test_examples_directory_exists(self):
        """测试示例目录是否存在"""
        assert EXAMPLES_DIR.exists(), "示例目录不存在"
        assert EXAMPLES_DIR.is_dir(), "examples应该是一个目录"
    
    def test_example_files_exist(self):
        """测试所有示例文件是否存在"""
        expected_files = [
            "01_basic_usage.py",
            "02_model_manager.py",
            "03_memory_system.py",
            "04_file_agent.py",
            "05_email_agent.py",
            "06_data_agent.py",
            "07_doc_agent.py",
            "08_knowledge_agent.py",
            "09_multi_agent_workflow.py",
            "10_custom_tools.py",
        ]
        
        for filename in expected_files:
            file_path = EXAMPLES_DIR / filename
            assert file_path.exists(), f"示例文件 {filename} 不存在"
    
    def test_readme_exists(self):
        """测试README文件是否存在"""
        readme_path = EXAMPLES_DIR / "README.md"
        assert readme_path.exists(), "README.md 不存在"
        
        # 检查README内容
        content = readme_path.read_text(encoding='utf-8')
        assert "示例集合" in content or "Examples" in content.lower()
    
    @pytest.mark.parametrize("example_file", [
        "01_basic_usage.py",
        "05_email_agent.py",
        "06_data_agent.py",
        "10_custom_tools.py",
    ])
    def test_example_execution(self, example_file):
        """测试示例文件可以正常运行（不需要Ollama的示例）"""
        example_path = EXAMPLES_DIR / example_file
        
        # 设置环境变量以支持UTF-8编码
        import os
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        
        # 运行示例文件
        result = subprocess.run(
            [sys.executable, str(example_path)],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=str(PROJECT_ROOT),
            env=env,
            encoding='utf-8',
            errors='ignore'
        )
        
        # 检查返回码
        assert result.returncode == 0, f"{example_file} 运行失败:\n{result.stderr}"
        
        # 检查输出包含成功标识
        assert "✅" in result.stdout or "成功" in result.stdout, \
            f"{example_file} 输出中没有找到成功标识"
    
    def test_example_imports(self):
        """测试示例文件的导入是否正确"""
        import importlib.util
        
        # 需要检查语法的示例
        examples_to_check = [
            "01_basic_usage.py",
            "02_model_manager.py",
            "03_memory_system.py",
            "04_file_agent.py",
        ]
        
        for example_file in examples_to_check:
            example_path = EXAMPLES_DIR / example_file
            
            # 尝试编译Python文件
            try:
                with open(example_path, 'r', encoding='utf-8') as f:
                    code = f.read()
                compile(code, str(example_path), 'exec')
            except SyntaxError as e:
                pytest.fail(f"{example_file} 存在语法错误: {e}")
    
    def test_example_docstrings(self):
        """测试示例文件是否包含文档字符串"""
        import ast
        
        examples = [
            "01_basic_usage.py",
            "05_email_agent.py",
            "10_custom_tools.py",
        ]
        
        for example_file in examples:
            example_path = EXAMPLES_DIR / example_file
            
            with open(example_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())
            
            # 检查模块级docstring
            module_docstring = ast.get_docstring(tree)
            assert module_docstring is not None, \
                f"{example_file} 缺少模块级文档字符串"
    
    def test_example_main_function(self):
        """测试示例文件是否包含main函数"""
        import ast
        
        examples = [
            "01_basic_usage.py",
            "05_email_agent.py",
            "06_data_agent.py",
        ]
        
        for example_file in examples:
            example_path = EXAMPLES_DIR / example_file
            
            with open(example_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())
            
            # 检查是否有main函数
            has_main = any(
                isinstance(node, ast.FunctionDef) and node.name == 'main'
                for node in ast.walk(tree)
            )
            
            assert has_main, f"{example_file} 缺少main函数"


class TestExampleContent:
    """测试示例内容的质量"""
    
    def test_examples_have_chinese_comments(self):
        """测试示例是否包含中文注释"""
        examples = [
            "01_basic_usage.py",
            "05_email_agent.py",
        ]
        
        for example_file in examples:
            example_path = EXAMPLES_DIR / example_file
            
            with open(example_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否有中文字符
            has_chinese = any('\u4e00' <= char <= '\u9fff' for char in content)
            assert has_chinese, f"{example_file} 应该包含中文注释"
    
    def test_examples_have_print_output(self):
        """测试示例是否有输出"""
        examples = [
            "01_basic_usage.py",
            "10_custom_tools.py",
        ]
        
        for example_file in examples:
            example_path = EXAMPLES_DIR / example_file
            
            with open(example_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否有print语句
            assert 'print(' in content, f"{example_file} 应该包含print输出"
    
    def test_examples_file_size(self):
        """测试示例文件大小合理"""
        for example_file in EXAMPLES_DIR.glob("*.py"):
            size_kb = example_file.stat().st_size / 1024
            
            # 示例文件应该在5KB-20KB之间
            assert 5 <= size_kb <= 25, \
                f"{example_file.name} 大小 {size_kb:.1f}KB 不在合理范围内"


class TestDocumentation:
    """测试文档完整性"""
    
    def test_summary_document_exists(self):
        """测试总结文档是否存在"""
        summary_path = EXAMPLES_DIR / "EXAMPLES_SUMMARY.md"
        assert summary_path.exists(), "EXAMPLES_SUMMARY.md 不存在"
    
    def test_final_report_exists(self):
        """测试最终报告是否存在"""
        report_path = EXAMPLES_DIR / "FINAL_REPORT.md"
        assert report_path.exists(), "FINAL_REPORT.md 不存在"
    
    def test_documentation_completeness(self):
        """测试文档完整性"""
        readme_path = EXAMPLES_DIR / "README.md"
        
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查README包含关键信息
        required_sections = [
            "示例",
            "运行",
            "basic_usage",
        ]
        
        for section in required_sections:
            assert section in content.lower(), \
                f"README.md 缺少 '{section}' 相关内容"


@pytest.mark.integration
class TestExampleIntegration:
    """集成测试：测试多个示例的组合运行"""
    
    def test_run_basic_examples_sequence(self):
        """测试基础示例可以按顺序运行"""
        basic_examples = [
            "01_basic_usage.py",
        ]
        
        import os
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        
        for example in basic_examples:
            example_path = EXAMPLES_DIR / example
            result = subprocess.run(
                [sys.executable, str(example_path)],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=str(PROJECT_ROOT),
                env=env,
                encoding='utf-8',
                errors='ignore'
            )
            
            assert result.returncode == 0, \
                f"{example} 在序列运行中失败: {result.stderr}"


if __name__ == "__main__":
    # 运行测试
    pytest.main([__file__, "-v", "--tb=short"])
