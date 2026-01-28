# MyTool - Anthropic Skills 部署工具

这是一个用于部署和管理 Anthropic Skills 仓库中所有技能的工具。

## 项目目标

- 部署 Anthropic Skills 仓库中的所有技能
- 提供技能管理和加载功能
- 支持技能的自定义和扩展
- 生成技能索引和部署报告

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 获取技能仓库

```bash
# 克隆官方技能仓库
git clone https://github.com/anthropics/skills.git

# 或者使用项目自带的示例技能进行测试
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

### 4. 查看技能

```bash
# 查看技能列表
python scripts/list_skills.py --skills-dir skills

# 查看详细信息
python scripts/list_skills.py --skills-dir skills --details
```

## 项目结构

```
MyTool/
├── src/                    # 源代码
│   ├── skill_manager.py    # 技能管理核心
│   ├── skill_loader.py     # 技能加载器
│   └── skill_deployer.py   # 技能部署器
├── scripts/                # 脚本文件
│   ├── deploy_skills.py    # 部署脚本
│   └── list_skills.py      # 列表脚本
├── example_skills/         # 示例技能
├── deployed_skills/        # 已部署技能
├── config/                 # 配置文件
├── tests/                  # 测试文件
└── docs/                   # 文档
```

## 技能仓库信息

- 来源：https://github.com/anthropics/skills.git
- 包含技能类型：创意设计、开发技术、企业通信、文档处理等
- 每个技能都是独立的文件夹，包含 SKILL.md 文件

## 核心功能

- **技能发现**: 自动发现技能仓库中的所有技能
- **技能解析**: 解析 SKILL.md 文件的 YAML 头部和 Markdown 内容
- **技能部署**: 将技能部署到指定目录，包含资源文件
- **技能管理**: 提供技能的加载、验证、部署和卸载功能
- **索引生成**: 自动生成技能索引和部署报告

## 文档

- [开发指南](docs/development_guide.md) - 技术栈和开发规范
- [使用指南](docs/usage_guide.md) - 详细使用说明

## 技能格式

每个技能包含 SKILL.md 文件，格式如下：

```yaml
---
name: skill-name
description: 技能描述
version: 1.0.0
author: 作者名
---

# 技能内容...
```