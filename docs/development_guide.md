# 开发指南

## 技术栈

- Python 3.8+
- 主要依赖：requests, pyyaml, click, rich
- 技能格式：基于 SKILL.md 文件的 YAML + Markdown 格式

## 目录结构

```
MyTool/
├── skills/                 # 技能仓库（从 GitHub 克隆）
├── deployed_skills/        # 已部署的技能
├── src/
│   ├── skill_manager.py    # 技能管理核心类
│   ├── skill_loader.py     # 技能加载器
│   └── skill_deployer.py   # 技能部署器
├── scripts/
│   ├── deploy_skills.py    # 部署脚本
│   └── list_skills.py      # 技能列表脚本
├── tests/                  # 测试文件
└── docs/                   # 文档
```

## 开发规范

1. **代码风格**: 遵循 PEP8，使用类型提示
2. **错误处理**: 所有外部操作都需要适当的错误处理
3. **日志记录**: 使用 logging 模块记录重要操作
4. **模块化**: 功能模块化，便于维护和扩展

## 技能格式规范

每个技能包含：
- SKILL.md 文件（YAML 头部 + Markdown 内容）
- 可选的资源文件（scripts/, resources/ 等）

SKILL.md 示例：
```yaml
---
name: my-skill-name
description: 技能描述
version: 1.0.0
author: 作者名
---

# 技能名称

技能详细说明和使用方法...
```