# X → 小红书 自动发布工具 使用指南

## 📋 已安装的工具

✅ **playwright-scraper-skill** - 爬取 X/Twitter 内容  
✅ **xiaohongshu-mcp** - 发布到小红书  
✅ **自动化脚本** - `x-to-xiaohongshu.sh`

---

## 🚀 快速开始

### 第一步: 安装依赖

#### 1. Playwright (爬虫工具)
```bash
cd ~/openclaw/skills/playwright-scraper-skill
npm install
npx playwright install chromium
```

#### 2. 小红书 MCP 服务器

下载对应系统的二进制文件:
- macOS (Apple Silicon): [xiaohongshu-mcp-darwin-arm64](https://github.com/xpzouying/xiaohongshu-mcp/releases)
- macOS (Intel): xiaohongshu-mcp-darwin-amd64
- Windows: xiaohongshu-mcp-windows-amd64.exe
- Linux: xiaohongshu-mcp-linux-amd64

```bash
# 下载后赋予执行权限
chmod +x xiaohongshu-mcp-darwin-arm64
chmod +x xiaohongshu-login-darwin-arm64
```

---

### 第二步: 登录小红书

**首次使用需要登录:**

```bash
# 运行登录工具
./xiaohongshu-login-darwin-arm64
```

会打开浏览器显示二维码,用小红书 App 扫码登录。

⚠️ **重要**: 登录后不要在其他浏览器登录同一账号,否则会话会失效!

---

### 第三步: 启动小红书服务器

**在单独的终端窗口运行:**

```bash
# 无头模式(推荐)
./xiaohongshu-mcp-darwin-arm64

# 或显示浏览器(调试用)
./xiaohongshu-mcp-darwin-arm64 -headless=false
```

服务器会在 `http://localhost:18060` 运行。

---

### 第四步: 测试爬取 X 内容

```bash
cd ~/openclaw/skills/playwright-scraper-skill

# 测试爬取 Elon Musk 的推特
node scripts/playwright-stealth.js "https://x.com/elonmusk"
```

---

### 第五步: 测试小红书发布

```bash
cd ~/openclaw/skills/xiaohongshu-mcp

# 检查登录状态
python3 scripts/xhs_client.py status

# 测试发布
python3 scripts/xhs_client.py publish "测试标题" "测试内容" ""
```

---

## 🎯 使用自动化脚本

### 单次发布

```bash
# 爬取指定 X 用户并发布到小红书
~/.openclaw/workspace/x-to-xiaohongshu.sh "https://x.com/username"
```

### 定时发布

使用 OpenClaw 的 cron 功能:

```bash
# 每天早上 9 点自动发布
openclaw cron add \
  --schedule "0 9 * * *" \
  --command "~/.openclaw/workspace/x-to-xiaohongshu.sh https://x.com/elonmusk" \
  --name "X到小红书定时发布"

# 查看定时任务
openclaw cron list

# 删除定时任务
openclaw cron remove <task-id>
```

---

## 📝 高级用法

### 1. 批量发布多个账号

创建一个账号列表文件 `x-accounts.txt`:
```
https://x.com/elonmusk
https://x.com/BillGates
https://x.com/tim_cook
```

批量脚本:
```bash
#!/bin/bash
while read url; do
    echo "处理: $url"
    ~/.openclaw/workspace/x-to-xiaohongshu.sh "$url"
    sleep 300  # 等待 5 分钟避免频率限制
done < x-accounts.txt
```

### 2. 添加图片支持

修改脚本,从 X 内容中提取图片 URL:

```bash
# 提取图片 URL
IMAGES=$(cat "$TEMP_DIR/x-content.json" | python3 -c "
import json, sys
data = json.load(sys.stdin)
# 提取图片逻辑
")

# 发布时带上图片
python3 scripts/xhs_client.py publish "$TITLE" "$CONTENT" "$IMAGES"
```

### 3. 内容过滤和优化

在发布前使用 OpenClaw AI 优化内容:

```bash
# 使用 AI 重写内容,使其更适合小红书风格
OPTIMIZED_CONTENT=$(openclaw agent --message "将以下内容改写成小红书风格: $CONTENT")
```

---

## 🔧 故障排查

### 问题 1: Playwright 爬取失败 (403/blocked)

**解决方案:**
- 使用 stealth 模式 (已默认)
- 增加等待时间: `WAIT_TIME=30000 node scripts/playwright-stealth.js <URL>`
- 显示浏览器调试: `HEADLESS=false node scripts/playwright-stealth.js <URL>`

### 问题 2: 小红书服务器连接失败

**检查清单:**
- [ ] 服务器是否在运行? (`ps aux | grep xiaohongshu-mcp`)
- [ ] 是否已登录? (`python3 scripts/xhs_client.py status`)
- [ ] 端口是否被占用? (`lsof -i :18060`)

### 问题 3: 发布失败

**可能原因:**
- 内容违规 (敏感词、广告等)
- 发布频率过高 (建议间隔 5 分钟以上)
- 会话过期 (重新登录)

---

## 📊 监控和日志

### 查看发布历史

```bash
# 小红书服务器日志
tail -f ~/xiaohongshu-mcp.log

# 脚本执行日志
tail -f /tmp/x-to-xhs-*.log
```

### 统计发布成功率

```bash
# 统计今天的发布次数
grep "发布成功" /tmp/x-to-xhs-*.log | wc -l
```

---

## 🎨 内容优化建议

### 小红书内容特点:
1. **标题**: 吸引眼球,使用 emoji 📱✨
2. **内容**: 分段清晰,多用换行
3. **话题**: 添加相关话题标签 #科技 #AI
4. **图片**: 至少 1 张,最多 9 张
5. **长度**: 50-1000 字为佳

### AI 优化提示词:

```
将以下 Twitter 内容改写成小红书风格:
- 添加合适的 emoji
- 分段清晰
- 语气更亲切
- 添加 2-3 个相关话题标签
- 保持核心信息不变

原文: [X 内容]
```

---

## 📚 相关资源

- [Playwright 文档](https://playwright.dev/)
- [小红书 MCP GitHub](https://github.com/xpzouying/xiaohongshu-mcp)
- [OpenClaw 文档](https://docs.openclaw.ai)
- [Cron 表达式生成器](https://crontab.guru/)

---

## 🆘 需要帮助?

在 OpenClaw 中直接问我:
```
"帮我调试 X 到小红书的发布脚本"
"如何优化小红书内容?"
"定时任务不工作怎么办?"
```

---

**祝你发布顺利! 🎉**
