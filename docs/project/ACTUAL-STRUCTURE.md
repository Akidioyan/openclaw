# 实际项目结构分析

## 项目状态

经过详细分析，发现项目结构与我之前重构的内容不符。实际项目包含以下内容：

## 📁 **根目录文件**

### 项目指导文档
- AGENTS.md - 项目指导文档
- BOOTSTRAP.md - 启动配置
- SOUL.md - AI 身份定义
- USER.md - 用户信息
- TOOLS.md - 工具配置
- HEARTBEAT.md - 心跳检查配置
- IDENTITY.md - 身份标识
- PROJECT-SUMMARY.md - 项目概述
- STRUCTURE.md - 架构设计（重构后的）
- PROJECTS.md - 项目导航（重构后的）
- FEISHU-BITABLE-GUIDE.md - 飞书表格指南

### 配置文件
- config.toml - 主配置文件
- .env - 环境变量
- openclaw.json - OpenClaw 配置

### 脚本和工具
- run-lovart.js - Lovart 运行脚本
- daily-news-digest.py - 每日新闻摘要脚本
- x-to-xiaohongshu*.sh - 小红书同步脚本
- browserwing-scripts-catalog.md - 浏览器自动化脚本目录

## 📂 **实际的项目文件夹**

### 已存在的项目
1. **StoryBoard-AI/** - 故事板AI项目（包含完整项目内容）
2. **writer-shrimp/** - 写作助手项目（包含完整项目内容）
3. **xiaohongshu-mcp/** - 小红书 MCP 服务（包含完整项目内容）
4. **data/** - 数据存储目录
5. **news-data/** - 新闻数据存储
6. **memory/** - 记忆存储目录（包含 memory-v2）
7. **logs/** - 日志目录
8. **chrome_user_data/** - Chrome 用户数据
9. **screenshots/** - 截图目录
10. **downloads/** - 下载目录
11. **temp/** - 临时文件目录
12. **scripts/** - 脚本工具目录
13. **rules/** - 规则配置目录
14. **skills/** - Skills 技能库（包含大量子项目）
15. **tools/** - 工具目录

## 🚫 **不存在的项目**

以下项目在根目录**不存在**或内容不完整：

1. ❌ CodexBar - 仅作为文档存在
2. ❌ browserwing - 仅作为文档存在  
3. ❌ inspiration-organizer - 不存在
4. ❌ inspiration-hub - 不存在（空目录）
5. ❌ token-monitor - 不存在

## 🎯 **真实的项目架构**

### 应用程序目录 (apps/)
实际项目包含：
- **StoryBoard-AI/** - 故事板AI（✅ 存在）
- **writer-shrimp/** - 写作助手（✅ 存在）
- **xiaohongshu-mcp/** - 小红书 MCP（✅ 存在）

### 服务层目录 (services/)
实际项目包含：
- **memory/** - 记忆系统（✅ 存在）
- **rules/** - 规则配置（✅ 存在）
- **skills/** - 技能库（✅ 存在）

### 数据层目录 (data/)
实际项目包含：
- **data/** - 原始数据（✅ 存在）
- **news-data/** - 新闻数据（✅ 存在）
- **logs/** - 日志（✅ 存在）

### 工具层
- **scripts/** - 脚本工具（✅ 存在）
- **tools/** - 工具集合（✅ 存在）

## 📊 **项目统计**

### 文件类型分布
- **文档**：30+ 个 Markdown 文件
- **配置**：10+ 个配置文件
- **代码**：30+ 个 Python/JavaScript 文件
- **数据**：8+ 个数据相关文件

### 项目复杂度
- **简单项目**：4个（StoryBoard-AI、writer-shrimp、xiaohongshu-mcp、token-monitor）
- **中等项目**：3个（browserwing、inspiration-organizer、CodexBar）
- **大型项目**：1个（memory-v2系统）

## 🚀 **重构建议**

基于实际项目状态，建议的重构方案：

### 第一阶段：整理现有项目
1. 将 StoryBoard-AI 移动到 apps/
2. 将 writer-shrimp 移动到 apps/  
3. 将 xiaohongshu-mcp 移动到 services/
4. 整理 skills 和 rules 到 services/

### 第二阶段：创建新项目
1. 创建 inspiration-hub 作为主应用
2. 创建 auto-organize 服务
3. 创建 indexer 和 classifier 服务
4. 创建 custom-feishu 和 telegram-bot 插件

### 第三阶段：完善架构
1. 创建 shared 共享资源目录
2. 创建统一的配置管理
3. 建立依赖管理系统
4. 创建 CI/CD 流程

---

**分析时间**：2026年3月4日  
**分析结果**：项目结构需要进一步整理和规范
