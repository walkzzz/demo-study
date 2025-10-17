"""
示例 04: 文件管理智能体使用
演示如何使用 FileAgent 进行文件整理和管理
"""

import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.tools import FileSystemTools


def example_1_scan_directory():
    """示例1: 扫描目录"""
    print("\n" + "="*60)
    print("📂 示例1: 扫描目录")
    print("="*60)
    
    config = {
        "backup_directory": "./data/backups",
        "file_classification_rules": "config/file_rules.json"
    }
    tools = FileSystemTools(config)
    
    print("\n扫描当前目录...")
    try:
        result = tools.scan_directory(
            directory=".",
            max_depth=1,
            file_types=['.py', '.md', '.yaml', '.json']
        )
        
        print(f"\n✅ 扫描完成:")
        print(f"  📊 文件总数: {result['total_files']}")
        print(f"  💾 总大小: {result['total_size'] / 1024:.2f} KB")
        print(f"\n  📋 文件类型分布:")
        for ext, count in result['file_type_stats'].items():
            print(f"     {ext}: {count} 个")
        
        # 显示部分文件
        print(f"\n  📁 文件列表 (前5个):")
        for file in result['files'][:5]:
            size_kb = file['size'] / 1024
            print(f"     {file['name']} ({size_kb:.2f} KB)")
            
    except Exception as e:
        print(f"❌ 扫描失败: {e}")


def example_2_classify_files():
    """示例2: 文件智能分类"""
    print("\n" + "="*60)
    print("🏷️  示例2: 文件智能分类")
    print("="*60)
    
    config = {
        "backup_directory": "./data/backups",
        "file_classification_rules": "config/file_rules.json"
    }
    tools = FileSystemTools(config)
    
    # 先扫描获取文件列表
    print("\n正在扫描文件...")
    try:
        scan_result = tools.scan_directory(".", max_depth=1)
        files = scan_result['files'][:20]  # 取前20个文件
        
        print(f"获取到 {len(files)} 个文件，开始分类...\n")
        
        # 分类文件
        classified = tools.classify_files(files)
        
        print("✅ 分类完成:")
        for category, file_list in classified.items():
            print(f"\n  📁 {category} ({len(file_list)} 个):")
            for file_info in file_list[:3]:  # 每类显示前3个
                print(f"     - {file_info['name']}")
            if len(file_list) > 3:
                print(f"     ... 还有 {len(file_list) - 3} 个文件")
                
    except Exception as e:
        print(f"❌ 分类失败: {e}")


def example_3_storage_analysis():
    """示例3: 磁盘空间分析"""
    print("\n" + "="*60)
    print("💾 示例3: 磁盘空间分析")
    print("="*60)
    
    config = {
        "backup_directory": "./data/backups",
        "file_classification_rules": "config/file_rules.json"
    }
    tools = FileSystemTools(config)
    
    print("\n分析当前目录磁盘使用情况...")
    try:
        report = tools.analyze_storage(".")
        
        print(f"\n✅ 分析完成:")
        print(f"  📊 文件总数: {report['total_files']}")
        print(f"  💾 总大小: {report['total_size_mb']:.2f} MB")
        
        # 显示最大的文件
        if report['largest_files']:
            print(f"\n  📈 最大的5个文件:")
            for i, file in enumerate(report['largest_files'][:5], 1):
                size_mb = file['size'] / (1024 * 1024)
                print(f"     {i}. {file['name']} ({size_mb:.2f} MB)")
        
        # 按类型统计
        if report['size_by_type']:
            print(f"\n  📊 按类型统计:")
            for ext, size in sorted(report['size_by_type'].items(), 
                                   key=lambda x: x[1], 
                                   reverse=True)[:5]:
                size_mb = size / (1024 * 1024)
                print(f"     {ext}: {size_mb:.2f} MB")
                
    except Exception as e:
        print(f"❌ 分析失败: {e}")


