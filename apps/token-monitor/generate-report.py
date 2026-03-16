#!/usr/bin/env python3
"""
Token 消耗监控报告生成器
"""

import os
import json
import datetime
import re
import hashlib

# 配置
WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
DATA_DIR = os.path.join(WORKSPACE, "data")
LOG_DIR = os.path.join(WORKSPACE, "log")
TOKEN_MONITOR_DIR = os.path.join(WORKSPACE, "apps", "token-monitor")
CHANNELS_FILE = os.path.join(TOKEN_MONITOR_DIR, "channels.json")
DASHBOARD_FILE = os.path.join(TOKEN_MONITOR_DIR, "dashboard.html")

# 默认频道配置
DEFAULT_CHANNELS = {
    "channels": {
        "akidio001": {
            "name": "大虾咪助手",
            "type": "telegram",
            "icon": "🤖",
            "created": "2026-02-27"
        },
        "akidio002": {
            "name": "作家虾",
            "type": "telegram",
            "icon": "📝",
            "created": "2026-02-27"
        },
        "akidio003": {
            "name": "架构虾",
            "type": "telegram",
            "icon": "🏗️",
            "created": "2026-02-27"
        }
    }
}

def load_channels():
    """加载频道配置"""
    if not os.path.exists(CHANNELS_FILE):
        with open(CHANNELS_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CHANNELS, f, ensure_ascii=False, indent=2)
        print("已创建默认频道配置")
        return DEFAULT_CHANNELS
    
    try:
        with open(CHANNELS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"加载频道配置失败: {e}")
        return DEFAULT_CHANNELS

def find_log_files():
    """查找所有日志文件"""
    log_files = []
    
    # 检查 log 目录
    if os.path.exists(LOG_DIR):
        for filename in os.listdir(LOG_DIR):
            if filename.endswith(".log") or filename.endswith(".json"):
                log_files.append(os.path.join(LOG_DIR, filename))
    
    # 检查 data 目录
    if os.path.exists(DATA_DIR):
        for filename in os.listdir(DATA_DIR):
            if filename.endswith(".log") or filename.endswith(".json"):
                log_files.append(os.path.join(DATA_DIR, filename))
    
    # 检查 memory 目录
    memory_dir = os.path.join(WORKSPACE, "memory")
    if os.path.exists(memory_dir):
        for filename in os.listdir(memory_dir):
            if filename.endswith(".md"):
                log_files.append(os.path.join(memory_dir, filename))
    
    return log_files

