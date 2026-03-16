# 小红书 MCP 服务器下载指南

## 📥 下载地址

访问 GitHub Releases 页面:
https://github.com/xpzouying/xiaohongshu-mcp/releases

## 🖥️ 根据你的系统选择:

### macOS (Apple Silicon - M1/M2/M3)
- **MCP 服务器**: `xiaohongshu-mcp-darwin-arm64`
- **登录工具**: `xiaohongshu-login-darwin-arm64`

### macOS (Intel)
- **MCP 服务器**: `xiaohongshu-mcp-darwin-amd64`
- **登录工具**: `xiaohongshu-login-darwin-amd64`

### Windows
- **MCP 服务器**: `xiaohongshu-mcp-windows-amd64.exe`
- **登录工具**: `xiaohongshu-login-windows-amd64.exe`

### Linux
- **MCP 服务器**: `xiaohongshu-mcp-linux-amd64`
- **登录工具**: `xiaohongshu-login-linux-amd64`

---

## 📦 安装步骤

### 1. 下载文件

在浏览器中打开上面的 GitHub Releases 链接,下载对应你系统的两个文件。

### 2. 移动到工作目录

```bash
# 创建目录
mkdir -p ~/xiaohongshu-mcp

# 移动下载的文件(假设在 Downloads 目录)
mv ~/Downloads/xiaohongshu-mcp-darwin-arm64 ~/xiaohongshu-mcp/xiaohongshu-mcp
mv ~/Downloads/xiaohongshu-login-darwin-arm64 ~/xiaohongshu-mcp/xiaohongshu-login

# 赋予执行权限
chmod +x ~/xiaohongshu-mcp/xiaohongshu-mcp
chmod +x ~/xiaohongshu-mcp/xiaohongshu-login
```

### 3. 首次登录

```bash
cd ~/xiaohongshu-mcp
./xiaohongshu-login
```

会打开浏览器显示二维码,用小红书 App 扫码登录。

⚠️ **重要**: 登录后不要在其他浏览器登录同一账号!

### 4. 启动服务器

```bash
cd ~/xiaohongshu-mcp

# 无头模式(推荐)
./xiaohongshu-mcp

# 或显示浏览器(调试用)
./xiaohongshu-mcp -headless=false
```

服务器会在 `http://localhost:18060` 运行。

### 5. 测试连接

```bash
cd ~/openclaw/skills/xiaohongshu-mcp
python3 scripts/xhs_client.py status
```

如果显示登录状态,说明配置成功!

---

## 🚀 快速测试

### 测试发布

```bash
cd ~/openclaw/skills/xiaohongshu-mcp
python3 scripts/xhs_client.py publish "测试标题" "测试内容 #测试" ""
```

### 测试搜索

```bash
python3 scripts/xhs_client.py search "咖啡"
```

---

## 🔧 故障排查

### 问题 1: 无法执行文件

```bash
# macOS 可能会提示"无法验证开发者"
# 解决方法:
xattr -d com.apple.quarantine ~/xiaohongshu-mcp/xiaohongshu-mcp
xattr -d com.apple.quarantine ~/xiaohongshu-mcp/xiaohongshu-login
```

### 问题 2: 端口被占用

```bash
# 检查端口
lsof -i :18060

# 杀掉占用进程
kill -9 <PID>
```

### 问题 3: 登录失效

重新运行登录工具:
```bash
cd ~/xiaohongshu-mcp
./xiaohongshu-login
```

---

## ✅ 完成后

服务器启动成功后,就可以运行完整的自动化脚本了:

```bash
~/.openclaw/workspace/x-to-xiaohongshu-v2.sh \
  "https://x.com/username" \
  "飞书表格URL"
```

---

**需要帮助?** 在 OpenClaw 中问我: "小红书 MCP 服务器配置问题"