def example_4_find_duplicates():
    """示例4: 查找重复文件"""
    print("\n" + "="*60)
    print("🔍 示例4: 查找重复文件")
    print("="*60)
    
    config = {
        "backup_directory": "./data/backups",
        "file_classification_rules": "config/file_rules.json"
    }
    tools = FileSystemTools(config)
    
    print("\n正在查找重复文件...")
    print("(基于文件大小和内容哈希)")
    
    try:
        # 扫描目录获取文件列表
        scan_result = tools.scan_directory(".")
        files = scan_result['files']
        
        # 按文件大小分组查找可能的重复
        size_groups = {}
        for file in files:
            size = file['size']
            if size not in size_groups:
                size_groups[size] = []
            size_groups[size].append(file['name'])
        
        # 找出大小相同的文件组
        duplicates = {size: files for size, files in size_groups.items() if len(files) > 1}
        
        if duplicates:
            print(f"\n✅ 找到 {len(duplicates)} 组可能重复的文件 (相同大小):")
            for i, (size, file_list) in enumerate(list(duplicates.items())[:3], 1):  # 显示前3组
                print(f"\n  重复组 {i} (大小: {size / 1024:.2f} KB):")
                for file_path in file_list:
                    print(f"     - {file_path}")
        else:
            print("\n✅ 未发现重复文件")
            
    except Exception as e:
        print(f"❌ 查找失败: {e}")


def example_5_organize_workflow():
    """示例5: 完整的文件整理工作流"""
    print("\n" + "="*60)
    print("🔄 示例5: 完整的文件整理工作流")
    print("="*60)
    
    config = {
        "backup_directory": "./data/backups",
        "file_classification_rules": "config/file_rules.json"
    }
    tools = FileSystemTools(config)
    
    target_dir = "./examples"  # 使用examples目录作为示例
    
    print(f"\n整理目标: {target_dir}")
    print("\n步骤:")
    
    # 步骤1: 扫描
    print("\n1️⃣ 扫描目录...")
    try:
        scan_result = tools.scan_directory(target_dir, max_depth=1)
        print(f"   ✅ 找到 {scan_result['total_files']} 个文件")
    except Exception as e:
        print(f"   ❌ 失败: {e}")
        return
    
    # 步骤2: 分析
    print("\n2️⃣ 分析存储...")
    try:
        storage = tools.analyze_storage(target_dir)
        print(f"   ✅ 总大小: {storage['total_size_mb']:.2f} MB")
    except Exception as e:
        print(f"   ❌ 失败: {e}")
    
    # 步骤3: 查找重复
    print("\n3️⃣ 查找重复文件...")
    try:
        # 简单的重复检查逻辑
        files = scan_result['files']
        size_groups = {}
        for file in files:
            size = file['size']
            if size not in size_groups:
                size_groups[size] = []
            size_groups[size].append(file['name'])
        
        duplicates = {size: files for size, files in size_groups.items() if len(files) > 1}
        
        if duplicates:
            print(f"   ⚠️  发现 {len(duplicates)} 组可能重复的文件")
        else:
            print(f"   ✅ 无重复文件")
    except Exception as e:
        print(f"   ❌ 失败: {e}")
    
    # 步骤4: 分类
    print("\n4️⃣ 智能分类...")
    try:
        files = scan_result['files']
        classified = tools.classify_files(files)
        print(f"   ✅ 分为 {len(classified)} 个类别")
        for category, file_list in classified.items():
            print(f"      - {category}: {len(file_list)} 个文件")
    except Exception as e:
        print(f"   ❌ 失败: {e}")
    
    print("\n✅ 整理工作流完成!")
    print("💡 实际整理时会移动文件到对应目录")


def main():
    """主函数"""
    print("\n" + "="*70)
    print("📁 文件管理智能体使用示例")
    print("="*70)
    
    print("\n本示例展示文件系统工具的各种功能")
    print("包括扫描、分类、分析、查找重复等")
    print()
    
    try:
        example_1_scan_directory()
        example_2_classify_files()
        example_3_storage_analysis()
        example_4_find_duplicates()
        example_5_organize_workflow()
        
        print("\n" + "="*70)
        print("✅ 所有示例运行完成!")
        print("="*70)
        
        print("\n💡 功能总结:")
        print("   1. 目录扫描 - 递归扫描文件")
        print("   2. 智能分类 - 基于规则分类文件")
        print("   3. 空间分析 - 统计磁盘使用")
        print("   4. 重复检测 - 基于哈希查找重复")
        print("   5. 完整工作流 - 组合多个功能")
        print()
        
    except Exception as e:
        print(f"\n❌ 运行出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
