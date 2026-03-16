#!/usr/bin/env python3
"""
Token 监控频道注册器
"""

import os
import json
import argparse
import datetime
import sys

# 配置
WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
TOKEN_MONITOR_DIR = os.path.join(WORKSPACE, "token-monitor")
CHANNELS_FILE = os.path.join(TOKEN_MONITOR_DIR, "channels.json")

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
        os.makedirs(TOKEN_MONITOR_DIR, exist_ok=True)
        with open(CHANNELS_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CHANNELS, f, ensure_ascii=False, indent=2)
        return DEFAULT_CHANNELS
    
    try:
        with open(CHANNELS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"加载频道配置失败: {e}")
        return DEFAULT_CHANNELS

def save_channels(channels_data):
    """保存频道配置"""
    try:
        with open(CHANNELS_FILE, "w", encoding="utf-8") as f:
            json.dump(channels_data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"保存频道配置失败: {e}")
        return False

def register_channel(channel_id, name, channel_type="telegram", icon="📺"):
    """注册新频道"""
    channels_data = load_channels()
    
    # 检查频道是否已存在
    if channel_id in channels_data["channels"]:
        print(f"⚠️  频道 {channel_id} 已存在")
        return False
    
    # 添加新频道
    channels_data["channels"][channel_id] = {
        "name": name,
        "type": channel_type,
        "icon": icon,
        "created": datetime.date.today().strftime("%Y-%m-%d")
    }
    
    if save_channels(channels_data):
        print(f"✅ 频道 {name} 已成功注册")
        return True
    else:
        return False

def list_channels():
    """列出所有已注册的频道"""
    channels_data = load_channels()
    print(f"📺 已注册频道 ({len(channels_data['channels'])} 个):")
    print("=" * 60)
    
    for channel_id, info in channels_data["channels"].items():
        print(f"  {channel_id}")
        print(f"    名称: {info['name']}")
        print(f"    类型: {info['type']}")
        print(f"    图标: {info['icon']}")
        print(f"    创建: {info['created']}")
        print()

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="Token 监控频道注册器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  1. 注册新频道:
    python3 register-channel.py --id "akidio004" --name "技术交流群" --type "telegram" --icon "💻"
    
  2. 列出所有频道:
    python3 register-channel.py --list
    
  3. 删除频道:
    python3 register-channel.py --delete "akidio004"
        """.strip()
    )
    
    parser.add_argument("--id", help="频道 ID (session key 片段)", metavar="ID")
    parser.add_argument("--name", help="频道显示名称", metavar="NAME")
    parser.add_argument("--type", help="频道类型 (telegram|feishu|cron|other)", 
                       choices=["telegram", "feishu", "cron", "other"],
                       default="telegram", metavar="TYPE")
    parser.add_argument("--icon", help="频道图标 (emoji)", default="📺", metavar="ICON")
    parser.add_argument("--list", help="列出所有已注册的频道", action="store_true")
    parser.add_argument("--delete", help="删除指定频道", metavar="ID")
    
    args = parser.parse_args()
    
    if args.list:
        list_channels()
        return
    
    if args.delete:
        channels_data = load_channels()
        if args.delete in channels_data["channels"]:
            del channels_data["channels"][args.delete]
            if save_channels(channels_data):
                print(f"✅ 频道 {args.delete} 已删除")
            else:
                print(f"❌ 删除频道失败")
        else:
            print(f"⚠️  频道 {args.delete} 不存在")
        return
    
    if args.id and args.name:
        if register_channel(args.id, args.name, args.type, args.icon):
            # 注册成功后更新报告
            print("📊 正在更新报告...")
            try:
                import subprocess
                subprocess.run([
                    sys.executable, 
                    os.path.join(TOKEN_MONITOR_DIR, "generate-report.py")
                ], check=True, capture_output=True, text=True)
                print("✅ 报告已更新")
            except Exception as e:
                print(f"⚠️  无法自动更新报告: {e}")
                print("   请手动运行: python3 generate-report.py")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
