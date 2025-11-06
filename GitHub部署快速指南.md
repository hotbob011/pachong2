# GitHub部署快速指南

## 🚀 快速部署（5分钟）

### 步骤1：创建GitHub仓库

1. 登录GitHub
2. 点击右上角 "+" → "New repository"
3. 输入仓库名称（例如：`apple-id-crawler`）
4. 选择 Public 或 Private
5. 点击 "Create repository"

### 步骤2：上传代码

#### 方法1：使用Git命令（推荐）

```bash
# 在项目目录下执行
git init
git add .
git commit -m "初始提交：苹果ID爬虫"
git branch -M main
git remote add origin https://github.com/你的用户名/仓库名.git
git push -u origin main
```

#### 方法2：使用GitHub Desktop

1. 下载安装 GitHub Desktop
2. 打开项目文件夹
3. 点击 "Publish repository"
4. 输入仓库名称，点击 "Publish"

#### 方法3：网页上传

1. 在GitHub仓库页面，点击 "uploading an existing file"
2. 拖拽所有文件上传
3. 点击 "Commit changes"

### 步骤3：启用GitHub Actions

1. 进入仓库页面
2. 点击 "Actions" 标签
3. 如果看到 "苹果ID爬虫自动运行" 工作流，点击 "Enable"
4. 如果没有，检查 `.github/workflows/crawler.yml` 文件是否存在

### 步骤4：设置API URL（可选）

如果需要同步到网站后台：

1. 进入仓库 Settings → Secrets and variables → Actions
2. 点击 "New repository secret"
3. 名称：`API_URL`
4. 值：你的API地址（例如：`http://your-domain.com/data_sync.php`）
5. 点击 "Add secret"

### 步骤5：测试运行

1. 进入 "Actions" 标签
2. 选择 "苹果ID爬虫自动运行"
3. 点击 "Run workflow" → "Run workflow"
4. 等待运行完成（约1-2分钟）

## ✅ 验证部署

### 检查工作流是否运行

1. 进入 "Actions" 标签
2. 查看是否有绿色的 ✓ 标记
3. 点击运行记录查看详细日志

### 检查文件是否更新

1. 进入仓库主页
2. 查看以下文件是否已更新：
   - `apple_ids.json`
   - `api_data.json`
   - `blog_accounts.json`

### 检查自动运行

1. 等待1小时后
2. 进入 "Actions" 标签
3. 应该能看到新的运行记录

## ⚙️ 配置说明

### 运行频率

默认：每小时运行一次

修改 `.github/workflows/crawler.yml`：

```yaml
schedule:
  - cron: '0 * * * *'  # 每小时
```

其他选项：
- `0 */2 * * *` - 每2小时
- `0 0 * * *` - 每天
- `0 */6 * * *` - 每6小时

### 时区

GitHub Actions使用UTC时间：
- UTC 0点 = 北京时间 8点
- UTC 8点 = 北京时间 16点

## 📁 必需文件清单

确保以下文件已上传：

- ✅ `apple_id_crawler.py`
- ✅ `main.py`
- ✅ `github_sync.py`
- ✅ `vpn_ads.json`
- ✅ `requirements.txt`
- ✅ `.github/workflows/crawler.yml`

## ⚠️ 注意事项

1. **免费额度**：GitHub Actions免费账户每月2000分钟
   - 每小时运行 ≈ 每月720分钟（在额度内）

2. **API URL**：如果不需要同步到网站后台，可以不设置

3. **文件提交**：如果数据没有变化，提交会被跳过（正常）

4. **VPN广告**：确保 `vpn_ads.json` 文件存在

## 🔍 常见问题

### Q: 工作流没有运行？
A: 检查 `.github/workflows/crawler.yml` 文件是否存在且格式正确

### Q: 运行失败？
A: 查看 "Actions" 标签中的错误日志

### Q: 文件没有更新？
A: 检查爬虫是否成功提取到数据

### Q: 如何手动运行？
A: 进入 "Actions" → 选择工作流 → "Run workflow"

## 📞 需要帮助？

查看详细文档：`部署到GitHub.md`

