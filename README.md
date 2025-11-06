# 苹果ID爬虫系统 - 集成版

自动爬取  的账号信息，并自动同步到：
1. **网站后台** - 通过API自动更新 `data_sync.php`
2. **GitHub仓库** - 供博客随机读取账号

## 功能特点

- 🔄 **自动爬取**: 每2小时自动爬取最新账号信息
- 🌐 **网站后台同步**: 自动更新到你的网站后台API
- ☁️ **GitHub同步**: 自动推送到GitHub仓库
- 📝 **博客集成**: 自动生成博客可用的随机账号数据
- 📊 **多格式输出**: JSON、TXT等多种格式

## 安装依赖

```bash
pip install -r requirements.txt
```

## 配置

### 1. 配置网站后台API

设置环境变量或在 `scheduler.py` 中配置：

**Windows (PowerShell):**
```powershell
$env:API_URL = "http://your-domain.com/data_sync.php"
```

**Windows (CMD):**
```cmd
set API_URL=http://your-domain.com/data_sync.php
```

**Linux/Mac:**
```bash
export API_URL="http://your-domain.com/data_sync.php"
```

或者在代码中直接修改 `main.py` 和 `scheduler.py` 中的 `api_url` 变量。

### 2. 配置GitHub仓库（可选）

如果需要同步到GitHub：

```bash
git init
git remote add origin https://github.com/your-username/your-repo.git
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

## 使用方法

### 方式1：使用批处理文件（Windows）
双击 `start.bat`，然后选择相应的选项。

### 方式2：命令行执行

**单次执行（爬取+同步到网站后台+GitHub）：**
```bash
py main.py
```

**启动定时任务（每2小时自动执行）：**
```bash
py scheduler.py
```

**仅爬取数据：**
```bash
py apple_id_crawler.py
```

**仅同步到GitHub：**
```bash
py github_sync.py
```

## 数据格式说明

爬虫会自动将数据格式化为你的网站后台API所需的格式：

```json
{
  "group1": [
    {
      "id": "1-1",
      "fullEmail": "example@hotmail.com",
      "password": "password123",
      "status": "正常",
      "checkTime": "2025-01-07 12:00:00",
      "region": "US",
      "regionName": "美国"
    }
  ],
  "group2": []
}
```

## 网站后台集成

爬虫会自动调用你的 `data_sync.php` API：

```php
POST http://your-domain.com/data_sync.php?type=accounts
Content-Type: application/json

{
  "data": {
    "group1": [...],
    "group2": []
  }
}
```

前端页面 `apple_id.html` 会自动从API读取最新数据并显示。

## 博客集成

博客可以通过GitHub Raw URL读取数据：

```javascript
// 获取随机账号
fetch('https://raw.githubusercontent.com/your-username/repo/main/blog_accounts.json')
  .then(response => response.json())
  .then(data => {
    console.log('账号列表:', data.accounts);
  });
```

## 定时任务

使用 `scheduler.py` 启动定时任务后，系统会：
1. 立即执行一次爬取
2. 每2小时自动执行一次
3. 自动同步到网站后台API
4. 自动同步到GitHub
5. 记录日志到 `crawler_scheduler.log`

### Windows任务计划程序

也可以使用Windows任务计划程序：
1. 打开"任务计划程序"
2. 创建基本任务
3. 触发器：每2小时
4. 操作：启动程序 `py scheduler.py`
5. 在"环境变量"中设置 `API_URL`

## 输出文件

- `apple_ids.json` - 完整账号数据
- `apple_ids_simple.json` - 简化数据（仅账号密码）
- `api_data.json` - API数据（供网站后台使用）
- `blog_accounts.json` - 博客数据（随机2个账号）

## 注意事项

1. ⚠️ **API URL配置**: 确保正确配置 `API_URL` 环境变量
2. ⚠️ **密码获取**: 如果密码无法获取，可能需要使用Selenium版本
3. ⚠️ **请求频率**: 合理设置请求延迟，避免对服务器造成压力
4. ⚠️ **数据格式**: 爬虫会自动格式化数据以匹配你的网站后台格式

## 故障排除

### 问题1：网站后台同步失败
- 检查 `API_URL` 是否正确配置
- 确认 `data_sync.php` 可以正常访问
- 检查网络连接和防火墙设置

### 问题2：无法获取密码
- 密码可能通过JavaScript动态加载
- 尝试检查网页源代码，查看密码存储位置
- 可能需要使用Selenium等浏览器自动化工具

### 问题3：定时任务不执行
- 检查 `scheduler.py` 是否在运行
- 查看日志文件 `crawler_scheduler.log`
- 确认系统时间正确

## 许可证

MIT License
