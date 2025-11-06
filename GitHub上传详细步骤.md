# GitHub上传详细步骤（完整版）

## 📋 准备工作

### 1. 检查文件

确保以下核心文件存在：
- ✅ `apple_id_crawler.py`
- ✅ `main.py`
- ✅ `github_sync.py`
- ✅ `vpn_ads.json`
- ✅ `requirements.txt`
- ✅ `.github/workflows/crawler.yml`
- ✅ `.gitignore`

## 🚀 方法一：使用Git命令（推荐）

### 步骤1：安装Git（如果还没安装）

1. 访问：https://git-scm.com/download/win
2. 下载并安装Git for Windows
3. 安装时选择默认选项即可

### 步骤2：打开Git Bash或命令提示符

**方法A：使用Git Bash（推荐）**
- 在项目文件夹中，右键点击空白处
- 选择 "Git Bash Here"

**方法B：使用命令提示符**
- 在项目文件夹中，按住 `Shift` 键，右键点击空白处
- 选择 "在此处打开PowerShell窗口" 或 "在此处打开命令窗口"

### 步骤3：初始化Git仓库

在打开的终端中，输入以下命令：

```bash
git init
```

**预期输出：**
```
Initialized empty Git repository in E:/google down/ID爬虫/.git/
```

### 步骤4：添加所有文件

```bash
git add .
```

**说明：** 这个命令会添加所有文件，但 `.gitignore` 会自动过滤掉不需要的文件

**验证：** 可以查看哪些文件被添加了：
```bash
git status
```

**预期输出：** 应该看到以下文件被添加：
- `apple_id_crawler.py`
- `main.py`
- `github_sync.py`
- `vpn_ads.json`
- `requirements.txt`
- `.github/workflows/crawler.yml`
- `.gitignore`
- 以及一些文档文件

**不应该看到：**
- `*.bat` 文件
- `*test*.py` 文件
- `api_data.json` 等生成的文件

### 步骤5：创建首次提交

```bash
git commit -m "初始提交：苹果ID爬虫"
```

**预期输出：**
```
[main (root-commit) xxxxxxx] 初始提交：苹果ID爬虫
 X files changed, XXXX insertions(+)
```

### 步骤6：在GitHub上创建仓库

1. 打开浏览器，访问：https://github.com
2. 登录你的GitHub账号（如果没有账号，先注册）
3. 点击右上角的 **"+"** 号
4. 选择 **"New repository"**
5. 填写仓库信息：
   - **Repository name**: 输入仓库名称（例如：`apple-id-crawler`）
   - **Description**: 可选，输入描述（例如：`苹果ID账号爬虫`）
   - **Public** 或 **Private**: 选择公开或私有
   - **不要勾选** "Add a README file"（我们已经有了）
   - **不要勾选** "Add .gitignore"（我们已经有了）
   - **不要选择** License
6. 点击 **"Create repository"** 按钮

### 步骤7：连接本地仓库到GitHub

创建仓库后，GitHub会显示一个页面，上面有仓库地址，类似：
```
https://github.com/你的用户名/仓库名.git
```

在终端中执行（**替换成你的实际地址**）：

```bash
git remote add origin https://github.com/你的用户名/仓库名.git
```

**示例：**
```bash
git remote add origin https://github.com/zhangsan/apple-id-crawler.git
```

### 步骤8：重命名分支为main（如果需要）

```bash
git branch -M main
```

### 步骤9：推送到GitHub

```bash
git push -u origin main
```

**说明：** 
- 第一次推送会要求输入GitHub用户名和密码
- 如果使用HTTPS，密码需要使用Personal Access Token（不是GitHub密码）
- 如果使用SSH，需要配置SSH密钥

**如果提示输入用户名和密码：**
1. 用户名：输入你的GitHub用户名
2. 密码：需要创建Personal Access Token
   - 访问：https://github.com/settings/tokens
   - 点击 "Generate new token" → "Generate new token (classic)"
   - 输入名称（例如：`git-push`）
   - 选择过期时间
   - 勾选 `repo` 权限
   - 点击 "Generate token"
   - 复制生成的token（只显示一次，要保存好）
   - 在密码提示处粘贴这个token

