"""AI分类器 - 使用OpenAI进行智能分类和标签提取"""
import os
import openai
from config import Config
from dotenv import load_dotenv

class AIClassifier:
    """AI分类器"""
    
    def __init__(self):
        """初始化AI分类器"""
        load_dotenv()
        openai.api_key = Config.OPENAI_API_KEY
    
    def classify_theme(self, content, content_type):
        """使用AI识别内容主题"""
        try:
            prompt = f"""
你需要根据提供的内容判断其主题类别。

可选择的主题类别：
- technology（技术）
- design（设计）
- art（艺术）
- life（生活）
- work（工作）

请只返回上述类别名称，不要添加其他解释或内容。

内容类型：{content_type}
内容：{content[:500]}...
            """.strip()
            
            response = openai.ChatCompletion.create(
                model=Config.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "你是一个专业的内容分类器，负责根据内容的主题和含义对其进行分类。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            theme = response.choices[0].message.content.strip().lower()
            
            # 验证主题是否在允许的列表中
            valid_themes = ['technology', 'design', 'art', 'life', 'work']
            return theme if theme in valid_themes else 'work'
            
        except Exception as e:
            print(f"主题分类失败: {e}")
            return 'work'  # 默认返回工作主题
    
    def extract_keywords(self, content, content_type):
        """使用AI提取关键词"""
        try:
            prompt = f"""
请从以下内容中提取最相关的关键词，最多10个。
关键词应该能准确反映内容的主题和核心概念。
返回格式：用逗号分隔的关键词列表。

内容类型：{content_type}
内容：{content[:500]}...
            """.strip()
            
            response = openai.ChatCompletion.create(
                model=Config.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "你是一个专业的关键词提取器，能够准确识别文本内容的核心关键词。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            keywords_str = response.choices[0].message.content.strip()
            keywords = [k.strip() for k in keywords_str.split(',') if k.strip()]
            
            return keywords
            
        except Exception as e:
            print(f"关键词提取失败: {e}")
            return ['未识别']
    
    def generate_title(self, content, content_type):
        """使用AI生成内容标题"""
        try:
            prompt = f"""
请为以下内容生成一个简洁、吸引人的标题。
标题长度应在10-30个字符之间。

内容类型：{content_type}
内容：{content[:500]}...
            """.strip()
            
            response = openai.ChatCompletion.create(
                model=Config.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "你是一个专业的标题生成器，能够为各种类型的内容生成吸引人的标题。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"标题生成失败: {e}")
            return '未命名'
    
    def summarize_content(self, content, content_type):
        """使用AI总结内容"""
        try:
            prompt = f"""
请对以下内容进行简洁的总结，最多100字。
总结应包含内容的核心要点和主要价值。

内容类型：{content_type}
内容：{content[:500]}...
            """.strip()
            
            response = openai.ChatCompletion.create(
                model=Config.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "你是一个专业的内容摘要生成器，能够准确概括内容的核心要点。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"内容总结失败: {e}")
            return '无法总结'
    
    def detect_duplicates(self, content1, content2):
        """使用AI检测内容相似度"""
        try:
            prompt = f"""
请判断以下两个内容的相似度。
返回一个0-1之间的数值，表示相似度（0表示完全不相似，1表示完全相同）。

内容1：{content1[:300]}...
内容2：{content2[:300]}...
            """.strip()
            
            response = openai.ChatCompletion.create(
                model=Config.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "你是一个专业的内容相似度分析器，能够准确评估两个内容之间的相似程度。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            similarity = float(response.choices[0].message.content.strip())
            return max(0, min(1, similarity))
            
        except Exception as e:
            print(f"相似度检测失败: {e}")
            return 0.0
