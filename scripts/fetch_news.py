#!/usr/bin/env python3
import feedparser
import requests
from datetime import datetime, timedelta
import pytz
import re
import html

# 设置时区
shanghai_tz = pytz.timezone('Asia/Shanghai')
now = datetime.now(shanghai_tz)
yesterday = now - timedelta(days=1)

# RSS源列表
rss_sources = [
    {"name": "Yann LeCun", "url": "https://rsshub.app/twitter/user/ylecun"},
    {"name": "Andrew Ng", "url": "https://rsshub.app/twitter/user/AndrewYNg"},
    {"name": "Andrej Karpathy", "url": "https://rsshub.app/twitter/user/karpathy"},
    {"name": "Jeff Dean", "url": "https://rsshub.app/twitter/user/jeffdean"},
    {"name": "Ilya Sutskever", "url": "https://rsshub.app/twitter/user/ilyasut"},
    {"name": "Fei-Fei Li", "url": "https://rsshub.app/twitter/user/DrFeiFeiLi"},
    {"name": "Shun-Yu Yao", "url": "https://rsshub.app/twitter/user/ShunYuYao"},
    {"name": "OpenAI", "url": "https://rsshub.app/twitter/user/OpenAI"},
    {"name": "DeepMind", "url": "https://rsshub.app/twitter/user/DeepMind"},
    {"name": "Google AI", "url": "https://rsshub.app/twitter/user/googleai"},
    {"name": "Meta AI", "url": "https://rsshub.app/twitter/user/MetaAI"},
    {"name": "Anthropic", "url": "https://rsshub.app/twitter/user/AnthropicAI"},
    {"name": "Hugging Face", "url": "https://rsshub.app/twitter/user/huggingface"},
    {"name": "Stability AI", "url": "https://rsshub.app/twitter/user/StabilityAI"},
    {"name": "Elon Musk", "url": "https://rsshub.app/twitter/user/elonmusk"},
    {"name": "Lex Fridman", "url": "https://rsshub.app/twitter/user/lexfridman"},
    {"name": "Tom Gruber", "url": "https://rsshub.app/twitter/user/TomGruber"},
    {"name": "Gary Marcus", "url": "https://rsshub.app/twitter/user/GaryMarcus"},
    {"name": "Li Chenwu", "url": "https://rsshub.app/twitter/user/lisachenwu"},
    {"name": "TechCrunch", "url": "https://feeds.feedburner.com/TechCrunch"},
    {"name": "The Verge", "url": "https://www.theverge.com/rss/index.xml"},
    {"name": "Ars Technica", "url": "https://feeds.arstechnica.com/arstechnica/index"},
    {"name": "Hacker News", "url": "https://news.ycombinator.com/rss"},
    {"name": "Reddit ML", "url": "https://www.reddit.com/r/MachineLearning/hot.rss"},
    {"name": "DeepLearning.ai", "url": "https://deeplearning.ai/blog/rss.xml"},
    {"name": "Google AI Blog", "url": "https://ai.googleblog.com/feeds/posts/default"},
    {"name": "arXiv AI", "url": "http://export.arxiv.org/rss/cs.AI"}
]

# 代理设置
proxies = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890'
}

# 关键词 - 用于筛选适合普通读者的内容
casual_keywords = [
    'AI impact', 'everyday life', 'ethical', 'ethics', 'for everyone', 'non-technical',
    'future of work', 'education', 'healthcare', 'public perception', 'AI tools',
    'productivity', 'creativity', 'human', 'society', 'discussion', 'opinion',
    'interview', 'podcast', 'debate', 'philosophy', 'policy', 'regulation',
    '日常', '伦理', '教育', '医疗', '工作', '社会', '观点', '讨论'
]

# 过于技术的关键词
technical_keywords = [
    'arxiv', 'paper', 'research', 'neural network', 'transformer', 'gradient',
    'backpropagation', 'optimization', 'benchmark', 'state-of-the-art', 'SOTA',
    'parameter', 'model architecture', 'training', 'inference', 'token',
    'technical report', 'preprint', 'ablation study', 'baseline', 'metric'
]

def is_today(entry):
    """检查文章是否是今天的"""
    if hasattr(entry, 'published_parsed'):
        pub_date = datetime.fromtimestamp(datetime(*entry.published_parsed[:6]).timestamp(), shanghai_tz)
        return pub_date >= yesterday
    elif hasattr(entry, 'updated_parsed'):
        pub_date = datetime.fromtimestamp(datetime(*entry.updated_parsed[:6]).timestamp(), shanghai_tz)
        return pub_date >= yesterday
    return False

def is_casual_content(title, summary):
    """检查内容是否适合普通读者"""
    text = (title + ' ' + summary).lower()
    
    # 排除过于技术的内容
    for keyword in technical_keywords:
        if keyword.lower() in text:
            return False
    
    # 包含适合普通读者的关键词
    for keyword in casual_keywords:
        if keyword.lower() in text:
            return True
    
    return False

def clean_html(text):
    """清理HTML标签"""
    text = html.unescape(text)
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def fetch_feed(source):
    """抓取单个RSS源"""
    try:
        print(f"Fetching {source['name']}...")
        feed = feedparser.parse(source['url'], request_headers={'User-Agent': 'Mozilla/5.0'})
        
        stories = []
        for entry in feed.entries[:10]:  # 只看最新的10条
            if is_today(entry):
                title = clean_html(entry.get('title', ''))
                summary = clean_html(entry.get('summary', ''))
                link = entry.get('link', '')
                
                if is_casual_content(title, summary):
                    stories.append({
                        'title': title,
                        'summary': summary[:200] + '...' if len(summary) > 200 else summary,
                        'link': link,
                        'source': source['name']
                    })
        
        return stories
    except Exception as e:
        print(f"Error fetching {source['name']}: {e}")
        return []

def main():
    all_stories = []
    
    for source in rss_sources:
        stories = fetch_feed(source)
        all_stories.extend(stories)
    
    # 按来源和内容质量排序
    all_stories.sort(key=lambda x: (
        x['source'] in ['Yann LeCun', 'Andrew Ng', 'Andrej Karpathy', 'Elon Musk', 'Gary Marcus'],
        len(x['summary'])
    ), reverse=True)
    
    # 选择前8个故事
    selected_stories = all_stories[:8]
    
    # 格式化输出
    output = f"📱 今日AI/科技精选 - {now.strftime('%Y年%m月%d日')}\n\n"
    
    for i, story in enumerate(selected_stories, 1):
        output += f"📰 **{story['title']}**\n"
        output += f"👤 来源: {story['source']}\n"
        output += f"🔗 {story['link']}\n"
        output += f"📄 {story['summary']}\n\n"
    
    output += "---\n"
    output += "由大虾咪助手自动整理 🦐"
    
    print(output)
    return output

if __name__ == "__main__":
    main()
