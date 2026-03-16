#!/usr/bin/env python3
"""调试脚本"""
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from content_analyzer import ContentAnalyzer

# 测试文件路径
test_files = [
    'data/text/tech-example.txt',
    'data/text/design-example.txt',
    'data/text/art-example.txt'
]

print("=== 调试 get_content_type 方法 ===")

for file_path in test_files:
    if os.path.exists(file_path):
        print(f"检查文件: {file_path}")
        content_type = ContentAnalyzer.get_content_type(file_path)
        print(f"文件类型: {content_type}")
        
        # 打印文件详细信息
        ext = os.path.splitext(file_path)[1]
        print(f"扩展名: {ext}")
        
        print()

# 打印目录结构
print("=== 目录结构 ===")
for root, dirs, files in os.walk('data'):
    print(f"目录: {root}")
    for file in files:
        print(f"  文件: {file}")
