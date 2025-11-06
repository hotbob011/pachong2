# 快速配置指南

## 第一步：配置网站后台API

### Windows PowerShell:
```powershell
$env:API_URL = "http://your-domain.com/data_sync.php"
```

### Windows CMD:
```cmd
set API_URL=http://your-domain.com/data_sync.php
```

### Linux/Mac:
```bash
export API_URL="http://your-domain.com/data_sync.php"
```

**注意**: 将 `your-domain.com` 替换为你的实际域名，例如：
- `http://fanqiangnan.com/data_sync.php`
- `https://yourdomain.com/data_sync.php`

## 第二步：安装依赖

```bash
py -m pip install -r requirements.txt
```

## 第三步：测试运行

### 测试爬取（不同步）:
```bash
py apple_id_crawler.py
```

### 测试完整流程（爬取+同步）:
```bash
py main.py
```

## 第四步：启动定时任务

```bash
py scheduler.py
```

## 数据流程说明

1. **爬虫** → 从 https://ccbaohe.com/appleID/ 爬取账号
2. **格式化** → 转换为你的网站后台格式（group1, group2）
3. **API同步** → 通过 `data_sync.php` 更新到网站后台
4. **GitHub同步** → 推送到GitHub供博客使用

## 数据格式

爬虫会自动将数据格式化为你的系统格式：

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

## 验证同步

1. 运行爬虫后，访问你的 `boss.php` 后台
2. 点击"从服务器加载数据"
3. 应该能看到最新爬取的账号

## 常见问题

### Q: 如何确认API URL是否正确？
A: 在浏览器访问 `http://your-domain.com/data_sync.php`，应该返回JSON数据。

### Q: 同步失败怎么办？
A: 
1. 检查API URL是否正确
2. 确认 `data_sync.php` 文件存在且可访问
3. 查看日志文件 `crawler_scheduler.log`

### Q: 密码无法获取？
A: 密码可能通过JavaScript动态加载，需要检查网页源代码或使用Selenium。


