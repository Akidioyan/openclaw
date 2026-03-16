# OpenClaw 项目导航

## 📁 项目结构概览

我们已经成功重构了项目结构，现在包含以下主要部分：

### 🚀 **应用程序目录** (apps/)
- **inspiration-hub/** - 灵感集应用（主应用）
- **inspiration-organizer/** - 灵感集组织器（已存在的项目）  
- **token-monitor/** - Token监控应用（已存在的项目）
- **StoryBoard-AI/** - 故事板AI（已存在的项目）
- **CodexBar/** - 代码分析工具（已存在的项目）

### 🛠️ **服务层目录** (services/)
- **auto-organize/** - 自动整理服务
- **indexer/** - 索引服务
- **classifier/** - 分类服务  
- **browserwing/** - 浏览器自动化服务（已存在的项目）

### 🔌 **插件目录** (plugins/)
- **custom-feishu/** - 飞书插件
- **telegram-bot/** - Telegram机器人

### 🔄 **共享资源** (shared/)
- **constants/** - 常量定义
- **types/** - 类型定义
- **utils/** - 共享工具
- **configs/** - 共享配置

## 📋 项目管理

### 快速访问

#### 灵感集相关项目
```bash
# 主应用
cd apps/inspiration-hub

# 组织器
cd apps/inspiration-organizer

# 运行组织器
python3 apps/inspiration-organizer/main.py

# 检查索引状态
python3 apps/inspiration-organizer/check_index.py
```

#### 其他应用
```bash
# Token监控
cd apps/token-monitor

# 故事板AI
cd apps/StoryBoard-AI
npm run dev

# 代码分析工具
cd apps/CodexBar
```

#### 服务层
```bash
# 浏览器自动化
cd services/browserwing
npm run start
```

### 📊 运行任务

#### 定时任务管理
```bash
# 查看所有任务
openclaw cron list

# 运行自动整理任务
openclaw cron run auto-organize-index-20260303

# 查看任务状态
openclaw cron status auto-organize-index-20260303
```

#### 服务启动
```bash
# 启动浏览器服务
cd services/browserwing
npm run start

# 启动故事板AI
cd apps/StoryBoard-AI
npm run dev
```

## 🛠️ 开发工具

### 常用命令

#### 代码质量
```bash
# 格式化代码
npm run format

# 检查代码
npm run lint

# 运行测试
npm run test
```

#### 项目维护
```bash
# 清理node_modules
rm -rf apps/*/node_modules
rm -rf services/*/node_modules

# 重新安装依赖
cd apps/inspiration-hub && npm install
cd apps/StoryBoard-AI && npm install
cd services/browserwing && npm install
```

#### 数据管理
```bash
# 备份数据
cp -r apps/inspiration-organizer/data ~/backup/
cp -r apps/inspiration-organizer/index ~/backup/

# 清理缓存
rm -rf apps/inspiration-organizer/.pytest_cache
rm -rf apps/inspiration-organizer/temp
```

## 📈 监控与调试

### 查看日志
```bash
# 查看项目日志
cat apps/inspiration-organizer/logs/app.log

# 查看系统日志
tail -f ~/.openclaw/logs/gateway.log
```

### 性能监控
```bash
# Token监控报告
python3 apps/token-monitor/generate-report.py

# 查看Token使用情况
openclaw cron run token-monitor-update
```

### 调试技巧
```bash
# 调试索引问题
python3 apps/inspiration-organizer/debug_scanner.py

# 测试搜索功能
python3 apps/inspiration-organizer/check_index.py

# 调试AI分类
python3 apps/inspiration-organizer/test_debug.py
```

## 🔗 相关文档

- [项目架构设计](STRUCTURE.md) - 详细的项目结构设计
- [灵感集应用文档](apps/inspiration-hub/README.md) - 主应用文档
- [灵感集组织器文档](apps/inspiration-organizer/README.md) - 组织器项目文档
- [Token监控文档](apps/token-monitor/README.md) - Token监控项目文档
- [记忆系统设计](memory-v2-design.md) - Memory v2.0设计文档

## 📞 支持与帮助

### 常见问题

#### 项目无法启动
```bash
# 检查Node版本
node -v

# 检查依赖
npm ls

# 清除缓存
npm cache clean --force
```

#### 任务运行失败
```bash
# 检查任务状态
openclaw cron status auto-organize-index-20260303

# 检查配置
cat ~/.openclaw/cron/jobs.json
```

#### 数据问题
```bash
# 检查数据目录
ls -la apps/inspiration-organizer/data

# 检查索引目录
ls -la apps/inspiration-organizer/index
```

### 开发资源

- [OpenClaw官方文档](https://docs.openclaw.ai/)
- [MCP协议文档](https://modelcontextprotocol.io/)
- [Node.js文档](https://nodejs.org/en/docs/)
- [Python文档](https://docs.python.org/3/)

---

**🔄 更新时间**：2026年03月03日  
**📝 文档版本**：v1.0  
**👨‍💻 维护者**：OpenClaw Assistant
