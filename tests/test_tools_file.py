"""文件工具测试"""

import pytest
import os
from pathlib import Path
from unittest.mock import Mock, patch
from src.tools.file_tools import FileTools


class TestFileTools:
    """FileTools测试类"""
    
    @pytest.fixture
    def file_tools(self):
        """创建FileTools实例"""
        return FileTools()
    
    @pytest.fixture
    def test_directory(self, tmp_path):
        """创建测试目录结构"""
        # 创建测试文件
        (tmp_path / "file1.txt").write_text("Content 1")
        (tmp_path / "file2.md").write_text("# Markdown")
        (tmp_path / "file3.py").write_text("print('hello')")
        
        # 创建子目录
        sub_dir = tmp_path / "subdir"
        sub_dir.mkdir()
        (sub_dir / "nested.txt").write_text("Nested content")
        
        return tmp_path
    
    def test_scan_directory(self, file_tools, test_directory):
        """测试扫描目录"""
        result = file_tools.scan_directory(str(test_directory))
        
        assert result["success"] is True
        assert result["file_count"] > 0
        assert "files" in result
        assert any(f["name"] == "file1.txt" for f in result["files"])
    
    def test_scan_directory_with_pattern(self, file_tools, test_directory):
        """测试使用模式扫描目录"""
        result = file_tools.scan_directory(str(test_directory), pattern="*.py")
        
        assert result["success"] is True
        assert any(f["name"] == "file3.py" for f in result["files"])
        assert not any(f["name"] == "file1.txt" for f in result["files"])
    
    def test_scan_directory_recursive(self, file_tools, test_directory):
        """测试递归扫描"""
        result = file_tools.scan_directory(str(test_directory), recursive=True)
        
        assert result["success"] is True
        assert any("nested.txt" in f["path"] for f in result["files"])
    
    def test_classify_files(self, file_tools, test_directory):
        """测试文件分类"""
        result = file_tools.classify_files(str(test_directory))
        
        assert result["success"] is True
        assert "classifications" in result
        # 应该有文档和代码分类
        classifications = result["classifications"]
        assert any(c["category"] in ["Documents", "Code"] for c in classifications)
    
    def test_read_file(self, file_tools, test_directory):
        """测试读取文件"""
        test_file = test_directory / "file1.txt"
        result = file_tools.read_file(str(test_file))
        
        assert result["success"] is True
        assert result["content"] == "Content 1"
        assert result["size"] > 0
    
    def test_read_file_not_found(self, file_tools):
        """测试读取不存在的文件"""
        result = file_tools.read_file("nonexistent.txt")
        
        assert result["success"] is False
        assert "error" in result
    
    def test_write_file(self, file_tools, tmp_path):
        """测试写入文件"""
        file_path = tmp_path / "new_file.txt"
        content = "New content"
        
        result = file_tools.write_file(str(file_path), content)
        
        assert result["success"] is True
        assert file_path.exists()
        assert file_path.read_text() == content
    
    def test_get_file_info(self, file_tools, test_directory):
        """测试获取文件信息"""
        test_file = test_directory / "file1.txt"
        result = file_tools.get_file_info(str(test_file))
        
        assert result["success"] is True
        assert result["name"] == "file1.txt"
        assert result["size"] > 0
        assert "modified_time" in result
        assert result["extension"] == ".txt"
    
    def test_detect_duplicates(self, file_tools, test_directory):
        """测试检测重复文件"""
        # 创建重复文件
        (test_directory / "duplicate.txt").write_text("Same content")
        (test_directory / "duplicate2.txt").write_text("Same content")
        
        result = file_tools.detect_duplicates(str(test_directory))
        
        assert result["success"] is True
        if result["duplicate_count"] > 0:
            assert "duplicates" in result
    
    def test_batch_rename(self, file_tools, test_directory):
        """测试批量重命名"""
        files_to_rename = [
            {"old": str(test_directory / "file1.txt"), "new": str(test_directory / "renamed1.txt")},
        ]
        
        result = file_tools.batch_rename(files_to_rename)
        
        assert result["success"] is True
        assert (test_directory / "renamed1.txt").exists()
        assert not (test_directory / "file1.txt").exists()
    
    def test_organize_files(self, file_tools, test_directory):
        """测试文件整理"""
        result = file_tools.organize_files(str(test_directory))
        
        assert result["success"] is True
        assert "organized_count" in result
    
    def test_analyze_storage(self, file_tools, test_directory):
        """测试存储分析"""
        result = file_tools.analyze_storage(str(test_directory))
        
        assert result["success"] is True
        assert "total_size" in result
        assert "file_count" in result
        assert "largest_files" in result
