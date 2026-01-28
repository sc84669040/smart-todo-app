# 使用指南

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 准备技能仓库

有两种方式获取技能仓库：

**方式一：克隆官方仓库（推荐）**
```bash
git clone https://github.com/anthropics/skills.git
```

**方式二：使用示例技能（测试用）**
```bash
# 项目已包含示例技能，可直接测试
```

### 3. 部署技能

```bash
# 部署所有技能
python scripts/deploy_skills.py --skills-dir skills

# 部署单个技能
python scripts/deploy_skills.py --skills-dir skills --skill pdf-skill

# 使用示例技能测试
python scripts/deploy_skills.py --skills-dir example_skills
```

### 4. 查看技能列表

```bash
# 查看技能列表
python scripts/list_skills.py --skills-dir skills

# 查看详细信息
python scripts/list_skills.py --skills-dir skills --details

# 查看技能索引
python scripts/list_skills.py --index
```

## 技能格式说明

### 技能文件结构

每个技能都是一个独立的文件夹，包含：

```
skill-name/
├── SKILL.md          # 技能主文件（必需）
├── scripts/          # 脚本文件（可选）
├── resources/        # 资源文件（可选）
├── examples/         # 示例文件（可选）
└── templates/        # 模板文件（可选）
```

### SKILL.md 文件格式

```yaml
---
name: skill-name              # 技能名称（必需）
description: 技能描述         # 技能描述（必需）
version: 1.0.0               # 版本号（可选）
author: 作者名               # 作者（可选）
category: 分类               # 分类（可选）
tags: [标签1, 标签2]         # 标签（可选）
---

# 技能标题

技能详细说明...

## 功能说明

- 功能点1
- 功能点2

## 使用方法

1. 第一步
2. 第二步

## 示例

- Example: 示例1
- Example: 示例2

## 指南

- Guideline: 指南1
- Guideline: 指南2
```

## 核心功能模块

### 1. 技能管理器 (SkillManager)

负责技能的发现、加载和管理：

```python
from src.skill_manager import SkillManager

# 初始化
manager = SkillManager(skills_dir="skills", deployed_dir="deployed_skills")

# 发现技能
skills = manager.discover_skills()

# 加载技能
skill_info = manager.load_skill("skill-name")

# 部署技能
manager.deploy_skill("skill-name")
```

### 2. 技能加载器 (SkillLoader)

负责技能的解析和验证：

```python
from src.skill_loader import SkillLoader

# 初始化
loader = SkillLoader()

# 解析技能文件
skill_info = loader.parse_skill_file("path/to/SKILL.md")

# 验证技能
errors = loader.validate_skill(skill_info)
```

### 3. 技能部署器 (SkillDeployer)

负责技能的部署和配置：

```python
from src.skill_deployer import SkillDeployer

# 初始化
deployer = SkillDeployer(deployed_dir="deployed_skills")

# 部署技能
deployer.deploy_skill(skill_path, skill_info)

# 列出已部署技能
deployed = deployer.list_deployed_skills()

# 生成技能索引
index = deployer.generate_skill_index()
```

## 常见问题

### Q: 技能部署失败怎么办？
A: 检查技能文件格式是否正确，确保 SKILL.md 文件包含正确的 YAML 头部。

### Q: 如何添加自定义技能？
A: 在技能仓库目录中创建新的技能文件夹，按照格式要求编写 SKILL.md 文件。

### Q: 部署后的技能在哪里？
A: 部署后的技能保存在 `deployed_skills` 目录中，每个技能一个文件夹。

### Q: 如何卸载技能？
A: 目前需要手动删除 `deployed_skills` 目录中对应的技能文件夹。

## 日志文件

系统会生成日志文件 `skill_deployment.log`，包含详细的部署过程信息。

## 配置文件

- `config/skill_index.json`: 技能索引文件
- 每个技能目录下的 `deployment.json`: 部署配置信息