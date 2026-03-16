#!/usr/bin/env python3
"""调试扫描器"""
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from organizer import ContentOrganizer

organizer = ContentOrganizer()

print("=== 使用ContentOrganizer.scan_directory() ===")
content_files = organizer.scan_directory()
print(f"找到 {len(content_files)} 个内容文件")

for file in content_files:
    print(f"{file['content_type']}: {file['file_path']}")

print("\n=== 直接使用os.walk ===")
for root, dirs, files in os.walk('data'):
    for file_name in files:
        file_path = os.path.join(root, file_name)
        print(f"直接找到: {file_path}")
