#!/usr/bin/env python3
"""基础功能测试"""
import os
import sys
import unittest
import tempfile
import shutil
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config
from content_analyzer import ContentAnalyzer
from ai_classifier import AIClassifier
from search_engine import SearchEngine

class TestBasicFunctions(unittest.TestCase):
    """测试基础功能"""
    
    def setUp(self):
        """设置测试环境"""
        self.analyzer = ContentAnalyzer()
        self.classifier = AIClassifier()
        self.search_engine = SearchEngine()
        
        # 创建临时文件进行测试
        self.temp_dir = tempfile.mkdtemp()
        
        # 创建测试文件
        self.test_text_file = os.path.join(self.temp_dir, 'test.txt')
        with open(self.test_text_file, 'w', encoding='utf-8') as f:
            f.write("这是一个测试文本内容。包含关键词测试和主题分类。")
    
    def tearDown(self):
        """清理测试环境"""
        shutil.rmtree(self.temp_dir)
    
    def test_config(self):
        """测试配置"""
        self.assertTrue(hasattr(Config, 'DATA_DIR'))
        self.assertTrue(hasattr(Config, 'CONTENT_TYPES'))
        self.assertTrue(hasattr(Config, 'THEMES'))
        
        self.assertIn('text', Config.CONTENT_TYPES)
        self.assertIn('image', Config.CONTENT_TYPES)
        self.assertIn('audio', Config.CONTENT_TYPES)
        self.assertIn('video', Config.CONTENT_TYPES)
        
        self.assertIn('technology', Config.THEMES)
        self.assertIn('design', Config.THEMES)
        self.assertIn('art', Config.THEMES)
        self.assertIn('life', Config.THEMES)
        self.assertIn('work', Config.THEMES)
    
    def test_content_analyzer(self):
        """测试内容分析器"""
        # 测试文本文件类型识别
        content_type = self.analyzer.get_content_type(self.test_text_file)
        self.assertEqual(content_type, 'text')
        
        # 测试扩展名判断
        self.assertEqual(self.analyzer.get_content_type('test.jpg'), 'image')
        self.assertEqual(self.analyzer.get_content_type('test.mp3'), 'audio')
        self.assertEqual(self.analyzer.get_content_type('test.mp4'), 'video')
        
        # 测试文本内容分析
        with open(self.test_text_file, 'r', encoding='utf-8') as f:
            text = f.read()
        
        analysis = self.analyzer.analyze_text_content(text)
        self.assertIsInstance(analysis, dict)
        self.assertIn('word_count', analysis)
        self.assertGreater(analysis['word_count'], 0)
    
    def test_search_engine(self):
        """测试搜索引擎"""
        # 测试索引创建
        self.assertTrue(os.path.exists(Config.INDEX_DIR))
        self.assertTrue(os.path.isdir(Config.INDEX_DIR))
        
        # 测试文档添加
        doc_id = 'test-doc-1'
        import datetime
        result = self.search_engine.add_document(
            doc_id=doc_id,
            title='测试文档',
            content='This is a test document for search engine functionality',
            keywords='test,document,search',
            content_type='text',
            themes='technology',
            file_path=self.test_text_file,
            created_time=datetime.datetime.now(),
            size_kb=0.1
        )
        self.assertTrue(result)
        
        # 测试搜索功能
        results = self.search_engine.search('test')
        print(f"搜索结果: {results}")
        
        # 测试文档删除
        result = self.search_engine.delete_document(doc_id)
        self.assertTrue(result)
    
    def test_ai_classifier(self):
        """测试AI分类器"""
        # 测试关键词提取（基础功能）
        text = "人工智能和机器学习的应用"
        keywords = self.classifier.extract_keywords(text, 'text')
        self.assertIsInstance(keywords, list)
        self.assertGreater(len(keywords), 0)
        
        # 测试主题分类（基础功能）
        theme = self.classifier.classify_theme(text, 'text')
        self.assertIn(theme, Config.THEMES)
        
        # 测试标题生成
        title = self.classifier.generate_title(text, 'text')
        self.assertIsInstance(title, str)
        self.assertGreater(len(title), 0)
    
    def test_directory_structure(self):
        """测试目录结构"""
        # 检查数据目录是否存在
        self.assertTrue(os.path.exists(Config.DATA_DIR))
        self.assertTrue(os.path.isdir(Config.DATA_DIR))
        
        # 检查子目录是否存在
        for content_type in Config.CONTENT_TYPES:
            type_dir = os.path.join(Config.DATA_DIR, content_type)
            self.assertTrue(os.path.exists(type_dir))
            self.assertTrue(os.path.isdir(type_dir))
        
        # 检查主题目录是否存在
        theme_base_dir = os.path.join(Config.DATA_DIR, 'themes')
        for theme in Config.THEMES:
            theme_dir = os.path.join(theme_base_dir, theme)
            self.assertTrue(os.path.exists(theme_dir))
            self.assertTrue(os.path.isdir(theme_dir))
        
        # 检查系统目录
        self.assertTrue(os.path.exists(Config.INDEX_DIR))
        self.assertTrue(os.path.exists(Config.LOG_DIR))
        self.assertTrue(os.path.exists(Config.TEMP_DIR))

if __name__ == '__main__':
    unittest.main()
