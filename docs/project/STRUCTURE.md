# OpenClaw 项目结构

## 应用程序目录 (apps/)

### 1. StoryBoard-AI/
- 位置: apps/StoryBoard-AI/
- 类型: AI 分镜工具
- 内容: 包含大量子项目
- 文件类型: *.js, *.ts, *.md, *.json

### 2. writer-shrimp/
- 位置: apps/writer-shrimp/
- 类型: 写作助手项目
- 内容: 包含项目配置和脚本
- 文件类型: *.md, *.json, *.sh, *.py

### 3. inspiration-organizer/
- 位置: apps/inspiration-organizer/
- 类型: 灵感集组织器
- 内容: 包含项目代码和数据
- 文件类型: *.py, *.md, *.json

### 4. token-monitor/
- 位置: apps/token-monitor/
- 类型: Token 监控项目
- 内容: 包含项目代码和配置
- 文件类型: *.js, *.ts, *.md, *.json

### 5. CodexBar/
- 位置: apps/CodexBar/
- 类型: 菜单栏应用
- 内容: 包含大量子项目
- 文件类型: *.js, *.ts, *.md, *.json

### 6. inspiration-hub/
- 位置: apps/inspiration-hub/
- 类型: 灵感集应用
- 内容: 包含项目骨架
- 文件类型: 空目录

## 服务目录 (services/)

### 1. browserwing/
- 位置: services/browserwing/
- 类型: 浏览器自动化服务
- 内容: 包含浏览器操作相关代码
- 文件类型: *.js, *.ts, *.go, *.tsx

### 2. xiaohongshu-mcp/
- 位置: services/xiaohongshu-mcp/
- 类型: 小红书 MCP 服务
- 内容: 包含小红书 API 接口
- 文件类型: *.js, *.ts, *.json

### 3. xiaohongshu-login/
- 位置: services/xiaohongshu-login/
- 类型: 小红书登录服务
- 内容: 包含登录相关代码
- 文件类型: *.js, *.ts, *.json

### 4. auto-organize/
- 位置: services/auto-organize/
- 类型: 自动整理服务
- 内容: 包含自动整理功能
- 文件类型: *.js, *.ts, *.json

### 5. indexer/
- 位置: services/indexer/
- 类型: 索引服务
- 内容: 包含内容索引功能
- 文件类型: *.js, *.ts, *.json

### 6. classifier/
- 位置: services/classifier/
- 类型: 分类服务
- 内容: 包含内容分类功能
- 文件类型: *.js, *.ts, *.json

## 插件目录 (plugins/)

### 1. custom-feishu/
- 位置: plugins/custom-feishu/
- 类型: 飞书插件
- 内容: 包含飞书相关功能
- 文件类型: *.js, *.ts, *.json

### 2. telegram-bot/
- 位置: plugins/telegram-bot/
- 类型: Telegram 机器人
- 内容: 包含 Telegram 相关功能
- 文件类型: *.js, *.ts, *.json

## 共享资源目录 (shared/)

### 1. constants/
- 位置: shared/constants/
- 类型: 常量定义
- 内容: 包含项目常量
- 文件类型: *.js, *.ts, *.json

### 2. types/
- 位置: shared/types/
- 类型: 类型定义
- 内容: 包含项目类型
- 文件类型: *.js, *.ts, *.json

### 3. utils/
- 位置: shared/utils/
- 类型: 共享工具
- 内容: 包含项目工具函数
- 文件类型: *.js, *.ts, *.json

### 4. configs/
- 位置: shared/configs/
- 类型: 共享配置
- 内容: 包含项目配置
- 文件类型: *.js, *.ts, *.json

## 其他目录

### skills/
- 位置: skills/
- 类型: Skills 技能库
- 内容: 包含大量技能定义
- 文件数量: 4000+ 文件

### memory/
- 位置: memory/
- 类型: 记忆存储
- 内容: 包含记忆相关功能
- 文件类型: *.md, *.jsonl

### rules/
- 位置: rules/
- 类型: 规则配置
- 内容: 包含项目规则
- 文件类型: *.mdc, *.json

### scripts/
- 位置: scripts/
- 类型: 脚本工具
- 内容: 包含项目脚本
- 文件类型: *.sh, *.py, *.js

### data/
- 位置: data/
- 类型: 数据存储
- 内容: 包含项目数据
- 文件类型: *.txt, *.json, *.csv

### logs/
- 位置: logs/
- 类型: 日志存储
- 内容: 包含项目日志
- 文件类型: *.log, *.txt

### downloads/
- 位置: downloads/
- 类型: 下载存储
- 内容: 包含下载文件
- 文件类型: 各种文件

### temp/
- 位置: temp/
- 类型: 临时存储
- 内容: 包含临时文件
- 文件类型: 各种文件

## 根目录文件

### 配置文件
- config.toml: 主配置文件
- .env: 环境变量配置
- openclaw.json: 系统配置

### 文档文件
- AGENTS.md: 项目指导文档
- BOOTSTRAP.md: 启动配置
- SOUL.md: AI 身份定义
- USER.md: 用户信息
- TOOLS.md: 工具配置
- HEARTBEAT.md: 心跳检查配置
- IDENTITY.md: 身份标识
- PROJECT-SUMMARY.md: 项目概述
- FEISHU-BITABLE-GUIDE.md: 飞书表格指南
- X-TO-XIAOHONGSHU-GUIDE.md: 小红书同步指南
- XIAOHONGSHU-MCP-INSTALL.md: MCP 安装指南
- short-drama-workflow.md: 短剧工作流程
- skills-analysis-2026-03-02.md: 技能分析

### 其他文件
- browserwing-scripts-catalog.md: 浏览器脚本目录
- run-lovart.js: Lovart 运行脚本
- daily-news-digest.py: 每日新闻摘要脚本
- x-to-xiaohongshu.sh: 小红书同步脚本
- x-to-xiaohongshu-v2.sh: 小红书同步脚本 v2
- voice-conversation-workflow.md: 语音对话流程

