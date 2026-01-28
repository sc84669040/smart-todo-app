# GitHub Pages 部署指南

## 🚀 快速部署步骤

### 第一步：创建GitHub仓库
1. 访问 https://github.com
2. 登录或注册账号
3. 点击右上角"+" → "New repository"
4. 填写仓库信息：
   - **Repository name**: `my-todo-app`（建议使用这个名称）
   - **Description**: 智能待办事项应用
   - **Public**（必须选择公开）
   - **Initialize this repository with a README**（勾选）
5. 点击"Create repository"

### 第二步：上传文件到GitHub

**方法A：网页直接上传（推荐给初学者）**
1. 进入你创建的仓库页面
2. 点击"Add file" → "Upload files"
3. 将以下文件拖拽到上传区域：
   - `index.html`（主页面）
   - `todo_list_enhanced.html`（增强版待办事项）
   - `todo_list_with_dates.html`（日期分类版）
   - `todo_list.html`（基础版）
4. 在提交信息中输入："Initial commit - 智能待办事项应用"
5. 点击"Commit changes"

**方法B：使用Git命令（推荐给有经验的用户）**
```bash
# 克隆仓库到本地
git clone https://github.com/你的用户名/my-todo-app.git

# 复制文件到仓库目录
cp index.html todo_list*.html my-todo-app/

# 添加、提交并推送文件
cd my-todo-app
git add .
git commit -m "Initial commit - 智能待办事项应用"
git push origin main
```

### 第三步：启用GitHub Pages
1. 进入仓库页面
2. 点击"Settings"标签
3. 在左侧菜单中找到"Pages"
4. 在"Source"部分选择：
   - **Branch**: `main`
   - **Folder**: `/ (root)`
5. 点击"Save"

### 第四步：访问你的网站
等待1-2分钟后，访问：
```
https://你的用户名.github.io/my-todo-app
```

例如：`https://zhangsan.github.io/my-todo-app`

## 📱 网站功能

### 主页面 (index.html)
- 提供三个版本的选择界面
- 清晰的版本说明
- 响应式设计

### 增强版 (todo_list_enhanced.html)
- ✅ 智能日期分类
- ✅ 优先级管理系统
- ✅ 重复任务功能
- ✅ 主题切换
- ✅ 任务编辑功能

## 🔧 技术说明

### 文件结构
```
my-todo-app/
├── index.html          # 主页面
├── todo_list_enhanced.html    # 增强版（推荐）
├── todo_list_with_dates.html  # 日期分类版
└── todo_list.html             # 基础版
```

### 浏览器兼容性
- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

### 移动端支持
- 完全响应式设计
- 支持触摸操作
- 适配各种屏幕尺寸

## 💡 常见问题

### Q: 网站无法访问？
A: 检查：
1. 仓库是否为公开（Public）
2. GitHub Pages是否已启用
3. 等待1-2分钟让部署生效

### Q: 如何更新网站？
A: 重新上传修改后的HTML文件到GitHub仓库

### Q: 可以自定义域名吗？
A: 可以，在GitHub Pages设置中添加自定义域名

## 📞 支持
如果遇到问题，可以：
1. 查看GitHub Pages文档
2. 在GitHub Issues中提问
3. 检查浏览器控制台错误信息

---

**部署完成后，你就可以在任何设备上访问你的智能待办事项应用了！** 🎉