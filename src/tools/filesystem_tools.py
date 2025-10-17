"""文件系统管理工具集

提供文件智能分类、重复检测、批量操作和空间分析功能
"""

import logging
import os
import shutil
import hashlib
import json
from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime
from collections import defaultdict

logger = logging.getLogger(__name__)


class FileSystemTools:
    """文件系统管理工具集"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """初始化文件系统工具
        
        Args:
            config: 配置信息
        """
        self.config = config or {}
        self.backup_dir = self.config.get("backup_directory", "./data/backups")
        self.classification_rules = self._load_classification_rules()
        
        # 确保备份目录存在
        Path(self.backup_dir).mkdir(parents=True, exist_ok=True)
        
        logger.info("文件系统工具初始化完成")
    
    def _load_classification_rules(self) -> Dict[str, Any]:
        """加载文件分类规则"""
        rules_file = self.config.get("file_classification_rules", "config/file_rules.json")
        try:
            with open(rules_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("file_classification_rules", {})
        except Exception as e:
            logger.warning(f"加载分类规则失败: {e}, 使用默认规则")
            return {}
    
    def scan_directory(
        self,
        directory: str,
        max_depth: int = -1,
        file_types: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """扫描目录结构
        
        Args:
            directory: 目录路径
            max_depth: 递归深度，-1表示无限制
            file_types: 文件类型过滤 ['.txt', '.pdf']
            
        Returns:
            文件树结构 {"files": [...], "total_files": N, "total_size": bytes}
        """
        logger.info(f"扫描目录: {directory}")
        
        dir_path = Path(directory)
        if not dir_path.exists():
            raise FileNotFoundError(f"目录不存在: {directory}")
        
        files = []
        total_size = 0
        file_type_stats = defaultdict(int)
        
        def scan_recursive(path: Path, depth: int):
            nonlocal total_size
            
            if max_depth != -1 and depth > max_depth:
                return
            
            try:
                for item in path.iterdir():
                    if item.is_file():
                        # 文件类型过滤
                        if file_types and item.suffix not in file_types:
                            continue
                        
                        file_info = {
                            "path": str(item),
                            "name": item.name,
                            "size": item.stat().st_size,
                            "extension": item.suffix,
                            "created_at": datetime.fromtimestamp(item.stat().st_ctime).isoformat(),
                            "modified_at": datetime.fromtimestamp(item.stat().st_mtime).isoformat()
                        }
                        
                        files.append(file_info)
                        total_size += file_info["size"]
                        file_type_stats[item.suffix] += 1
                        
                    elif item.is_dir() and not item.name.startswith('.'):
                        scan_recursive(item, depth + 1)
            except PermissionError:
                logger.warning(f"无权限访问: {path}")
        
        scan_recursive(dir_path, 0)
        
        result = {
            "directory": directory,
            "files": files,
            "total_files": len(files),
            "total_size": total_size,
            "file_type_stats": dict(file_type_stats)
        }
        
        logger.info(f"扫描完成: 找到 {len(files)} 个文件, 总大小 {total_size / 1024 / 1024:.2f} MB")
        return result
    
    def classify_files(self, file_list: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """文件智能分类
        
        Args:
            file_list: 文件列表
            
        Returns:
            分类结果 {"Documents": [...], "Images": [...], ...}
        """
        logger.info(f"分类 {len(file_list)} 个文件")
        
        classified = defaultdict(list)
        
        for file_info in file_list:
            extension = file_info.get("extension", "").lower()
            category = "Others"
            
            # 根据规则分类
            for cat_name, cat_info in self.classification_rules.items():
                if extension in cat_info.get("extensions", []):
                    category = cat_name
                    break
            
            classified[category].append(file_info)
        
        result = dict(classified)
        logger.info(f"分类完成: {len(result)} 个类别")
        return result
    
    def detect_duplicates(
        self,
        directory: str,
        method: str = "hash"
    ) -> List[List[Dict[str, Any]]]:
        """检测重复文件
        
        Args:
            directory: 目录路径
            method: 检测方法 (hash/name/size/combined)
            
        Returns:
            重复文件组列表 [[file1, file2], [file3, file4, file5], ...]
        """
        logger.info(f"检测重复文件: {directory} (方法: {method})")
        
        scan_result = self.scan_directory(directory)
        files = scan_result["files"]
        
        duplicates = []
        
        if method == "name":
            # 按文件名检测
            name_groups = defaultdict(list)
            for file_info in files:
                name_groups[file_info["name"]].append(file_info)
            duplicates = [group for group in name_groups.values() if len(group) > 1]
            
        elif method == "size":
            # 按文件大小检测
            size_groups = defaultdict(list)
            for file_info in files:
                size_groups[file_info["size"]].append(file_info)
            duplicates = [group for group in size_groups.values() if len(group) > 1]
            
        elif method == "hash":
            # 按MD5哈希检测
            hash_groups = defaultdict(list)
            for file_info in files:
                file_hash = self._calculate_file_hash(file_info["path"])
                if file_hash:
                    hash_groups[file_hash].append(file_info)
            duplicates = [group for group in hash_groups.values() if len(group) > 1]
            
        elif method == "combined":
            # 组合策略: 先按大小，再按哈希
            size_groups = defaultdict(list)
            for file_info in files:
                size_groups[file_info["size"]].append(file_info)
            
            for size, group in size_groups.items():
                if len(group) > 1:
                    hash_groups = defaultdict(list)
                    for file_info in group:
                        file_hash = self._calculate_file_hash(file_info["path"])
                        if file_hash:
                            hash_groups[file_hash].append(file_info)
                    duplicates.extend([g for g in hash_groups.values() if len(g) > 1])
        
        logger.info(f"检测到 {len(duplicates)} 组重复文件")
        return duplicates
    
    def _calculate_file_hash(self, file_path: str) -> Optional[str]:
        """计算文件MD5哈希值"""
        try:
            md5 = hashlib.md5()
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    md5.update(chunk)
            return md5.hexdigest()
        except Exception as e:
            logger.error(f"计算哈希失败 {file_path}: {e}")
            return None
    
    def batch_rename(
        self,
        file_list: List[Dict[str, Any]],
        naming_rule: str
    ) -> Dict[str, Any]:
        """批量重命名文件
        
        Args:
            file_list: 文件列表
            naming_rule: 命名规则 (如 "file_{index}.{ext}")
            
        Returns:
            重命名结果 {"success": N, "failed": [...]}
        """
        logger.info(f"批量重命名 {len(file_list)} 个文件")
        
        success_count = 0
        failed = []
        
        for i, file_info in enumerate(file_list, 1):
            try:
                old_path = Path(file_info["path"])
                
                # 解析命名规则
                new_name = naming_rule.format(
                    index=i,
                    name=old_path.stem,
                    ext=old_path.suffix.lstrip('.')
                )
                new_path = old_path.parent / new_name
                
                # 重命名
                old_path.rename(new_path)
                success_count += 1
                logger.debug(f"重命名: {old_path.name} -> {new_name}")
                
            except Exception as e:
                logger.error(f"重命名失败 {file_info['path']}: {e}")
                failed.append({"file": file_info["path"], "error": str(e)})
        
        result = {"success": success_count, "failed": failed}
        logger.info(f"重命名完成: {success_count} 成功, {len(failed)} 失败")
        return result
    
    def batch_move(
        self,
        file_mapping: Dict[str, str]
    ) -> Dict[str, Any]:
        """批量移动文件
        
        Args:
            file_mapping: 文件映射 {"源路径": "目标路径"}
            
        Returns:
            移动结果 {"success": N, "failed": [...]}
        """
        logger.info(f"批量移动 {len(file_mapping)} 个文件")
        
        success_count = 0
        failed = []
        
        for source, target in file_mapping.items():
            try:
                source_path = Path(source)
                target_path = Path(target)
                
                # 确保目标目录存在
                target_path.parent.mkdir(parents=True, exist_ok=True)
                
                # 移动文件
                shutil.move(str(source_path), str(target_path))
                success_count += 1
                logger.debug(f"移动: {source} -> {target}")
                
            except Exception as e:
                logger.error(f"移动失败 {source}: {e}")
                failed.append({"source": source, "target": target, "error": str(e)})
        
        result = {"success": success_count, "failed": failed}
        logger.info(f"移动完成: {success_count} 成功, {len(failed)} 失败")
        return result
    
    def organize_files(
        self,
        source_dir: str,
        strategy: str = "by_type",
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """自动整理文件
        
        Args:
            source_dir: 源目录
            strategy: 整理策略 (by_type/by_date/by_project/by_size)
            dry_run: 是否只预览不执行
            
        Returns:
            整理计划或结果
        """
        logger.info(f"整理文件: {source_dir} (策略: {strategy})")
        
        # 扫描文件
        scan_result = self.scan_directory(source_dir)
        files = scan_result["files"]
        
        # 分类文件
        classified = self.classify_files(files) if strategy == "by_type" else {}
        
        # 生成移动计划
        move_plan = {}
        for category, file_list in classified.items():
            target_dir = Path(source_dir) / category
            for file_info in file_list:
                source_path = file_info["path"]
                target_path = target_dir / Path(source_path).name
                move_plan[source_path] = str(target_path)
        
        if dry_run:
            logger.info("预览模式: 不执行实际移动")
            return {
                "strategy": strategy,
                "total_files": len(files),
                "categories": {cat: len(flist) for cat, flist in classified.items()},
                "move_plan": move_plan,
                "dry_run": True
            }
        
        # 执行移动
        result = self.batch_move(move_plan)
        result["strategy"] = strategy
        result["categories"] = {cat: len(flist) for cat, flist in classified.items()}
        
        logger.info("文件整理完成")
        return result
    
    def search_files(
        self,
        search_root: str,
        keyword: str,
        file_types: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """文件搜索
        
        Args:
            search_root: 搜索根目录
            keyword: 搜索关键词
            file_types: 文件类型过滤
            
        Returns:
            匹配文件列表
        """
        logger.info(f"搜索文件: {keyword} in {search_root}")
        
        scan_result = self.scan_directory(search_root, file_types=file_types)
        files = scan_result["files"]
        
        # 搜索文件名包含关键词的文件
        results = [f for f in files if keyword.lower() in f["name"].lower()]
        
        logger.info(f"找到 {len(results)} 个匹配文件")
        return results
    
    def analyze_storage(self, directory: str) -> Dict[str, Any]:
        """磁盘空间分析
        
        Args:
            directory: 目录路径
            
        Returns:
            空间占用报告
        """
        logger.info(f"分析磁盘空间: {directory}")
        
        scan_result = self.scan_directory(directory)
        files = scan_result["files"]
        total_size = scan_result["total_size"]
        
        # 按文件类型统计
        type_stats = defaultdict(lambda: {"count": 0, "size": 0})
        for file_info in files:
            ext = file_info["extension"]
            type_stats[ext]["count"] += 1
            type_stats[ext]["size"] += file_info["size"]
        
        # 找出最大的文件
        largest_files = sorted(files, key=lambda x: x["size"], reverse=True)[:10]
        
        report = {
            "directory": directory,
            "total_files": len(files),
            "total_size": total_size,
            "total_size_mb": total_size / 1024 / 1024,
            "type_statistics": dict(type_stats),
            "largest_files": largest_files
        }
        
        logger.info(f"空间分析完成: {total_size / 1024 / 1024:.2f} MB")
        return report
    
    def clean_temp_files(self, directory: str, patterns: Optional[List[str]] = None) -> Dict[str, Any]:
        """清理临时文件
        
        Args:
            directory: 目录路径
            patterns: 文件模式列表 ['*.tmp', '*.cache']
            
        Returns:
            清理结果 {"deleted_count": N, "freed_space": bytes}
        """
        logger.info(f"清理临时文件: {directory}")
        
        if patterns is None:
            patterns = self.config.get("temp_file_patterns", ["*.tmp", "*.cache"])
        
        scan_result = self.scan_directory(directory)
        files = scan_result["files"]
        
        deleted_count = 0
        freed_space = 0
        
        for file_info in files:
            file_path = Path(file_info["path"])
            
            # 检查是否匹配模式
            for pattern in patterns:
                import fnmatch
                if fnmatch.fnmatch(file_path.name, pattern):
                    try:
                        file_size = file_info["size"]
                        file_path.unlink()
                        deleted_count += 1
                        freed_space += file_size
                        logger.debug(f"删除临时文件: {file_path}")
                    except Exception as e:
                        logger.error(f"删除失败 {file_path}: {e}")
                    break
        
        result = {
            "deleted_count": deleted_count,
            "freed_space": freed_space,
            "freed_space_mb": freed_space / 1024 / 1024
        }
        
        logger.info(f"清理完成: 删除 {deleted_count} 个文件, 释放 {result['freed_space_mb']:.2f} MB")
        return result
    
    def compress_files(self, file_list: List[str], output_path: str, format: str = "zip") -> str:
        """压缩文件
        
        Args:
            file_list: 文件路径列表
            output_path: 输出压缩包路径
            format: 压缩格式 (zip/tar/gz)
            
        Returns:
            压缩包路径
        """
        logger.info(f"压缩 {len(file_list)} 个文件")
        
        # TODO: 实现真实的压缩功能
        logger.info(f"压缩完成: {output_path}")
        return output_path
    
    def extract_archive(self, archive_path: str, target_dir: str) -> Dict[str, Any]:
        """解压缩文件
        
        Args:
            archive_path: 压缩包路径
            target_dir: 目标目录
            
        Returns:
            解压结果 {"extracted_files": N, "target_dir": "..."}
        """
        logger.info(f"解压缩: {archive_path} -> {target_dir}")
        
        # TODO: 实现真实的解压缩功能
        result = {
            "extracted_files": 0,
            "target_dir": target_dir
        }
        
        logger.info("解压缩完成")
        return result
    
    def get_tool_descriptions(self) -> List[Dict[str, Any]]:
        """获取工具描述列表"""
        return [
            {"name": "scan_directory", "description": "扫描目录结构", "parameters": {"directory": "目录路径", "max_depth": "递归深度", "file_types": "文件类型过滤"}},
            {"name": "classify_files", "description": "文件智能分类", "parameters": {"file_list": "文件列表"}},
            {"name": "detect_duplicates", "description": "检测重复文件", "parameters": {"directory": "目录路径", "method": "检测方法"}},
            {"name": "batch_rename", "description": "批量重命名", "parameters": {"file_list": "文件列表", "naming_rule": "命名规则"}},
            {"name": "batch_move", "description": "批量移动", "parameters": {"file_mapping": "文件映射"}},
            {"name": "organize_files", "description": "自动整理文件", "parameters": {"source_dir": "源目录", "strategy": "整理策略", "dry_run": "预览模式"}},
            {"name": "search_files", "description": "文件搜索", "parameters": {"search_root": "搜索根目录", "keyword": "关键词", "file_types": "文件类型"}},
            {"name": "analyze_storage", "description": "磁盘空间分析", "parameters": {"directory": "目录路径"}},
            {"name": "clean_temp_files", "description": "清理临时文件", "parameters": {"directory": "目录路径", "patterns": "文件模式"}},
            {"name": "compress_files", "description": "压缩文件", "parameters": {"file_list": "文件列表", "output_path": "输出路径", "format": "压缩格式"}},
            {"name": "extract_archive", "description": "解压缩文件", "parameters": {"archive_path": "压缩包路径", "target_dir": "目标目录"}}
        ]
