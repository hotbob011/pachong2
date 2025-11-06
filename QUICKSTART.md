# 快速开始指南

## 第一步：安装依赖

```bash
py -m pip install -r requirements.txt
```

## 第二步：配置GitHub（可选）

如果你想自动同步到GitHub：

1. 初始化Git仓库：
```bash
git init
git remote add origin https://github.com/your-username/your-repo.git
```

2. 配置Git用户：
```bash
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

## 第三步：运行爬虫

### 方式1：使用批处理文件（Windows）
双击 `start.bat`，然后选择相应的选项。

### 方式2：命令行执行

**单次爬取并同步：**
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

## 输出文件说明

爬取完成后会生成以下文件：

- `apple_ids.json` - 完整数据（包含账号、密码、地区、状态等）
- `apple_ids_simple.json` - 简化数据（仅账号密码）
- `apple_ids.txt` - 文本格式
- `api_data.json` - API数据（供网站后台使用）
- `blog_accounts.json` - 博客数据（随机2个账号）

## 博客集成

你的博客可以通过GitHub Raw URL读取数据：

```html
<script>
fetch('https://raw.githubusercontent.com/your-username/repo/main/blog_accounts.json')
  .then(response => response.json())
  .then(data => {
    // 显示账号信息
    data.accounts.forEach(account => {
      console.log(`账号: ${account.email}, 密码: ${account.password}`);
    });
  });
</script>
```

## 网站后台集成

```php
<?php
// 从GitHub获取最新数据
$json = file_get_contents('https://raw.githubusercontent.com/your-username/repo/main/api_data.json');
$data = json_decode($json, true);

// 更新数据库
foreach ($data['accounts'] as $account) {
    // 更新账号信息
    updateAccount($account['email'], $account['password'], $account['region']);
}
?>
```

## 定时任务

### 方式1：使用scheduler.py（推荐）
```bash
py scheduler.py
```
程序会每2小时自动执行一次。

### 方式2：Windows任务计划程序

1. 打开"任务计划程序"
2. 创建基本任务
3. 名称：苹果ID爬虫
4. 触发器：重复任务，每2小时
5. 操作：启动程序
   - 程序：`py`
   - 参数：`scheduler.py`
   - 起始于：项目目录路径

## 注意事项

1. **密码获取**：如果密码无法获取，可能是因为密码通过JavaScript动态加载。可以尝试使用Selenium版本（需要额外安装selenium）。

2. **GitHub Token**：如果推送失败，可能需要配置GitHub Personal Access Token：
```bash
git remote set-url origin https://<your-token>@github.com/username/repo.git
```

3. **网络问题**：如果爬取失败，检查网络连接和目标网站是否可访问。

4. **日志查看**：定时任务的日志保存在 `crawler_scheduler.log` 文件中。

## 故障排除

### 问题1：无法获取密码
- 密码可能通过JavaScript动态加载
- 尝试检查网页源代码，查看密码存储位置
- 可能需要使用Selenium等浏览器自动化工具

### 问题2：GitHub推送失败
- 检查Git配置是否正确
- 确认有推送权限
- 使用GitHub Token进行身份验证

### 问题3：定时任务不执行
- 检查scheduler.py是否在运行
- 查看日志文件 `crawler_scheduler.log`
- 确认系统时间正确

## 技术支持

如有问题，请检查：
1. Python版本（需要Python 3.7+）
2. 依赖包是否安装完整
3. 网络连接是否正常
4. 目标网站是否可访问


