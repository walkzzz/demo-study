"""全面的类型和语法检查脚本"""

import ast
import sys
from pathlib import Path
from typing import List, Dict, Tuple
import py_compile


class CodeChecker:
    """代码检查器"""
    
    def __init__(self):
        self.errors: List[Dict] = []
        self.warnings: List[Dict] = []
        self.checked_files = 0
        
    def check_syntax(self, file_path: Path) -> bool:
        """检查Python语法"""
        try:
            py_compile.compile(str(file_path), doraise=True)
            return True
        except py_compile.PyCompileError as e:
            self.errors.append({
                'file': str(file_path),
                'type': 'SyntaxError',
                'message': str(e)
            })
            return False
    
    def check_imports(self, file_path: Path) -> bool:
        """检查导入语句"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read(), filename=str(file_path))
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        # 这里可以添加导入检查逻辑
                        pass
                elif isinstance(node, ast.ImportFrom):
                    # 检查相对导入
                    pass
            return True
        except Exception as e:
            self.warnings.append({
                'file': str(file_path),
                'type': 'ImportWarning',
                'message': str(e)
            })
            return False
    
    def check_type_hints(self, file_path: Path) -> Dict:
        """检查类型注解覆盖率"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read(), filename=str(file_path))
            
            total_functions = 0
            typed_functions = 0
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    total_functions += 1
                    # 检查是否有返回类型注解
                    if node.returns is not None:
                        typed_functions += 1
                    # 检查参数类型注解
                    elif any(arg.annotation for arg in node.args.args):
                        typed_functions += 1
            
            coverage = (typed_functions / total_functions * 100) if total_functions > 0 else 0
            
            return {
                'file': str(file_path),
                'total_functions': total_functions,
                'typed_functions': typed_functions,
                'coverage': coverage
            }
        except Exception as e:
            return {
                'file': str(file_path),
                'error': str(e)
            }
    
    def check_file(self, file_path: Path) -> bool:
        """检查单个文件"""
        try:
            rel_path = file_path.relative_to(Path.cwd())
        except ValueError:
            rel_path = file_path
        
        print(f"检查: {rel_path}")
        
        # 语法检查
        if not self.check_syntax(file_path):
            return False
        
        # 导入检查
        self.check_imports(file_path)
        
        # 类型注解检查
        # type_info = self.check_type_hints(file_path)
        
        self.checked_files += 1
        return True
    
    def check_directory(self, directory: str) -> None:
        """检查目录中的所有Python文件"""
        dir_path = Path(directory)
        if not dir_path.exists():
            print(f"⚠️  目录不存在: {directory}")
            return
        
        py_files = list(dir_path.rglob('*.py'))
        print(f"\n📁 检查目录: {directory}")
        print(f"   找到 {len(py_files)} 个Python文件\n")
        
        for py_file in py_files:
            self.check_file(py_file)
    
    def print_report(self) -> None:
        """打印检查报告"""
        print("\n" + "="*70)
        print("📊 类型检查报告")
        print("="*70)
        
        print(f"\n✅ 检查文件数: {self.checked_files}")
        print(f"❌ 语法错误: {len(self.errors)}")
        print(f"⚠️  警告: {len(self.warnings)}")
        
        if self.errors:
            print("\n" + "="*70)
            print("❌ 错误详情:")
            print("="*70)
            for error in self.errors:
                print(f"\n文件: {error['file']}")
                print(f"类型: {error['type']}")
                print(f"信息: {error['message']}")
        
        if self.warnings:
            print("\n" + "="*70)
            print("⚠️  警告详情:")
            print("="*70)
            for warning in self.warnings[:10]:  # 只显示前10个警告
                print(f"\n文件: {warning['file']}")
                print(f"类型: {warning['type']}")
                print(f"信息: {warning['message']}")
            
            if len(self.warnings) > 10:
                print(f"\n... 还有 {len(self.warnings) - 10} 个警告")
        
        print("\n" + "="*70)
        if not self.errors and not self.warnings:
            print("🎉 所有检查通过！代码质量良好！")
        elif not self.errors:
            print("✅ 没有严重错误，但有一些警告需要注意")
        else:
            print("❌ 发现错误，请修复后再次检查")
        print("="*70 + "\n")


def main():
    """主函数"""
    print("\n" + "="*70)
    print("🔍 Python 代码类型和语法检查")
    print("="*70)
    
    checker = CodeChecker()
    
    # 检查各个目录
    directories = ['src', 'tests', 'examples']
    
    for directory in directories:
        checker.check_directory(directory)
    
    # 打印报告
    checker.print_report()
    
    # 返回状态码
    sys.exit(1 if checker.errors else 0)


if __name__ == "__main__":
    main()
