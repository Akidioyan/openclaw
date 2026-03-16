# API 调用方式和密钥信息

## 概览

本文档提供了 OpenClaw 中使用的 API 调用方式和密钥信息，供其他机器人配置使用。

## API 调用方式

### Volces Claude Sonnet 4-6 (默认使用)

#### 基本信息
- **提供商**：Volces（火山引擎）
- **模型**：Claude Sonnet 4-6
- **API 类型**：Anthropic Messages API
- **API 端点**：`https://ark.cn-beijing.volces.com/api/coding`
- **认证方式**：API Key

#### 认证信息
```
API Key: 5cf4716d-0135-47a1-8a4f-417ef6943af7
```

#### 请求示例
```bash
curl -X POST https://ark.cn-beijing.volces.com/api/coding/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer 5cf4716d-0135-47a1-8a4f-417ef6943af7" \
  -d '{
    "model": "volces/claude-sonnet-4-6",
    "messages": [
      {
        "role": "user",
        "content": "Hello, world!"
      }
    ],
    "max_tokens": 1000,
    "temperature": 0.7
  }'
```

### Yunyi Claude

#### 基本信息
- **提供商**：Yunyi Claude
- **模型**：Claude 系列（如 Sonnet、Opus、Haiku）
- **API 类型**：Anthropic Messages API
- **API 端点**：`https://yunyi.rdzhvip.com/claude`
- **认证方式**：API Key

#### 认证信息
```
API Key: R09KR3T9-P6MG-FARH-9JTW-3W34298TR345
```

#### 请求示例
```bash
curl -X POST https://yunyi.rdzhvip.com/claude/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer R09KR3T9-P6MG-FARH-9JTW-3W34298TR345" \
  -d '{
    "model": "claude-sonnet-3-5",
    "messages": [
      {
        "role": "user",
        "content": "Hello, world!"
      }
    ],
    "max_tokens": 1000,
    "temperature": 0.7
  }'
```

## 安全注意事项

### 密钥安全
- **不要在公共代码仓库中提交 API 密钥**
- **不要在公共聊天中分享 API 密钥**
- **使用环境变量或密钥管理工具存储**
- **定期轮换 API 密钥**
- **限制 API 密钥的权限范围**

### 使用最佳实践
- **实施请求限制**：限制 API 调用频率，防止过度使用
- **使用 HTTPS**：始终使用加密连接传输数据
- **验证响应**：验证 API 响应的完整性和正确性
- **错误处理**：实现适当的错误处理和重试机制

## OpenClaw 配置

### 在 OpenClaw 中使用

在 `openclaw.json` 配置文件中添加以下内容：

```json
"models": {
  "mode": "merge",
  "providers": {
    "volces": {
      "baseUrl": "https://ark.cn-beijing.volces.com/api/coding",
      "apiKey": "5cf4716d-0135-47a1-8a4f-417ef6943af7",
      "auth": "api-key",
      "api": "anthropic-messages",
      "headers": {},
      "authHeader": false,
      "models": []
    },
    "yunyi-claude": {
      "baseUrl": "https://yunyi.rdzhvip.com/claude",
      "apiKey": "R09KR3T9-P6MG-FARH-9JTW-3W34298TR345",
      "auth": "api-key",
      "api": "anthropic-messages",
      "headers": {},
      "authHeader": false,
      "models": []
    }
  }
}
```

### 使用其他机器人

对于其他支持 Anthropic API 的机器人，配置方法类似，但需要根据具体机器人的要求调整：

#### 1. 在代码中使用
```python
from anthropic import Anthropic

# 使用 Volces API
anthropic = Anthropic(
    base_url="https://ark.cn-beijing.volces.com/api/coding",
    api_key="5cf4716d-0135-47a1-8a4f-417ef6943af7"
)

# 使用 Yunyi API
anthropic = Anthropic(
    base_url="https://yunyi.rdzhvip.com/claude",
    api_key="R09KR3T9-P6MG-FARH-9JTW-3W34298TR345"
)

# 发送请求
response = anthropic.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1000,
    temperature=0.7,
    messages=[
        {"role": "user", "content": "Hello, world!"}
    ]
)
```

#### 2. 在 CLI 工具中使用
```bash
# 使用 Volces API
anthropic-cli --base-url=https://ark.cn-beijing.volces.com/api/coding --api-key=5cf4716d-0135-47a1-8a4f-417ef6943af7

# 使用 Yunyi API
anthropic-cli --base-url=https://yunyi.rdzhvip.com/claude --api-key=R09KR3T9-P6MG-FARH-9JTW-3W34298TR345
```

## 错误处理

### 常见错误
1. **认证失败**：检查 API 密钥是否正确
2. **无效 API 密钥**：重新获取并验证 API 密钥
3. **访问受限**：检查 API 密钥是否已被禁用或过期
4. **请求限制**：检查是否达到 API 调用次数限制
5. **网络错误**：检查网络连接和 API 端点是否可访问

### 调试建议
1. 使用详细的错误信息
2. 实现日志记录和监控
3. 使用调试工具和抓包分析
4. 遵循提供商的错误处理指南

## 监控和使用建议

### 使用限制
- **请求频率**：避免过于频繁的 API 调用
- **最大令牌**：根据任务复杂度设置合理的 `max_tokens`
- **温度参数**：调整 `temperature` 参数控制响应的创造性
- **超时设置**：根据网络条件设置合理的超时时间

### 成本管理
- 了解 API 使用费用和价格结构
- 设置使用限制和预警
- 优化请求内容以减少 token 消耗
- 定期检查和优化 API 使用

## 更新和维护

### API 变更
- 定期检查 API 文档和更新
- 实现向后兼容的请求格式
- 处理 API 端点变更和迁移

### 密钥更新
- 定期轮换 API 密钥
- 及时更新所有相关配置
- 确保密钥更新过程的安全性

---

**最后更新时间**：2026-03-05  
**文档版本**：v1.0
