"""
主执行脚本 - 爬取并同步到网站后台和GitHub
"""

from apple_id_crawler import AppleIDCrawler
from github_sync import GitHubSync
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """主函数"""
    logger.info("=" * 60)
    logger.info("苹果ID爬虫系统启动")
    logger.info("=" * 60)
    
    # 配置API URL（从环境变量或配置文件读取）
    api_url = os.environ.get('API_URL') or os.environ.get('WEBSITE_API_URL')
    # 例如: "http://your-domain.com/data_sync.php"
    
    # 步骤1: 爬取数据
    logger.info("\n[步骤1] 开始爬取苹果ID账号...")
    crawler = AppleIDCrawler(api_url=api_url)
    accounts = crawler.crawl()
    
    if not accounts:
        logger.error("未爬取到账号数据，终止执行")
        return
    
    # 保存本地数据
    crawler.save_to_json('apple_ids.json')
    crawler.save_to_simple_json('apple_ids_simple.json')
    
    logger.info(f"成功爬取 {len(accounts)} 个账号")
    
    # 步骤2: 同步到网站后台API
    if api_url:
        logger.info("\n[步骤2] 开始同步到网站后台...")
        if crawler.sync_to_api():
            logger.info("✅ 网站后台同步成功！")
        else:
            logger.warning("⚠️ 网站后台同步失败，请检查API配置")
    else:
        logger.warning("⚠️ 未配置API URL，跳过网站后台同步")
        logger.info("提示: 设置环境变量 API_URL 或 WEBSITE_API_URL 来启用自动同步")
    
    # 步骤3: 生成GitHub文件（供博客使用）
    # 注意：在GitHub Actions中，文件提交由workflow处理
    logger.info("\n[步骤3] 生成GitHub文件...")
    sync = GitHubSync()
    # 只生成文件，不执行git操作（GitHub Actions会处理提交）
    if os.environ.get('GITHUB_ACTIONS'):
        # 在GitHub Actions中，只生成文件
        accounts = sync.load_accounts('apple_ids.json')
        if accounts:
            sync.create_api_file(accounts, 'api_data.json')
            sync.create_blog_file(accounts, 'blog_accounts.json')
            sync.create_simple_file(accounts, 'accounts_simple.json')
            logger.info("✅ 文件已生成，将由GitHub Actions自动提交")
    else:
        # 本地运行，执行完整的同步
        sync.sync()
    
    logger.info("\n" + "=" * 60)
    logger.info("所有任务完成！")
    logger.info("=" * 60)


if __name__ == '__main__':
    main()
