# GitHub Actions 自动爬虫配置

## 功能说明

这个工作流会自动：
1. 每小时运行一次爬虫
2. 爬取苹果ID账号数据
3. 自动提交更新到GitHub仓库

## 配置说明

### 1. 设置API URL（可选）

如果需要在爬取后同步到网站后台，需要设置API URL：

1. 进入GitHub仓库
2. 点击 Settings → Secrets and variables → Actions
3. 点击 New repository secret
4. 名称：`API_URL`
5. 值：你的API地址，例如：`http://your-domain.com/data_sync.php`
6. 点击 Add secret

### 2. 时区说明

工作流使用UTC时间，默认每小时运行一次（`0 * * * *`）。

如果需要调整运行时间，修改 `.github/workflows/crawler.yml` 中的 `cron` 表达式。

**Cron表达式说明：**
- `0 * * * *` - 每小时的第0分钟运行（每小时一次）
- `0 */2 * * *` - 每2小时运行一次
- `0 0 * * *` - 每天0点运行
- `0 0 */6 * *` - 每6小时运行一次

**时区转换：**
- UTC 0点 = 北京时间 8点
- UTC 8点 = 北京时间 16点
- UTC 16点 = 北京时间 0点（次日）

### 3. 手动触发

除了自动运行，你也可以手动触发：
1. 进入GitHub仓库
2. 点击 Actions 标签
3. 选择 "苹果ID爬虫自动运行"
4. 点击 "Run workflow"

## 生成的文件

爬虫运行后会生成以下文件：
- `apple_ids.json` - 完整账号数据
- `api_data.json` - API格式数据（符合网站要求）
- `apple_ids_simple.json` - 简化版数据
- `blog_accounts.json` - 博客用数据（随机2个账号）
- `accounts_simple.json` - 简化版数据

## 注意事项

1. 确保 `requirements.txt` 包含所有依赖
2. 确保 `vpn_ads.json` 文件存在
3. 如果使用API同步，确保设置了 `API_URL` secret
4. GitHub Actions有免费额度限制，注意使用频率

