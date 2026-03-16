# 微博发布指南

## 目前可用的方法

### 方法一：使用 Clawhub 微博技能（推荐）

Clawhub 有以下微博相关的技能：

1. **weibo-publisher** - 微博发布器（最相关）
2. **weibo-browser-ops** - 微博浏览器操作
3. **weibo-fresh-posts** - 微博时间线监控
4. **weibo-openclaw-ops** - 微博 OpenClaw 操作
5. **weibo** - 微博 CLI 工具

**安装方法：**
```bash
# 安装微博发布器
npx clawhub install weibo-publisher

# 或安装完整的微博工具
npx clawhub install weibo
```

### 方法二：使用浏览器直接访问微博

如果浏览器工具正常，可以直接访问 https://weibo.com 来发布微博。

### 方法三：手动使用浏览器

1. 在 Chrome 或其他浏览器中打开 https://weibo.com
2. 登录你的微博账号
3. 在首页的发布框中输入内容
4. 点击"发布"按钮

## 当前问题

目前浏览器控制服务有问题，无法直接自动化发微博。

## 解决方案建议

### 方案一：等待 Clawhub 速率限制解除
等待一段时间后，再尝试安装 `weibo-publisher` 技能。

### 方案二：直接使用微博网页版
1. 手动在浏览器中打开微博
2. 登录并发布内容
3. 这个方法最直接可靠

### 方案三：创建自定义微博技能
可以开发一个简单的微博发布技能，使用微博开放 API。

## 微博开放 API

微博提供开放 API，可以通过 API 发布内容：
- 开发平台：https://open.weibo.com/
- 需要创建应用并获取 API Key
- 可以使用微博 SDK 或直接调用 API

## 下一步建议

**推荐方案：**
1. 先手动在浏览器中发布微博（方法二）
2. 等待 Clawhub 速率限制解除后安装 `weibo-publisher` 技能
3. 考虑创建自定义微博技能，使用微博开放 API

**快速临时方案：**
如果只是需要快速发一条微博，建议直接手动在浏览器中操作，这是最可靠的方法。