**预期输出：**
```
Enumerating objects: XX, done.
Counting objects: 100% (XX/XX), done.
Writing objects: 100% (XX/XX), done.
To https://github.com/你的用户名/仓库名.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

### 步骤10：验证上传成功

1. 刷新GitHub仓库页面
2. 应该能看到所有文件都已上传
3. 检查是否有 `.github/workflows/crawler.yml` 文件

## 🔧 方法二：使用GitHub Desktop（图形界面）

### 步骤1：下载GitHub Desktop

1. 访问：https://desktop.github.com/
2. 下载并安装GitHub Desktop
3. 登录你的GitHub账号

### 步骤2：添加本地仓库

1. 打开GitHub Desktop
2. 点击 **"File"** → **"Add Local Repository"**
3. 点击 **"Choose..."** 按钮
4. 选择你的项目文件夹（`E:\google down\ID爬虫`）
5. 点击 **"Add repository"**

### 步骤3：检查文件

1. 在GitHub Desktop中，应该能看到所有文件
2. 检查是否有不需要的文件（如 `*.bat`、`test_result.json` 等）
3. 如果有不需要的文件，可以手动删除或修改 `.gitignore`

### 步骤4：提交文件

1. 在左下角输入提交信息：`初始提交：苹果ID爬虫`
2. 点击 **"Commit to main"** 按钮

### 步骤5：发布到GitHub

1. 点击右上角的 **"Publish repository"** 按钮
2. 输入仓库名称（例如：`apple-id-crawler`）
3. 选择是否公开（Public/Private）
4. 点击 **"Publish repository"**

### 步骤6：验证

1. 在GitHub Desktop中点击 **"View on GitHub"**
2. 检查文件是否都已上传

## 🔧 方法三：使用网页上传（最简单）

### 步骤1：在GitHub上创建仓库

1. 访问：https://github.com
2. 登录账号
3. 点击右上角 **"+"** → **"New repository"**
4. 填写仓库名称，点击 **"Create repository"**

### 步骤2：上传文件

1. 在仓库页面，点击 **"uploading an existing file"** 链接
2. 将以下文件拖拽到上传区域：
   - `apple_id_crawler.py`
   - `main.py`
   - `github_sync.py`
   - `vpn_ads.json`
   - `requirements.txt`
   - `.gitignore`
   - `.github/workflows/crawler.yml`（需要先创建文件夹）
3. 对于 `.github/workflows/crawler.yml`：
   - 点击 **"Add file"** → **"Create new file"**
   - 路径输入：`.github/workflows/crawler.yml`
   - 复制文件内容粘贴进去
4. 在页面底部输入提交信息：`初始提交：苹果ID爬虫`
5. 点击 **"Commit changes"**

## ✅ 上传后检查

### 1. 检查必需文件

在GitHub仓库页面，确认以下文件存在：
- [ ] `apple_id_crawler.py`
- [ ] `main.py`
- [ ] `github_sync.py`
- [ ] `vpn_ads.json`
- [ ] `requirements.txt`
- [ ] `.github/workflows/crawler.yml`
- [ ] `.gitignore`

### 2. 检查不需要的文件

确认以下文件**不存在**（被.gitignore过滤）：
- [ ] 没有 `*.bat` 文件
- [ ] 没有 `*test*.py` 文件
- [ ] 没有 `api_data.json` 等生成的文件

### 3. 启用GitHub Actions

1. 点击仓库顶部的 **"Actions"** 标签
2. 如果看到 **"苹果ID爬虫自动运行"** 工作流
3. 点击 **"Enable"** 或 **"I understand my workflows, go ahead and enable them"**

### 4. 测试运行

1. 在 **"Actions"** 标签中
2. 选择 **"苹果ID爬虫自动运行"**
3. 点击 **"Run workflow"** → **"Run workflow"**
4. 等待运行完成（约1-2分钟）
5. 检查是否成功（绿色✓表示成功）

## 🔑 设置API URL（可选）

如果需要同步到网站后台：

1. 进入仓库 **Settings**（设置）
2. 左侧菜单选择 **Secrets and variables** → **Actions**
3. 点击 **"New repository secret"**
4. 填写：
   - **Name**: `API_URL`
   - **Secret**: 你的API地址（例如：`http://your-domain.com/data_sync.php`）
5. 点击 **"Add secret"**

## ⚠️ 常见问题

### Q1: 提示 "fatal: not a git repository"
**解决：** 先执行 `git init`

### Q2: 提示 "remote origin already exists"
**解决：** 先删除：`git remote remove origin`，然后重新添加

### Q3: 提示 "Authentication failed"
**解决：** 
- 使用Personal Access Token代替密码
- 或配置SSH密钥

### Q4: 提示 "Permission denied"
**解决：** 
- 检查仓库名称是否正确
- 检查是否有权限访问该仓库

### Q5: 文件上传了但Actions没有运行
**解决：** 
- 检查 `.github/workflows/crawler.yml` 文件是否存在
- 检查文件路径是否正确
- 手动触发一次测试

## 📝 后续更新

如果以后修改了代码，需要更新到GitHub：

```bash
git add .
git commit -m "更新说明"
git push
```

## 🎉 完成！

上传成功后：
- ✅ 代码已上传到GitHub
- ✅ GitHub Actions会自动每小时运行一次
- ✅ 生成的文件会自动提交到仓库

