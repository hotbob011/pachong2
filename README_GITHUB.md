# 苹果ID爬虫 - GitHub自动运行

## 📦 功能

- ✅ 每小时自动爬取苹果ID账号
- ✅ 自动生成符合网站要求的格式
- ✅ 自动提交更新到GitHub
- ✅ 支持同步到网站后台API

## 🚀 快速开始

### 1. 上传代码到GitHub

```bash
git init
git add .
git commit -m "初始提交"
git branch -M main
git remote add origin https://github.com/你的用户名/仓库名.git
git push -u origin main
```

### 2. 启用GitHub Actions

1. 进入仓库 → Actions 标签
2. 如果看到工作流，点击 "Enable"
3. 工作流会自动每小时运行一次

### 3. 设置API URL（可选）

如果需要同步到网站后台：

1. Settings → Secrets and variables → Actions
2. New repository secret
3. 名称：`API_URL`
4. 值：你的API地址
5. Add secret

## ⏰ 运行时间

- **默认**：每小时运行一次（UTC时间）
- **手动触发**：Actions → Run workflow

## 📁 生成的文件

- `apple_ids.json` - 完整数据
- `api_data.json` - API格式（符合网站要求）
- `blog_accounts.json` - 博客用数据（随机2个）
- `apple_ids_simple.json` - 简化版
- `accounts_simple.json` - 简化版

## 📖 详细文档

- `GitHub部署快速指南.md` - 快速部署步骤
- `部署到GitHub.md` - 详细配置说明

