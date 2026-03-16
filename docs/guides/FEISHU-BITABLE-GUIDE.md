# 飞书多维表格配置指南

## 📊 创建小红书内容管理表格

### 第一步: 创建多维表格

1. 打开飞书,进入"多维表格"
2. 点击"新建多维表格"
3. 命名为: **小红书内容管理**

### 第二步: 配置字段结构

创建以下字段:

| 字段名 | 字段类型 | 说明 |
|--------|----------|------|
| **来源URL** | 文本 | X/Twitter 原始链接 |
| **原标题** | 文本 | 原始标题 |
| **优化后内容** | 多行文本 | AI 优化后的小红书内容 |
| **抓取时间** | 日期时间 | 内容抓取时间 |
| **状态** | 单选 | 待发布/已发布/已失败 |
| **字数** | 数字 | 内容字数统计 |
| **图片链接** | 文本 | 配图 URL(可选) |
| **发布时间** | 日期时间 | 实际发布时间 |
| **互动数据** | 文本 | 点赞/评论/收藏数(可选) |
| **备注** | 多行文本 | 其他说明 |

### 第三步: 配置单选字段选项

**状态字段选项:**
- 🟡 待发布
- 🟢 已发布  
- 🔴 已失败
- 🔵 草稿

### 第四步: 添加 OpenClaw 机器人

1. 点击表格右上角"..."
2. 选择"添加机器人"
3. 搜索你的 OpenClaw 应用名称
4. 给予"可管理"权限

### 第五步: 获取表格 URL

1. 点击表格右上角"分享"
2. 复制链接,格式类似:
   ```
   https://xxx.feishu.cn/base/xxxxx?table=tblxxxx
   ```

---

## 🔧 使用 OpenClaw 操作表格

### 1. 解析表格 URL

```bash
# 在 OpenClaw 中执行
openclaw agent --message "解析这个飞书表格: https://xxx.feishu.cn/base/xxxxx?table=tblxxxx"
```

OpenClaw 会自动调用 `feishu_bitable_get_meta` 工具获取:
- `app_token`: 表格应用 ID
- `table_id`: 数据表 ID

### 2. 查看表格字段

```bash
openclaw agent --message "列出表格字段: app_token=xxx table_id=xxx"
```

### 3. 添加记录

```bash
openclaw agent --message "
在飞书表格中添加一条记录:
- 来源URL: https://x.com/elonmusk/status/123
- 原标题: Tesla 新产品发布
- 优化后内容: 🚗 特斯拉新品来啦!...
- 状态: 待发布
"
```

### 4. 查询记录

```bash
openclaw agent --message "查询飞书表格中状态为'待发布'的记录"
```

### 5. 更新记录状态

```bash
openclaw agent --message "
更新飞书表格记录:
- record_id: recxxxx
- 状态: 已发布
- 发布时间: 2026-02-25 18:00:00
"
```

---

## 🤖 集成到自动化脚本

### 方式 1: 使用脚本 v2.0

```bash
# 带飞书表格的完整流程
~/.openclaw/workspace/x-to-xiaohongshu-v2.sh \
  "https://x.com/username" \
  "https://xxx.feishu.cn/base/xxxxx?table=tblxxxx"
```

### 方式 2: 通过 OpenClaw Agent

在飞书群聊中直接对话:

```
@OpenClaw 帮我从 https://x.com/elonmusk 爬取内容,
优化成小红书风格,并添加到我的内容管理表格中
```

---

## 📈 数据分析视图

### 创建统计视图

1. **发布统计**
   - 按状态分组统计
   - 查看待发布/已发布数量

2. **时间分析**
   - 按抓取时间排序
   - 查看每日内容产出

3. **字数分布**
   - 统计内容字数范围
   - 优化内容长度策略

### 创建筛选器

- 筛选"待发布"内容
- 筛选今日抓取内容
- 筛选特定来源内容

---

## 🔄 完整工作流

```
1. 爬取 X 内容
   ↓
2. AI 优化内容
   ↓
3. 写入飞书表格(状态: 待发布)
   ↓
4. 人工审核(可选)
   ↓
5. 发布到小红书
   ↓
6. 更新表格状态(状态: 已发布)
   ↓
7. 记录互动数据(可选)
```

---

## 💡 高级功能

### 1. 批量导入

创建一个 X 账号列表,批量抓取并存入表格:

```bash
#!/bin/bash
BITABLE_URL="https://xxx.feishu.cn/base/xxxxx?table=tblxxxx"

cat x-accounts.txt | while read url; do
    ~/.openclaw/workspace/x-to-xiaohongshu-v2.sh "$url" "$BITABLE_URL"
    sleep 300  # 间隔 5 分钟
done
```

### 2. 定时同步

使用 OpenClaw cron 定时抓取:

```bash
openclaw cron add \
  --schedule "0 9,15,21 * * *" \
  --command "~/.openclaw/workspace/x-to-xiaohongshu-v2.sh https://x.com/elonmusk https://xxx.feishu.cn/base/xxxxx?table=tblxxxx" \
  --name "定时抓取 Elon Musk 推文"
```

### 3. 数据导出

定期导出表格数据进行分析:

```bash
openclaw agent --message "
导出飞书表格中最近 7 天的所有记录,
生成 CSV 文件用于数据分析
"
```

---

## 🎯 最佳实践

1. **内容审核**: 发布前人工审核"待发布"内容
2. **定时发布**: 避开高峰期,选择最佳发布时间
3. **数据备份**: 定期导出表格数据
4. **标签管理**: 添加"话题标签"字段,统一管理
5. **效果追踪**: 记录互动数据,分析内容表现

---

## 📞 需要帮助?

在 OpenClaw 中问我:
```
"如何配置飞书多维表格?"
"飞书表格字段怎么设置?"
"如何批量导入数据到飞书?"
```

---

**祝你的内容管理更高效! 📊✨**
