.PHONY: help install run clean test

# 项目名称
PROJECT_NAME := "Inspiration Organizer"
VERSION := "1.0.0"

help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@echo "  help        - 显示此帮助信息"
	@echo "  install     - 安装项目依赖"
	@echo "  run         - 运行自动整理程序"
	@echo "  scan        - 扫描内容文件"
	@echo "  organize    - 整理内容文件"
	@echo "  clean       - 清理过期内容"
	@echo "  analyze     - 分析内容"
	@echo "  report      - 生成报告"
	@echo "  test        - 运行测试"
	@echo "  init        - 初始化项目结构"
	@echo "  deps        - 检查依赖"

# 安装项目依赖
install:
	@echo "正在安装项目依赖..."
	pip install -r requirements.txt
	python -c "import nltk; nltk.download('punkt'); nltk.download('wordnet'); nltk.download('averaged_perceptron_tagger')"
	@echo "依赖安装完成!"

# 运行自动整理程序
run:
	@echo "正在运行灵感集自动整理系统..."
	python main.py --action auto

# 扫描内容文件
scan:
	@echo "正在扫描内容文件..."
	python main.py --action scan

# 整理内容文件
organize:
	@echo "正在整理内容文件..."
	python main.py --action organize

# 清理过期内容
clean:
	@echo "正在清理过期内容..."
	python main.py --action clean

# 分析内容
analyze:
	@echo "正在分析内容..."
	python main.py --action analyze

# 生成报告
report:
	@echo "正在生成报告..."
	python main.py --action report

# 运行测试
test:
	@echo "正在运行测试..."
	python -m pytest tests/ -v

# 初始化项目结构
init:
	@echo "正在初始化项目结构..."
	mkdir -p data/text data/image data/audio data/video
	mkdir -p data/themes/technology data/themes/design data/themes/art
	mkdir -p data/themes/life data/themes/work
	mkdir -p index logs temp reports
	@echo "项目结构初始化完成!"

# 检查依赖
deps:
	@echo "正在检查项目依赖..."
	python -c "import sys; print(f'Python版本: {sys.version}')"
	pip list | grep -E "(numpy|pandas|nltk|whoosh|Pillow|librosa|opencv|python-dotenv|openai|scikit-learn|torch)"

# 项目信息
info:
	@echo "项目名称: $(PROJECT_NAME)"
	@echo "版本: $(VERSION)"
	@echo "Python版本: $(shell python --version)"
	@echo "数据目录: $(shell python -c "from config import Config; print(Config.DATA_DIR)")"
