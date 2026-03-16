#!/usr/bin/env python3
"""检查索引内容"""
import sys
sys.path.append("/Users/aidenyan/openclaw/inspiration-organizer")

from search_engine import SearchEngine

def main():
    search_engine = SearchEngine()
    ix = search_engine.get_index()
    
    print("=== 索引统计信息 ===")
    with ix.searcher() as searcher:
        doc_count = searcher.doc_count()
        print(f"文档总数: {doc_count}")
        
        print("\n=== 所有文档 ===")
        for i, doc in enumerate(searcher.documents()):
            print(f"\n文档 {i+1}:")
            print(f"  ID: {doc['id']}")
            print(f"  标题: {doc['title']}")
            print(f"  内容: {doc['content']}")
            print(f"  类型: {doc['content_type']}")
            print(f"  主题: {doc['themes']}")
            print(f"  关键词: {doc['keywords']}")
            print(f"  文件路径: {doc['file_path']}")

if __name__ == "__main__":
    main()
