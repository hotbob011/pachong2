# GitHub上传文件清单

## ✅ 必须上传的文件（核心功能）

### 核心爬虫文件
- ✅ `apple_id_crawler.py` - 核心爬虫脚本
- ✅ `main.py` - 主执行脚本
- ✅ `github_sync.py` - GitHub同步脚本
- ✅ `vpn_ads.json` - VPN广告数据（必需）

### 配置文件
- ✅ `requirements.txt` - Python依赖列表
- ✅ `.github/workflows/crawler.yml` - GitHub Actions工作流（必需）
- ✅ `.gitignore` - Git忽略文件配置

## 📝 可选上传的文件（文档）

### 文档文件（可选，建议上传）
- 📄 `README.md` - 项目说明
- 📄 `README_GITHUB.md` - GitHub使用说明
- 📄 `GitHub部署快速指南.md` - 快速部署指南
- 📄 `部署到GitHub.md` - 详细部署文档
- 📄 `部署说明.md` - 服务器部署说明
- 📄 `部署文件清单.txt` - 部署文件清单
- 📄 `QUICKSTART.md` - 快速开始指南
- 📄 `CONFIG_GUIDE.md` - 配置指南

## ❌ 不需要上传的文件

### 测试/调试文件（不需要）
- ❌ `simple_test.py` - 测试脚本
- ❌ `test.bat` - Windows测试脚本
- ❌ `运行测试.bat` - Windows测试脚本
- ❌ `调试地区.bat` - 调试脚本
- ❌ `debug_region.py` - 调试脚本
- ❌ `debug_password_detail.py` - 调试脚本
- ❌ `debug_password.py` - 调试脚本
- ❌ `test_crawler.py` - 测试脚本
- ❌ `test_inline.py` - 测试脚本
- ❌ `quick_test.py` - 快速测试
- ❌ `simple_test_v2.py` - 测试脚本
- ❌ `format_check.py` - 格式检查
- ❌ `test_region_extract.py` - 测试脚本

### 示例/演示文件（不需要）
- ❌ `example.py` - 示例文件
- ❌ `id_crawler.py` - 通用爬虫（不使用）
- ❌ `cf_email_decoder.py` - 已集成到主文件
- ❌ `config.example.json` - 示例配置
- ❌ `config.example.py` - 示例配置

### 批处理文件（Windows专用，不需要）
- ❌ `*.bat` - 所有批处理文件
  - `test.bat`
  - `运行测试.bat`
  - `调试地区.bat`
  - `debug_password_detail.bat`
  - `debug_password.bat`
  - `run_simple_test.bat`
  - `run_test.bat`
  - `start.bat`

### 文档文件（本地使用，不需要）
- ❌ `测试说明.txt` - 本地测试说明
- ❌ `快速测试.txt` - 本地测试说明
- ❌ `RUN_TEST.txt` - 本地测试说明
- ❌ `MANUAL_TEST.md` - 手动测试说明
- ❌ `TEST_GUIDE.md` - 测试指南
- ❌ `TEST_UPDATE.md` - 测试更新说明
- ❌ `UPDATE_NOTES.md` - 更新说明

### 生成的文件（会自动生成，不需要上传）
- ❌ `apple_ids.json` - 运行后自动生成
- ❌ `api_data.json` - 运行后自动生成
- ❌ `apple_ids_simple.json` - 运行后自动生成
- ❌ `blog_accounts.json` - 运行后自动生成
- ❌ `accounts_simple.json` - 运行后自动生成
- ❌ `test_result.json` - 测试结果

### 其他文件（不需要）
- ❌ `scheduler.py` - 本地定时任务（GitHub Actions不需要）

## 📋 推荐上传的文件清单

### 最小化上传（只包含必需文件）

```bash
# 核心文件
apple_id_crawler.py
main.py
github_sync.py
vpn_ads.json
requirements.txt
.github/workflows/crawler.yml
.gitignore
```

### 完整上传（包含文档）

```bash
# 核心文件
apple_id_crawler.py
main.py
github_sync.py
vpn_ads.json
requirements.txt
.github/workflows/crawler.yml
.gitignore

# 文档文件（可选）
README.md
README_GITHUB.md
GitHub部署快速指南.md
部署到GitHub.md
```

## 🚀 快速上传命令

### 方法1：只上传必需文件

```bash
git add apple_id_crawler.py main.py github_sync.py vpn_ads.json requirements.txt .github/workflows/crawler.yml .gitignore
git commit -m "初始提交：核心文件"
git push
```

### 方法2：上传核心文件+文档

```bash
git add apple_id_crawler.py main.py github_sync.py vpn_ads.json requirements.txt .github/workflows/crawler.yml .gitignore
git add README*.md GitHub*.md 部署*.md
git commit -m "初始提交：核心文件+文档"
git push
```

### 方法3：使用.gitignore自动过滤

```bash
# .gitignore已经配置好了，会自动忽略不需要的文件
git add .
git commit -m "初始提交"
git push
```

## ⚠️ 重要提示

1. **`.gitignore` 已配置**：会自动忽略生成的文件和测试文件
2. **`vpn_ads.json` 必须上传**：这是数据文件，不是生成的
3. **`.github/workflows/crawler.yml` 必须上传**：这是自动运行的关键
4. **生成的文件不需要上传**：GitHub Actions会自动生成

## 📝 检查清单

上传前检查：
- [ ] `apple_id_crawler.py` ✓
- [ ] `main.py` ✓
- [ ] `github_sync.py` ✓
- [ ] `vpn_ads.json` ✓
- [ ] `requirements.txt` ✓
- [ ] `.github/workflows/crawler.yml` ✓
- [ ] `.gitignore` ✓

