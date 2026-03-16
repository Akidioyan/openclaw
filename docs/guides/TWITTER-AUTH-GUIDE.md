# Twitter 身份验证指南

根据 `xurl` 技能的安全说明，**身份验证过程必须在代理会话之外手动完成**，以确保机密信息的安全性。

## 🚫 禁止在代理会话中执行的操作

- **禁止使用任何包含机密信息的命令**，如 `--bearer-token`、`--consumer-key`、`--consumer-secret`、`--access-token`、`--token-secret`、`--client-id`、`--client-secret`
- **禁止在代理会话中执行身份验证命令**，因为这可能会导致机密信息泄露到 LLM 上下文中
- **禁止使用 `--verbose` 或 `-v` 标志**，因为这会打印包含身份验证信息的详细请求和响应

## ✅ 安全身份验证步骤

### 1. 准备工作

在开始之前，请确保：
1. 你有一个 Twitter/X 开发者账号
2. 你已经创建了一个应用程序（App）
3. 你已经获得了应用程序的凭证（API Key、API Secret Key）

### 2. 身份验证过程

#### 方法一：OAuth 2.0 身份验证（推荐）

**必须在代理会话之外执行**：

```bash
# 1. 注册应用程序（第一次使用时）
xurl auth apps add my-app --consumer-key "YOUR_API_KEY" --consumer-secret "YOUR_API_SECRET_KEY"

# 2. 认证（会打开浏览器进行 OAuth 流程）
xurl auth oauth2

# 3. 检查身份验证状态
xurl auth status

# 4. 验证身份
xurl whoami
```

#### 方法二：OAuth 1.0a 身份验证

**必须在代理会话之外执行**：

```bash
# 1. 注册应用程序
xurl auth apps add my-app --consumer-key "YOUR_API_KEY" --consumer-secret "YOUR_API_SECRET_KEY"

# 2. 认证
xurl auth oauth1
```

### 3. 身份验证成功后的操作

**在代理会话中可以安全执行的操作**：

```bash
# 检查身份验证状态
xurl auth status

# 查看当前用户
xurl whoami

# 发送推文
xurl post "Hello, World!"

# 查看时间线
xurl timeline
```

### 4. 管理多个应用程序

**在代理会话中可以安全执行的操作**：

```bash
# 列出所有已注册的应用程序
xurl auth apps list

# 切换应用程序
xurl auth default my-app

# 使用特定应用程序执行命令
xurl --app my-app whoami
```

## 📝 安全注意事项

### 机密信息安全
- **永远不要**在代理会话中粘贴或输入任何机密信息
- **永远不要**将包含机密信息的文件发送到 LLM 上下文中
- 机密信息（如 API 密钥）应该只存储在你的本地机器上

### 令牌存储
- `xurl` 将令牌存储在 `~/.xurl` 文件中（YAML 格式）
- **永远不要**让 LLM 读取或分析这个文件
- 令牌文件应该由你自己手动管理和保护

### 代理会话限制
在代理会话中，我只能执行**不包含机密信息的操作**：
- 发送没有媒体附件的推文
- 查看公共时间线
- 查看用户信息
- 搜索推文

需要包含机密信息的操作**必须在代理会话之外手动完成**。

## 🔄 恢复身份验证

如果身份验证令牌过期，你可以重新执行：

```bash
xurl auth oauth2
```

## 📱 移动设备注意事项

如果你使用的是移动设备，可能需要在桌面浏览器中完成 OAuth 流程。

## 🆘 故障排除

### 常见问题

1. **身份验证失败**
   - 确保你使用了正确的 API 密钥和 API 密钥密码
   - 检查应用程序的权限设置
   - 确认你没有在代理会话中执行身份验证命令

2. **命令未找到**
   - 确保 `~/.local/bin` 在你的 PATH 中
   - 如果使用的是 macOS Catalina 或更高版本，可能需要更新 `~/.zshrc` 或 `~/.bashrc`

3. **令牌过期**
   - 重新执行身份验证过程
   - 删除旧的令牌文件（`~/.xurl`）并重新开始

---

记住，**安全永远是第一位的**。只有在确保机密信息安全的前提下，我们才能充分利用 Twitter API 的功能。