def parse_token_usage(log_file):
    """解析单个日志文件的 token 使用情况"""
    usage = {}
    
    try:
        with open(log_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 查找 token 消耗模式 - 支持多种格式
        patterns = [
            r'tokens.*?(\d+)',
            r'(\d+) tokens',
            r'token.*?(\d+)',
            r'(\d+) token'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                try:
                    count = int(match)
                    # 获取文件名的日期信息
                    filename = os.path.basename(log_file)
                    date_str = "unknown"
                    
                    # 尝试从文件名提取日期 (YYYY-MM-DD 格式)
                    date_match = re.search(r'(\d{4}-\d{2}-\d{2})', filename)
                    if date_match:
                        date_str = date_match.group(1)
                    
                    # 尝试从文件名提取会话/频道信息
                    channel_id = "unknown"
                    for known_id in load_channels()["channels"].keys():
                        if known_id in filename:
                            channel_id = known_id
                            break
                    
                    if date_str not in usage:
                        usage[date_str] = {}
                    if channel_id not in usage[date_str]:
                        usage[date_str][channel_id] = 0
                    
                    usage[date_str][channel_id] += count
                    
                except ValueError:
                    continue
        
    except Exception as e:
        print(f"解析文件 {log_file} 失败: {e}")
    
    return usage

def aggregate_usage():
    """汇总所有 token 使用情况"""
    all_usage = {}
    log_files = find_log_files()
    
    print(f"找到 {len(log_files)} 个日志文件")
    
    for log_file in log_files:
        file_usage = parse_token_usage(log_file)
        for date_str, channels in file_usage.items():
            if date_str not in all_usage:
                all_usage[date_str] = {}
            for channel_id, count in channels.items():
                if channel_id not in all_usage[date_str]:
                    all_usage[date_str][channel_id] = 0
                all_usage[date_str][channel_id] += count
    
    return all_usage

def generate_html_report(usage_data, channels_config):
    """生成 HTML 报告"""
    html = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Token 消耗监控仪表盘</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
        }
        
        .header .subtitle {
            font-size: 1.1rem;
            opacity: 0.9;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            padding: 30px;
        }
        
        .stat-card {
            background: #f8f9fa;
            padding: 25px;
            border-radius: 12px;
            border-left: 4px solid #667eea;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        }
        
        .stat-label {
            font-size: 0.9rem;
            color: #666;
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .stat-value {
            font-size: 2.5rem;
            font-weight: bold;
            color: #667eea;
        }
        
        .content {
            padding: 30px;
        }
        
        .section {
            margin-bottom: 40px;
        }
        
        .section-title {
            font-size: 1.5rem;
            color: #333;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #667eea;
        }
        
        .usage-table {
            width: 100%;
            border-collapse: collapse;
            background: white;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .usage-table th,
        .usage-table td {
            padding: 15px;
            text-align: left;
            border-bottom: 1px solid #e0e0e0;
        }
        
        .usage-table th {
            background: #f8f9fa;
            font-weight: 600;
            color: #333;
            text-transform: uppercase;
            font-size: 0.85rem;
            letter-spacing: 0.5px;
        }
        
        .usage-table tr:hover {
            background: #f5f5f5;
        }
        
        .channel-cell {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .channel-icon {
            font-size: 1.5rem;
        }
        
        .channel-name {
            font-weight: 600;
            color: #333;
        }
        
        .channel-type {
            font-size: 0.85rem;
            color: #666;
        }
        
        .token-count {
            text-align: right;
            font-family: 'Courier New', monospace;
            font-size: 1.1rem;
            font-weight: 600;
            color: #667eea;
        }
        
        .date-cell {
            color: #666;
            font-size: 0.9rem;
        }
        
        .footer {
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            font-size: 0.9rem;
        }
        
        .empty-state {
            text-align: center;
            padding: 60px 20px;
            color: #666;
        }
        
        .empty-state .emoji {
            font-size: 4rem;
            margin-bottom: 20px;
            opacity: 0.5;
        }
        
        .chart-container {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        
        @media (max-width: 768px) {
            .header h1 {
                font-size: 2rem;
            }
            
            .stat-value {
                font-size: 2rem;
            }
            
            .stats-grid {
                grid-template-columns: 1fr;
            }
            
            .usage-table {
                font-size: 0.9rem;
            }
            
            .usage-table th,
            .usage-table td {
                padding: 10px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 Token 消耗监控仪表盘</h1>
            <div class="subtitle">实时追踪 OpenClaw 会话的 Token 使用情况</div>
        </div>
"""
    
    # 计算统计数据
    total_tokens = 0
    total_days = len(usage_data)
    channels = load_channels()["channels"]
    channel_usage = {}
    
    for date_str, daily_usage in usage_data.items():
        for channel_id, count in daily_usage.items():
            total_tokens += count
            if channel_id not in channel_usage:
                channel_usage[channel_id] = 0
            channel_usage[channel_id] += count
    
    # 添加统计卡片
    html += """
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-label">总 Token 消耗</div>
                <div class="stat-value">{0:,}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">监控天数</div>
                <div class="stat-value">{1:,}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">活跃频道</div>
                <div class="stat-value">{2:,}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">平均每日消耗</div>
                <div class="stat-value">{3:,}</div>
            </div>
        </div>
    """.format(
        total_tokens,
        total_days,
        len(channel_usage),
        int(total_tokens / total_days) if total_days > 0 else 0
    )
    
    # 添加每日使用详情
    html += """
        <div class="content">
            <div class="section">
                <h2 class="section-title">📊 每日使用详情</h2>
                <table class="usage-table">
                    <thead>
                        <tr>
                            <th>日期</th>
                            <th>频道</th>
                            <th>Token 消耗</th>
                        </tr>
                    </thead>
                    <tbody>
    """
    
    if usage_data:
        for date_str in sorted(usage_data.keys()):
            daily_usage = usage_data[date_str]
            for channel_id, count in daily_usage.items():
                channel_info = channels.get(channel_id, {
                    "name": channel_id,
                    "type": "unknown",
                    "icon": "📺"
                })
                
                html += """
                    <tr>
                        <td class="date-cell">{0}</td>
                        <td>
                            <div class="channel-cell">
                                <span class="channel-icon">{1}</span>
                                <div>
                                    <div class="channel-name">{2}</div>
                                    <div class="channel-type">{3}</div>
                                </div>
                            </div>
                        </td>
                        <td class="token-count">{4:,}</td>
                    </tr>
                """.format(date_str, channel_info["icon"], channel_info["name"], channel_info["type"], count)
    else:
        html += """
            <tr>
                <td colspan="3" class="empty-state">
                    <div class="emoji">📭</div>
                    <div>暂无 Token 使用数据</div>
                    <div style="font-size: 0.9rem; margin-top: 10px;">开始使用 OpenClaw 后，这里会显示详细的 Token 消耗记录</div>
                </td>
            </tr>
        """
    
    html += """
                    </tbody>
                </table>
            </div>
    """
    
    # 添加频道排名
    html += """
            <div class="section">
                <h2 class="section-title">🏆 频道使用排名</h2>
                <table class="usage-table">
                    <thead>
                        <tr>
                            <th>排名</th>
                            <th>频道</th>
                            <th>总 Token 消耗</th>
                            <th>占比</th>
                        </tr>
                    </thead>
                    <tbody>
    """
    
    if channel_usage:
        # 按使用量排序
        sorted_channels = sorted(channel_usage.items(), key=lambda x: x[1], reverse=True)
        for i, (channel_id, count) in enumerate(sorted_channels):
            channel_info = channels.get(channel_id, {
                "name": channel_id,
                "type": "unknown",
                "icon": "📺"
            })
            
            percentage = (count / total_tokens) * 100 if total_tokens > 0 else 0
            
            html += """
                <tr>
                    <td style="text-align: center; font-weight: bold; color: #667eea;">#{0}</td>
                    <td>
                        <div class="channel-cell">
                            <span class="channel-icon">{1}</span>
                            <div>
                                <div class="channel-name">{2}</div>
                                <div class="channel-type">{3}</div>
                            </div>
                        </div>
                    </td>
                    <td class="token-count">{4:,}</td>
                    <td style="text-align: right; font-weight: 600; color: #666;">{5:.1f}%</td>
                </tr>
            """.format(i + 1, channel_info["icon"], channel_info["name"], channel_info["type"], count, percentage)
    else:
        html += """
            <tr>
                <td colspan="4" class="empty-state">
                    <div class="emoji">📭</div>
                    <div>暂无频道使用数据</div>
                </td>
            </tr>
        """
    
    html += """
                    </tbody>
                </table>
            </div>
        </div>
        
        <div class="footer">
            <p>数据更新时间: {} | 数据来源: OpenClaw 日志系统</p>
        </div>
    </div>
</body>
</html>
    """.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    return html

def main():
    """主函数"""
    print("🚀 开始生成 Token 消耗报告...")
    
    # 检查并创建配置文件
    load_channels()
    
    # 聚合使用数据
    usage_data = aggregate_usage()
    
    # 生成 HTML 报告
    html_content = generate_html_report(usage_data, load_channels())
    
    # 保存报告
    with open(DASHBOARD_FILE, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"✅ 报告生成成功!")
    print(f"📊 报告文件: {DASHBOARD_FILE}")
    print(f"🌐 访问地址: http://localhost:18888/dashboard.html")
    print(f"📈 总 Token 消耗: {sum(sum(daily.values()) for daily in usage_data.values())}")
    
    # 启动本地服务器 (后台运行)
    print("\n🚀 启动本地服务器...")
    try:
        import http.server
        import socketserver
        import threading
        
        PORT = 18888
        DIRECTORY = TOKEN_MONITOR_DIR
        
        class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=DIRECTORY, **kwargs)
        
        with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
            server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
            server_thread.start()
            print(f"✅ 服务器正在运行: http://localhost:{PORT}/dashboard.html")
            
    except Exception as e:
        print(f"⚠️ 无法启动服务器: {e}")
        print("❓ 请手动启动服务器:")
        print(f"   cd {TOKEN_MONITOR_DIR}")
        print(f"   python3 -m http.server 18888")
    
    # 显示使用统计
    total_tokens = sum(sum(daily.values()) for daily in usage_data.values())
    print(f"\n📊 报告摘要:")
    print(f"   总 Token 消耗: {total_tokens:,}")
    print(f"   监控天数: {len(usage_data)}")
    print(f"   活跃频道: {len(set(ch for daily in usage_data.values() for ch in daily.keys()))}")
    
    if usage_data:
        average_daily = total_tokens / len(usage_data)
        print(f"   平均每日消耗: {average_daily:.0f}")
    
    return total_tokens

if __name__ == "__main__":
    main()
