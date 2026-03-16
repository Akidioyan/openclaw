#!/usr/bin/env python3
"""灵感集自动整理和索引系统主程序"""
import os
import sys
import argparse
import logging
from dotenv import load_dotenv
from config import Config
from organizer import ContentOrganizer

def setup_logging():
    """配置日志系统"""
    log_dir = Config.LOG_DIR
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, f"inspiration_organizer_{Config.LOG_LEVEL.lower()}.log")
    
    logging.basicConfig(
        level=getattr(logging, Config.LOG_LEVEL),
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)

def main():
    """主程序"""
    # 加载环境变量
    load_dotenv()
    
    # 初始化配置
    Config.ensure_directories()
    
    # 设置日志
    logger = setup_logging()
    
    # 解析命令行参数
    parser = argparse.ArgumentParser(
        description='灵感集自动整理和索引系统'
    )
    
    parser.add_argument('--action', '-a', 
                      choices=['scan', 'organize', 'clean', 'analyze', 'report', 'auto'],
                      default='auto',
                      help='操作类型: scan(扫描), organize(整理), clean(清理), analyze(分析), report(报告), auto(自动)')
    
    parser.add_argument('--directory', '-d',
                      help='指定目录路径（默认: data目录）')
    
    parser.add_argument('--recursive', '-r',
                      action='store_true',
                      default=True,
                      help='递归扫描子目录（默认: True）')
    
    parser.add_argument('--expire-days', type=int,
                      default=Config.EXPIRE_DAYS,
                      help='过期天数（默认: 7天）')
    
    args = parser.parse_args()
    
    # 创建整理器实例
    organizer = ContentOrganizer()
    
    logger.info(f"开始执行操作: {args.action}")
    
    try:
        if args.action == 'auto':
            # 自动模式 - 执行完整流程
            logger.info("进入自动整理模式")
            report = organizer.run_auto_organize()
            
            logger.info(f"整理完成! 总内容数: {report['summary']['total_content']}")
            
        elif args.action == 'scan':
            # 扫描模式
            logger.info(f"扫描目录: {args.directory or Config.DATA_DIR}")
            content_files = organizer.scan_directory(args.directory, args.recursive)
            
            logger.info(f"找到 {len(content_files)} 个内容文件")
            
            for content_file in content_files:
                logger.info(f"{content_file['content_type']}: {content_file['file_path']}")
                
        elif args.action == 'organize':
            # 整理模式
            logger.info("开始整理内容")
            organizer.organize_by_type()
            organizer.organize_by_theme()
            logger.info("整理完成")
            
        elif args.action == 'clean':
            # 清理模式
            logger.info(f"清理 {args.expire_days} 天前的过期内容")
            expired_count, removed_files = organizer.clean_expired_content()
            
            logger.info(f"清理完成! 共删除 {expired_count} 个文件")
            for file_path in removed_files:
                logger.warning(f"已删除: {file_path}")
                
        elif args.action == 'analyze':
            # 分析模式
            logger.info("开始分析内容")
            
            if not args.directory:
                # 分析所有内容
                content_files = organizer.scan_directory()
                logger.info(f"分析 {len(content_files)} 个文件")
                
                for content_file in content_files:
                    result = organizer.process_content(content_file['file_path'], 
                                                    content_file['content_type'])
                    
                    if result['processed']:
                        logger.info(f"处理成功: {result['doc_id']} - {content_file['file_path']}")
                    else:
                        logger.error(f"处理失败: {content_file['file_path']} - {result['error']}")
                        
        elif args.action == 'report':
            # 报告模式
            logger.info("生成整理报告")
            report = organizer.generate_report()
            report_file = organizer.save_report(report)
            
            logger.info(f"报告已保存到: {report_file}")
            logger.info(f"总内容数: {report['summary']['total_content']}")
            logger.info(f"内容类型分布: {report['summary']['content_types']}")
            
        else:
            parser.print_help()
            
    except Exception as e:
        logger.error(f"操作失败: {e}")
        return 1
        
    logger.info("操作完成")
    return 0

if __name__ == "__main__":
    sys.exit(main())
