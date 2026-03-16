"""自动整理器 - 处理内容分类、清理和报告"""
import os
import shutil
import hashlib
import datetime
import pandas as pd
from config import Config
from content_analyzer import ContentAnalyzer
from ai_classifier import AIClassifier
from search_engine import SearchEngine

class ContentOrganizer:
    """内容整理器"""
    
    def __init__(self):
        """初始化整理器"""
        self.analyzer = ContentAnalyzer()
        self.classifier = AIClassifier()
        self.search_engine = SearchEngine()
        self.data_dir = Config.DATA_DIR
        
    def scan_directory(self, directory=None, recursive=True):
        """扫描目录获取内容文件"""
        directory = directory or self.data_dir
        content_files = []
        
        # 处理根目录和子目录
        if recursive:
            for root, dirs, files in os.walk(directory):
                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    content_type = self.analyzer.get_content_type(file_path)
                    
                    if content_type != 'unknown':
                        file_stat = os.stat(file_path)
                        created_time = datetime.datetime.fromtimestamp(file_stat.st_ctime)
                        modified_time = datetime.datetime.fromtimestamp(file_stat.st_mtime)
                        size_kb = file_stat.st_size / 1024
                        
                        content_files.append({
                            'file_path': file_path,
                            'file_name': file_name,
                            'content_type': content_type,
                            'created_time': created_time,
                            'modified_time': modified_time,
                            'size_kb': size_kb
                        })
        else:
            for file_name in os.listdir(directory):
                file_path = os.path.join(directory, file_name)
                if os.path.isfile(file_path):
                    content_type = self.analyzer.get_content_type(file_path)
                    
                    if content_type != 'unknown':
                        file_stat = os.stat(file_path)
                        created_time = datetime.datetime.fromtimestamp(file_stat.st_ctime)
                        modified_time = datetime.datetime.fromtimestamp(file_stat.st_mtime)
                        size_kb = file_stat.st_size / 1024
                        
                        content_files.append({
                            'file_path': file_path,
                            'file_name': file_name,
                            'content_type': content_type,
                            'created_time': created_time,
                            'modified_time': modified_time,
                            'size_kb': size_kb
                        })
                
        return content_files
    
    def process_content(self, file_path, content_type):
        """处理单个内容文件"""
        try:
            # 获取文件元数据
            file_stat = os.stat(file_path)
            created_time = datetime.datetime.fromtimestamp(file_stat.st_ctime)
            size_kb = file_stat.st_size / 1024
            
            # 读取内容
            content = self._read_content(file_path, content_type)
            
            # 分析内容
            analysis_result = self._analyze_content(content, content_type, file_path)
            
            # 分类和标签
            theme = self.classifier.classify_theme(content, content_type)
            keywords = self.classifier.extract_keywords(content, content_type)
            
            # 生成唯一ID
            doc_id = self._generate_doc_id(file_path)
            
            # 添加到索引
            title = os.path.splitext(os.path.basename(file_path))[0]
            self.search_engine.add_document(
                doc_id=doc_id,
                title=title,
                content=content,
                keywords=','.join(keywords),
                content_type=content_type,
                themes=theme,
                file_path=file_path,
                created_time=created_time,
                size_kb=size_kb
            )
            
            return {
                'doc_id': doc_id,
                'file_path': file_path,
                'content_type': content_type,
                'theme': theme,
                'keywords': keywords,
                'analysis': analysis_result,
                'created_time': created_time,
                'size_kb': size_kb,
                'processed': True
            }
            
        except Exception as e:
            print(f"处理内容失败 {file_path}: {e}")
            return {
                'file_path': file_path,
                'content_type': content_type,
                'processed': False,
                'error': str(e)
            }
    
    def _read_content(self, file_path, content_type):
        """读取内容"""
        if content_type == 'text':
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            except:
                try:
                    with open(file_path, 'r', encoding='gbk') as f:
                        return f.read()
                except:
                    return ''
        else:
            return f"[{content_type.upper()} content]"
    
    def _analyze_content(self, content, content_type, file_path):
        """分析内容特征"""
        if content_type == 'text':
            return self.analyzer.analyze_text_content(content)
        elif content_type == 'image':
            return self.analyzer.analyze_image_content(file_path)
        elif content_type == 'audio':
            return self.analyzer.analyze_audio_content(file_path)
        elif content_type == 'video':
            return self.analyzer.analyze_video_content(file_path)
        return {}
    
    def _generate_doc_id(self, file_path):
        """生成唯一文档ID"""
        return hashlib.md5(file_path.encode('utf-8')).hexdigest()
    
    def organize_by_type(self):
        """按内容类型整理文件"""
        for content_type in Config.CONTENT_TYPES:
            type_dir = os.path.join(self.data_dir, content_type)
            os.makedirs(type_dir, exist_ok=True)
        
        for content_file in self.scan_directory():
            src_path = content_file['file_path']
            content_type = content_file['content_type']
            
            if os.path.dirname(src_path) != os.path.join(self.data_dir, content_type):
                dest_dir = os.path.join(self.data_dir, content_type)
                dest_path = os.path.join(dest_dir, os.path.basename(src_path))
                
                if not os.path.exists(dest_path):
                    shutil.move(src_path, dest_path)
                    print(f"移动文件: {src_path} -> {dest_path}")
    
    def organize_by_theme(self):
        """按主题分类整理文件"""
        for theme in Config.THEMES:
            theme_dir = os.path.join(self.data_dir, 'themes', theme)
            os.makedirs(theme_dir, exist_ok=True)
        
        # TODO: 实现主题分类整理逻辑
        pass
    
    def find_duplicates(self):
        """查找重复内容"""
        all_content = self.scan_directory()
        duplicates = []
        
        for i, content1 in enumerate(all_content):
            for j, content2 in enumerate(all_content[i+1:], i+1):
                if content1['content_type'] != content2['content_type']:
                    continue
                
                # 读取内容
                content1_text = self._read_content(content1['file_path'], content1['content_type'])
                content2_text = self._read_content(content2['file_path'], content2['content_type'])
                
                # 检测相似度
                similarity = self.classifier.detect_duplicates(content1_text, content2_text)
                
                if similarity > Config.DUPLICATE_THRESHOLD:
                    duplicates.append({
                        'file1': content1['file_path'],
                        'file2': content2['file_path'],
                        'similarity': similarity,
                        'content_type': content1['content_type']
                    })
        
        return duplicates
    
    def clean_expired_content(self):
        """清理过期内容"""
        today = datetime.datetime.now()
        expired_count = 0
        removed_files = []
        
        for content_file in self.scan_directory():
            created_time = content_file['created_time']
            age_days = (today - created_time).days
            
            if age_days > Config.EXPIRE_DAYS:
                # 删除索引
                doc_id = self._generate_doc_id(content_file['file_path'])
                self.search_engine.delete_document(doc_id)
                
                # 删除文件
                os.remove(content_file['file_path'])
                expired_count += 1
                removed_files.append(content_file['file_path'])
        
        return expired_count, removed_files
    
    def generate_report(self):
        """生成整理报告"""
        report = {
            'summary': {},
            'details': {}
        }
        
        # 内容统计
        all_content = self.scan_directory()
        type_counts = pd.Series([f['content_type'] for f in all_content]).value_counts().to_dict()
        theme_counts = {}
        
        for content_file in all_content:
            doc_id = self._generate_doc_id(content_file['file_path'])
            # TODO: 获取主题信息
            pass
        
        # 索引统计
        index_stats = self.search_engine.get_statistics()
        
        report['summary'] = {
            'total_content': len(all_content),
            'content_types': type_counts,
            'themes': theme_counts,
            'indexed_docs': index_stats.get('total_docs', 0) if index_stats else 0
        }
        
        # 详细信息
        report['details'] = all_content
        
        return report
    
    def save_report(self, report, output_dir=None):
        """保存报告"""
        output_dir = output_dir or os.path.join(Config.BASE_DIR, 'reports')
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = os.path.join(output_dir, f'report_{timestamp}.json')
        
        pd.DataFrame(report['details']).to_json(report_file, orient='records', indent=2, 
                                              date_format='iso')
        
        return report_file
    
    def run_auto_organize(self):
        """运行自动整理流程"""
        print("开始自动整理...")
        
        # 1. 确保目录结构
        Config.ensure_directories()
        
        # 2. 扫描内容
        print("扫描内容...")
        content_files = self.scan_directory()
        print(f"找到 {len(content_files)} 个内容文件")
        
        # 3. 处理内容
        print("处理内容...")
        processed_count = 0
        failed_count = 0
        
        for content_file in content_files:
            result = self.process_content(content_file['file_path'], 
                                         content_file['content_type'])
            
            if result['processed']:
                processed_count += 1
            else:
                failed_count += 1
        
        # 4. 整理文件
        print("整理文件...")
        self.organize_by_type()
        
        # 5. 查找重复
        print("查找重复内容...")
        duplicates = self.find_duplicates()
        print(f"找到 {len(duplicates)} 个重复内容")
        
        # 6. 清理过期
        print("清理过期内容...")
        expired_count, removed_files = self.clean_expired_content()
        print(f"清理了 {expired_count} 个过期内容")
        
        # 7. 生成报告
        print("生成报告...")
        report = self.generate_report()
        report_file = self.save_report(report)
        
        print("自动整理完成!")
        print(f"成功处理: {processed_count}个")
        print(f"失败: {failed_count}个")
        print(f"报告已保存到: {report_file}")
        
        return report
