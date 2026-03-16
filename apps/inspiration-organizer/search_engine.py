"""搜索引擎 - 基于Whoosh的全文搜索"""
import os
from whoosh import index
from whoosh.fields import Schema, TEXT, KEYWORD, DATETIME, ID, NUMERIC
from whoosh.qparser import QueryParser
from whoosh.analysis import SimpleAnalyzer
from datetime import datetime
from config import Config

class SearchEngine:
    """搜索引擎"""
    
    def __init__(self):
        """初始化搜索引擎"""
        Config.ensure_directories()
        self.index_dir = Config.INDEX_DIR
        self._create_index()
    
    def _create_index(self):
        """创建索引"""
        if not index.exists_in(self.index_dir):
            schema = Schema(
                id=ID(stored=True, unique=True),
                title=TEXT(analyzer=SimpleAnalyzer(), stored=True),
                content=TEXT(analyzer=SimpleAnalyzer(), stored=True),
                keywords=KEYWORD(stored=True),
                content_type=TEXT(stored=True),
                themes=KEYWORD(stored=True),
                file_path=ID(stored=True),
                created_time=DATETIME(stored=True),
                size_kb=NUMERIC(stored=True)
            )
            index.create_in(self.index_dir, schema)
    
    def get_index(self):
        """获取索引"""
        return index.open_dir(self.index_dir)
    
    def add_document(self, doc_id, title, content, keywords, content_type, 
                    themes, file_path, created_time, size_kb):
        """添加文档到索引"""
        try:
            ix = self.get_index()
            writer = ix.writer()
            writer.add_document(
                id=str(doc_id),
                title=title,
                content=content,
                keywords=keywords,
                content_type=content_type,
                themes=themes,
                file_path=file_path,
                created_time=created_time,
                size_kb=size_kb
            )
            writer.commit()
            return True
        except Exception as e:
            print(f"索引添加失败: {e}")
            return False
    
    def update_document(self, doc_id, **kwargs):
        """更新文档索引"""
        try:
            ix = self.get_index()
            writer = ix.writer()
            writer.update_document(
                id=str(doc_id),
                **kwargs
            )
            writer.commit()
            return True
        except Exception as e:
            print(f"索引更新失败: {e}")
            return False
    
    def delete_document(self, doc_id):
        """删除文档索引"""
        try:
            ix = self.get_index()
            writer = ix.writer()
            writer.delete_by_term('id', str(doc_id))
            writer.commit()
            return True
        except Exception as e:
            print(f"索引删除失败: {e}")
            return False
    
    def search(self, query_str, content_type=None, themes=None, 
               min_score=0.3, limit=10):
        """搜索文档"""
        try:
            ix = self.get_index()
            
            with ix.searcher() as searcher:
                parser = QueryParser("content", ix.schema)
                query = parser.parse(query_str)
                
                # 基本搜索
                results = searcher.search(query, limit=limit)
                
                # 过滤结果
                filtered_results = []
                for result in results:
                    score = result.score
                    if score < min_score:
                        continue
                        
                    # 类型过滤
                    if content_type and result['content_type'] != content_type:
                        continue
                        
                    # 主题过滤
                    if themes and result['themes'] not in themes:
                        continue
                        
                    filtered_results.append({
                        'id': result['id'],
                        'title': result['title'],
                        'content': result['content'],
                        'keywords': result['keywords'],
                        'content_type': result['content_type'],
                        'themes': result['themes'],
                        'file_path': result['file_path'],
                        'created_time': result['created_time'],
                        'size_kb': result['size_kb'],
                        'score': score
                    })
                
                return filtered_results
        except Exception as e:
            print(f"搜索失败: {e}")
            return []
    
    def search_by_keyword(self, keyword, content_type=None, limit=10):
        """按关键词搜索"""
        try:
            ix = self.get_index()
            
            with ix.searcher() as searcher:
                query = QueryParser("keywords", ix.schema).parse(keyword)
                results = searcher.search(query, limit=limit)
                
                filtered_results = []
                for result in results:
                    if content_type and result['content_type'] != content_type:
                        continue
                        
                    filtered_results.append({
                        'id': result['id'],
                        'title': result['title'],
                        'content': result['content'],
                        'keywords': result['keywords'],
                        'content_type': result['content_type'],
                        'themes': result['themes'],
                        'file_path': result['file_path'],
                        'created_time': result['created_time'],
                        'size_kb': result['size_kb'],
                        'score': result.score
                    })
                
                return filtered_results
        except Exception as e:
            print(f"关键词搜索失败: {e}")
            return []
    
    def get_statistics(self):
        """获取索引统计信息"""
        try:
            ix = self.get_index()
            with ix.searcher() as searcher:
                doc_count = searcher.doc_count()
                
                type_counts = {}
                theme_counts = {}
                
                for doc in searcher.documents():
                    # 内容类型统计
                    content_type = doc['content_type']
                    type_counts[content_type] = type_counts.get(content_type, 0) + 1
                    
                    # 主题统计
                    themes = doc['themes']
                    if themes:
                        for theme in themes.split(','):
                            theme_counts[theme.strip()] = theme_counts.get(theme.strip(), 0) + 1
                
                return {
                    'total_docs': doc_count,
                    'type_counts': type_counts,
                    'theme_counts': theme_counts
                }
        except Exception as e:
            print(f"统计信息获取失败: {e}")
            return None
