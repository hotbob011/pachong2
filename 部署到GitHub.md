# 部署到GitHub并设置自动运行

## 📋 部署步骤

### 1. 准备文件

确保以下文件都在仓库中：

**必需文件：**
- ✅ `apple_id_crawler.py` - 核心爬虫
- ✅ `main.py` - 主执行脚本
- ✅ `github_sync.py` - GitHub同步（可选）
- ✅ `vpn_ads.json` - VPN广告数据
- ✅ `requirements.txt` - Python依赖
- ✅ `.github/workflows/crawler.yml` - GitHub Actions工作流

**可选文件：**
- `simple_test.py` - 测试脚本
- `scheduler.py` - 本地定时任务（服务器上不需要）

### 2. 创建GitHub仓库

1. 在GitHub上创建新仓库（或使用现有仓库）
2. 将代码推送到仓库

```bash
git init
git add .
git commit -m "初始提交：苹果ID爬虫"
git branch -M main
git remote add origin https://github.com/你的用户名/仓库名.git
git push -u origin main
```

### 3. 配置GitHub Actions

#### 方法1：使用提供的配置文件（推荐）

1. 确保 `.github/workflows/crawler.yml` 文件已上传
2. GitHub会自动识别并启用工作流

#### 方法2：手动创建

1. 在GitHub仓库中，点击 "Actions" 标签
2. 点击 "set up a workflow yourself"
3. 复制 `.github/workflows/crawler.yml` 的内容
4. 保存文件

### 4. 设置API URL（可选）

如果需要同步到网站后台：

1. 进入仓库 Settings → Secrets and variables → Actions
2. 点击 "New repository secret"
3. 名称：`API_URL`
4. 值：你的API地址（例如：`http://your-domain.com/data_sync.php`）
5. 点击 "Add secret"

### 5. 测试运行

1. 进入 "Actions" 标签
2. 选择 "苹果ID爬虫自动运行"
3. 点击 "Run workflow" → "Run workflow"（手动触发一次测试）

### 6. 查看运行结果

1. 在 "Actions" 标签中查看运行状态
2. 运行成功后，检查生成的文件是否已提交

## ⚙️ 配置说明

### 运行频率

默认配置：每小时运行一次

修改 `.github/workflows/crawler.yml` 中的 `cron` 表达式：

```yaml
schedule:
  - cron: '0 * * * *'  # 每小时
  # - cron: '0 */2 * * *'  # 每2小时
  # - cron: '0 0 * * *'  # 每天
```

### 时区说明

GitHub Actions使用UTC时间：
- UTC 0点 = 北京时间 8点
- UTC 8点 = 北京时间 16点
- UTC 16点 = 北京时间 0点（次日）

### Cron表达式示例

- `0 * * * *` - 每小时的第0分钟
- `0 */2 * * *` - 每2小时
- `0 0 * * *` - 每天0点
- `0 0 */6 * *` - 每6小时
- `0 8 * * *` - 每天8点（UTC）= 北京时间16点

## 📁 生成的文件

爬虫运行后会生成并提交以下文件：

- `apple_ids.json` - 完整账号数据
- `api_data.json` - API格式数据（符合网站要求）
- `apple_ids_simple.json` - 简化版数据
- `blog_accounts.json` - 博客用数据（随机2个账号）
- `accounts_simple.json` - 简化版数据

## ⚠️ 注意事项

1. **免费额度**：GitHub Actions免费账户每月有2000分钟额度
   - 每小时运行一次 ≈ 每月720分钟（在额度内）

2. **API URL**：如果不需要同步到网站后台，可以不设置 `API_URL`

3. **VPN广告数据**：确保 `vpn_ads.json` 文件存在且格式正确

4. **依赖安装**：确保 `requirements.txt` 包含所有必需的包

5. **文件提交**：工作流会自动提交生成的文件，如果文件没有变化，提交会被跳过（这是正常的）

## 🔍 故障排查

### 工作流没有运行

1. 检查 `.github/workflows/crawler.yml` 文件是否存在
2. 检查文件格式是否正确（YAML格式）
3. 检查 "Actions" 标签是否启用

### 运行失败

1. 查看 "Actions" 标签中的错误信息
2. 检查依赖是否正确安装
3. 检查网络连接（是否能访问目标网站）

### 文件没有更新

1. 检查爬虫是否成功运行
2. 检查是否有账号数据被提取
3. 查看日志确认是否有错误

## 📞 需要帮助？

如果遇到问题，请检查：
1. GitHub Actions日志
2. 代码是否正确上传
3. 依赖是否完整

