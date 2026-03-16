#!/usr/bin/env python3
"""
作家虾风格分析器
分析每个章节的写作风格演进
"""

import re
import json
from pathlib import Path
from collections import Counter

def analyze_chapter(text):
    """分析单个章节的风格特征"""
    
    # 基础统计
    char_count = len(text)
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    para_count = len(paragraphs)
    
    # 对话密度（引号数量）
    dialogue_marks = text.count('"') + text.count('"') + text.count('"')
    dialogue_density = dialogue_marks / char_count * 1000 if char_count > 0 else 0
    
    # 情感词汇
    emotion_words = ['焦虑', '迷茫', '害怕', '担心', '紧张', '不安', '失落', '愧疚', 
                     '温柔', '温暖', '希望', '笑', '哭', '颤抖', '出汗', '心跳']
    emotion_count = sum(text.count(word) for word in emotion_words)
    emotion_density = emotion_count / char_count * 1000 if char_count > 0 else 0
    
    # 细节描写（数字、具体时间、具体金额）
    detail_patterns = [
        r'\d+[块元]',  # 金额
        r'\d+[点时分秒]',  # 时间
        r'\d+[岁年月日]',  # 年龄/日期
        r'\d+[米厘米公里]',  # 距离
    ]
    detail_count = sum(len(re.findall(p, text)) for p in detail_patterns)
    detail_density = detail_count / char_count * 1000 if char_count > 0 else 0
    
    # 短句密度（句号、问号、感叹号）
    sentence_marks = text.count('。') + text.count('？') + text.count('！')
    avg_sentence_length = char_count / sentence_marks if sentence_marks > 0 else 0
    
    # 留白技巧（单独成段的短句）
    short_paras = [p for p in paragraphs if len(p) < 20]
    blank_ratio = len(short_paras) / para_count if para_count > 0 else 0
    
    # 内心独白（"她想"、"他觉得"等）
    inner_patterns = ['想', '觉得', '以为', '知道', '明白', '记得', '忘了']
    inner_count = sum(text.count(f'她{w}') + text.count(f'他{w}') for w in inner_patterns)
    inner_density = inner_count / char_count * 1000 if char_count > 0 else 0
    
    return {
        'char_count': char_count,
        'para_count': para_count,
        'dialogue_density': round(dialogue_density, 2),
        'emotion_density': round(emotion_density, 2),
        'detail_density': round(detail_density, 2),
        'avg_sentence_length': round(avg_sentence_length, 1),
        'blank_ratio': round(blank_ratio * 100, 1),
        'inner_density': round(inner_density, 2),
    }

def compare_chapters(reports_dir):
    """比较所有章节的风格演进"""
    
    reports_path = Path(reports_dir)
    chapters = []
    
    # 读取所有章节
    for chapter_file in sorted(reports_path.glob('chapter-*.md')):
        chapter_num = re.search(r'chapter-(\d+)', chapter_file.name)
        if not chapter_num:
            continue
            
        with open(chapter_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 提取正文（跳过元数据）
        if '## 正文' in content:
            content = content.split('## 正文', 1)[1]
        
        analysis = analyze_chapter(content)
        analysis['chapter'] = int(chapter_num.group(1))
        analysis['file'] = chapter_file.name
        chapters.append(analysis)
    
    return chapters

def generate_report(chapters):
    """生成风格演进报告"""
    
    if not chapters:
        return "没有找到章节文件"
    
    report = ["# 📊 作家虾风格演进分析\n"]
    report.append(f"分析时间：{Path.cwd()}\n")
    report.append(f"章节数量：{len(chapters)}\n")
    report.append("\n## 📈 风格演进趋势\n")
    
    # 表格头
    report.append("| 章节 | 字数 | 对话密度 | 情感密度 | 细节密度 | 平均句长 | 留白% | 内心独白 |")
    report.append("|------|------|----------|----------|----------|----------|-------|----------|")
    
    for ch in chapters:
        report.append(
            f"| 第{ch['chapter']}章 | {ch['char_count']:,} | "
            f"{ch['dialogue_density']} | {ch['emotion_density']} | "
            f"{ch['detail_density']} | {ch['avg_sentence_length']} | "
            f"{ch['blank_ratio']}% | {ch['inner_density']} |"
        )
    
    # 分析演进
    if len(chapters) >= 2:
        report.append("\n## 🎯 关键发现\n")
        
        first = chapters[0]
        latest = chapters[-1]
        
        # 对话密度变化
        dialogue_change = ((latest['dialogue_density'] - first['dialogue_density']) 
                          / first['dialogue_density'] * 100 if first['dialogue_density'] > 0 else 0)
        report.append(f"**对话密度**：{'增加' if dialogue_change > 0 else '减少'} {abs(dialogue_change):.1f}%")
        
        # 情感密度变化
        emotion_change = ((latest['emotion_density'] - first['emotion_density']) 
                         / first['emotion_density'] * 100 if first['emotion_density'] > 0 else 0)
        report.append(f"**情感密度**：{'增加' if emotion_change > 0 else '减少'} {abs(emotion_change):.1f}%")
        
        # 细节密度变化
        detail_change = ((latest['detail_density'] - first['detail_density']) 
                        / first['detail_density'] * 100 if first['detail_density'] > 0 else 0)
        report.append(f"**细节密度**：{'增加' if detail_change > 0 else '减少'} {abs(detail_change):.1f}%")
        
        # 留白技巧
        blank_change = latest['blank_ratio'] - first['blank_ratio']
        report.append(f"**留白技巧**：{'增加' if blank_change > 0 else '减少'} {abs(blank_change):.1f}%")
        
        # 内心独白
        inner_change = ((latest['inner_density'] - first['inner_density']) 
                       / first['inner_density'] * 100 if first['inner_density'] > 0 else 0)
        report.append(f"**内心独白**：{'增加' if inner_change > 0 else '减少'} {abs(inner_change):.1f}%")
    
    report.append("\n## 💡 风格特征\n")
    
    avg_dialogue = sum(ch['dialogue_density'] for ch in chapters) / len(chapters)
    avg_emotion = sum(ch['emotion_density'] for ch in chapters) / len(chapters)
    avg_blank = sum(ch['blank_ratio'] for ch in chapters) / len(chapters)
    
    if avg_dialogue > 15:
        report.append("- ✅ **对话丰富**：善用对话推动情节")
    else:
        report.append("- 📝 **叙事为主**：以叙述和描写为主")
    
    if avg_emotion > 3:
        report.append("- ❤️ **情感充沛**：情感词汇密度高")
    else:
        report.append("- 🎭 **克制内敛**：情感表达克制")
    
    if avg_blank > 15:
        report.append("- 🎨 **留白艺术**：善用短句和段落留白")
    else:
        report.append("- 📖 **连贯叙事**：段落饱满连贯")
    
    report.append("\n---\n")
    report.append("*数据说明：密度指标为每千字出现次数*")
    
    return '\n'.join(report)

if __name__ == '__main__':
    import sys
    
    reports_dir = sys.argv[1] if len(sys.argv) > 1 else './project-001-ai-predictions/reports'
    
    chapters = compare_chapters(reports_dir)
    report = generate_report(chapters)
    
    print(report)
    
    # 保存报告
    output_file = Path(reports_dir).parent / 'style-evolution.md'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✅ 报告已保存：{output_file}")
