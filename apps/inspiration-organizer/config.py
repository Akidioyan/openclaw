"""配置文件"""
import os

class Config:
    """系统配置"""
    
    # 项目路径
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    INDEX_DIR = os.path.join(BASE_DIR, 'index')
    LOG_DIR = os.path.join(BASE_DIR, 'logs')
    TEMP_DIR = os.path.join(BASE_DIR, 'temp')
    
    # 内容类型
    CONTENT_TYPES = ['text', 'image', 'audio', 'video']
    
    # 主题分类
    THEMES = ['technology', 'design', 'art', 'life', 'work']
    
    # 过期时间（天）
    EXPIRE_DAYS = 7
    
    # OpenAI配置
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    OPENAI_MODEL = 'gpt-3.5-turbo'
    
    # 搜索配置
    SEARCH_RESULTS_PER_PAGE = 10
    SEARCH_MIN_SCORE = 0.3
    
    # 相似度阈值
    DUPLICATE_THRESHOLD = 0.85
    
    # 日志配置
    LOG_LEVEL = 'INFO'
    LOG_MAX_FILES = 7
    
    @classmethod
    def ensure_directories(cls):
        """确保目录存在"""
        for directory in [cls.DATA_DIR, cls.INDEX_DIR, cls.LOG_DIR, cls.TEMP_DIR]:
            os.makedirs(directory, exist_ok=True)
            
        # 确保内容类型子目录存在
        for content_type in cls.CONTENT_TYPES:
            os.makedirs(os.path.join(cls.DATA_DIR, content_type), exist_ok=True)
            
        # 确保主题分类目录存在
        theme_base_dir = os.path.join(cls.DATA_DIR, 'themes')
        for theme in cls.THEMES:
            os.makedirs(os.path.join(theme_base_dir, theme), exist_ok=True)
