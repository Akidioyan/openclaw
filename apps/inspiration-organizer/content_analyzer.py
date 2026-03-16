"""内容分析器 - 识别内容类型和主题"""
import os
import mimetypes
import cv2
import librosa
from PIL import Image
from config import Config

class ContentAnalyzer:
    """内容分析器"""
    
    @staticmethod
    def get_content_type(file_path):
        """获取内容类型"""
        # 首先尝试通过文件扩展名判断
        ext = os.path.splitext(file_path)[1].lower()
        
        # 文本类型
        if ext in ['.txt', '.md', '.json', '.yaml', '.yml', '.csv', '.html', '.htm']:
            return 'text'
        
        # 图片类型
        if ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg']:
            return 'image'
        
        # 音频类型
        if ext in ['.mp3', '.wav', '.ogg', '.flac', '.m4a', '.aac']:
            return 'audio'
        
        # 视频类型
        if ext in ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv']:
            return 'video'
        
        # 尝试通过MIME类型判断
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type:
            if mime_type.startswith('text'):
                return 'text'
            if mime_type.startswith('image'):
                return 'image'
            if mime_type.startswith('audio'):
                return 'audio'
            if mime_type.startswith('video'):
                return 'video'
        
        return 'unknown'
    
    @staticmethod
    def analyze_text_content(text):
        """分析文本内容"""
        # TODO: 实现文本分析逻辑
        # 包括关键词提取、主题识别等
        keywords = []
        themes = []
        
        return {
            'keywords': keywords,
            'themes': themes,
            'word_count': len(text.split()),
            'sentence_count': text.count('.') + text.count('!') + text.count('?')
        }
    
    @staticmethod
    def analyze_image_content(image_path):
        """分析图片内容"""
        try:
            with Image.open(image_path) as img:
                width, height = img.size
                format = img.format
                mode = img.mode
                
                # 简单的颜色分析
                pixels = list(img.getdata())
                avg_color = tuple(int(sum(c)/len(pixels)) for c in zip(*pixels))
                
                return {
                    'width': width,
                    'height': height,
                    'format': format,
                    'mode': mode,
                    'avg_color': avg_color,
                    'size_kb': os.path.getsize(image_path) / 1024
                }
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def analyze_audio_content(audio_path):
        """分析音频内容"""
        try:
            y, sr = librosa.load(audio_path)
            
            # 音频特征提取
            duration = librosa.get_duration(y=y, sr=sr)
            tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
            rms = librosa.feature.rms(y=y)
            avg_energy = rms.mean()
            
            return {
                'duration': duration,
                'tempo': tempo,
                'sample_rate': sr,
                'avg_energy': float(avg_energy),
                'size_kb': os.path.getsize(audio_path) / 1024
            }
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def analyze_video_content(video_path):
        """分析视频内容"""
        try:
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                return {'error': '无法打开视频文件'}
            
            # 视频属性
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            duration = frame_count / fps if fps > 0 else 0
            
            cap.release()
            
            return {
                'width': width,
                'height': height,
                'frame_count': frame_count,
                'fps': fps,
                'duration': duration,
                'size_kb': os.path.getsize(video_path) / 1024
            }
        except Exception as e:
            return {'error': str(e)}
