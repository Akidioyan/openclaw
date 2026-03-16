#!/usr/bin/env python3
"""
自动整理桌面文件的Python工具
将不同类型的文件分类移动到对应的文件夹中
"""

import os
import shutil
import argparse
from pathlib import Path

# 文件类型与目标文件夹的映射
FILE_TYPE_MAPPING = {
    "图片": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg"],
    "文档": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt"],
    "表格": [".xlsx", ".xls", ".csv", ".ods"],
    "演示": [".pptx", ".ppt", ".odp"],
    "压缩": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "代码": [".py", ".js", ".java", ".cpp", ".c", ".html", ".css", ".json"],
    "音频": [".mp3", ".wav", ".flac", ".m4a"],
    "视频": [".mp4", ".avi", ".mov", ".mkv"],
    "安装": [".dmg", ".pkg", ".exe", ".msi"]
}


def create_folders(base_dir, folders):
    """创建目标文件夹"""
    for folder in folders:
        folder_path = os.path.join(base_dir, folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"创建文件夹: {folder_path}")


def organize_files(source_dir):
    """整理源目录下的文件"""
    # 获取所有目标文件夹名称
    target_folders = list(FILE_TYPE_MAPPING.keys())
    
    # 创建目标文件夹
    create_folders(source_dir, target_folders)
    
    # 遍历源目录下的所有文件
    for filename in os.listdir(source_dir):
        file_path = os.path.join(source_dir, filename)
        
        # 跳过文件夹
        if os.path.isdir(file_path):
            continue
            
        # 获取文件扩展名
        file_ext = os.path.splitext(filename)[1].lower()
        
        # 找到对应的目标文件夹
        target_folder = None
        for folder, extensions in FILE_TYPE_MAPPING.items():
            if file_ext in extensions:
                target_folder = folder
                break
                
        # 移动文件到对应文件夹
        if target_folder:
            target_path = os.path.join(source_dir, target_folder, filename)
            shutil.move(file_path, target_path)
            print(f"移动: {filename} -> {target_folder}")
        else:
            print(f"未分类: {filename} (扩展名: {file_ext})")


def main():
    parser = argparse.ArgumentParser(
        description="自动整理桌面文件的Python工具"
    )
    parser.add_argument(
        "-d", "--dir", 
        default=str(Path.home() / "Desktop"),
        help="要整理的目标目录 (默认: 桌面)"
    )
    
    args = parser.parse_args()
    
    print(f"开始整理目录: {args.dir}")
    organize_files(args.dir)
    print("整理完成!")


if __name__ == "__main__":
    main()
