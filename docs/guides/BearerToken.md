# Bearer Token 身份验证方法

## 方法一：使用 Bearer Token 进行身份验证

如果 OAuth2 流程在当前环境下无法工作，您可以尝试使用 Bearer Token 进行身份验证。

### 1. 获取 Bearer Token

**您需要从 Twitter/X 开发者平台获取 Bearer Token：**

1. 访问 https://developer.x.com/en/portal/dashboard
2. 找到您的应用程序
3. 在 "Keys and tokens" 页面找到 "Bearer Token"
4. 复制该 Bearer Token

### 2. 存储 Bearer Token

**在代理会话之外执行以下命令：**

```bash
cat > ~/.xurl << EOF
---
version: 1
apps:
  openclaw:
    name: openclaw
    client_id: dummy
    client_secret: dummy
    tokens:
      - type: bearer
        token: YOUR_BEARER_TOKEN_HERE
EOF
```

**注意**：请替换 `YOUR_BEARER_TOKEN_HERE` 为您的实际 Bearer Token。

### 3. 验证身份

**在代理会话之外执行：**

```bash
xurl whoami
```

## 方法二：使用 OAuth 1.0a 身份验证

如果 OAuth2 无法工作，您可以尝试 OAuth 1.0a 身份验证：

### 1. 注册应用程序

```bash
xurl auth apps add openclaw --consumer-key "YOUR_CONSUMER_KEY" --consumer-secret "YOUR_CONSUMER_SECRET"
```

### 2. 身份验证

```bash
xurl auth oauth1
```

## 方法三：使用 Application Only 身份验证

如果您只需要读取数据，可以使用应用程序身份验证：

```bash
xurl auth oauth2 --app-only
```

## 🚫 安全警告

**永远不要在代理会话中输入或显示您的 Bearer Token！**

## 🆘 故障排除

如果您遇到身份验证问题，请：

1. 确认您的应用程序配置是否正确
2. 检查 `~/.xurl` 文件的内容
3. 尝试重新注册应用程序
4. 使用其他身份验证方法

## 📱 替代方法

如果所有方法都无法工作，您可以尝试使用其他 Twitter CLI 工具，如：

1. `t` - Twitter CLI（https://github.com/sferik/t）
2. `twurl` - Twitter URL 工具（https://github.com/twitter/twurl）
3. `twitter-api-v2` - Node.js 库

## 🔄 恢复身份验证

如果您的身份验证信息已失效：

1. 删除 `~/.xurl` 文件
2. 重新开始身份验证过程
3. 确保使用正确的身份验证方法
