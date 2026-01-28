#!/usr/bin/env python3
"""
生成技能列表文档

扫描项目中的所有技能，生成包含技能名称和描述的文档
"""

import os
import yaml
import json
from pathlib import Path
from datetime import datetime


def scan_skills_directory(base_dir: str) -> list:
    """
    扫描技能目录，提取技能信息
    
    Args:
        base_dir: 基础目录路径
        
    Returns:
        技能信息列表
    """
    skills = []
    base_path = Path(base_dir)
    
    if not base_path.exists():
        return skills
    
    # 扫描所有包含 SKILL.md 的文件夹
    for item in base_path.rglob("SKILL.md"):
        skill_dir = item.parent
        
        try:
            # 读取技能文件
            content = item.read_text(encoding='utf-8')
            
            # 解析 YAML 头部
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    yaml_content = parts[1].strip()
                    metadata = yaml.safe_load(yaml_content) or {}
                    
                    # 提取技能信息
                    skill_info = {
                        'name': metadata.get('name', skill_dir.name),
                        'description': metadata.get('description', '暂无描述'),
                        'version': metadata.get('version', '1.0.0'),
                        'author': metadata.get('author', '未知'),
                        'category': metadata.get('category', '未分类'),
                        'tags': metadata.get('tags', []),
                        'path': str(skill_dir.relative_to(base_path)),
                        'source': base_dir
                    }
                    
                    skills.append(skill_info)
                    
        except Exception as e:
            print(f"解析技能文件失败 {item}: {e}")
    
    return skills


def load_deployed_skills(deployed_dir: str) -> list:
    """
    加载已部署的技能信息
    
    Args:
        deployed_dir: 已部署技能目录
        
    Returns:
        已部署技能信息列表
    """
    skills = []
    deployed_path = Path(deployed_dir)
    
    if not deployed_path.exists():
        return skills
    
    # 扫描部署目录
    for item in deployed_path.iterdir():
        if item.is_dir():
            config_file = item / "deployment.json"
            if config_file.exists():
                try:
                    with open(config_file, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                    
                    metadata = config.get('metadata', {})
                    skill_info = {
                        'name': config.get('skill_name', item.name),
                        'description': metadata.get('description', '暂无描述'),
                        'version': metadata.get('version', '1.0.0'),
                        'author': metadata.get('author', '未知'),
                        'category': metadata.get('category', '未分类'),
                        'tags': metadata.get('tags', []),
                        'path': str(item.relative_to(deployed_path)),
                        'source': '已部署',
                        'deployed_at': config.get('deployed_at')
                    }
                    
                    skills.append(skill_info)
                    
                except Exception as e:
                    print(f"读取部署配置失败 {config_file}: {e}")
    
    return skills


def generate_skill_document(skills: list, output_file: str):
    """
    生成技能列表文档
    
    Args:
        skills: 技能信息列表
        output_file: 输出文件路径
    """
    # 按分类分组
    categories = {}
    for skill in skills:
        category = skill['category']
        if category not in categories:
            categories[category] = []
        categories[category].append(skill)
    
    # 生成文档内容
    content = f"""# 技能列表文档

## 概述

本文档列出了当前项目中所有可用的技能，包括技能名称、描述、版本、作者等信息。

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**总技能数**: {len(skills)}  
**分类数量**: {len(categories)}

---

"""
    
    # 按分类输出技能信息
    for category, category_skills in sorted(categories.items()):
        content += f"## {category} 类技能\n\n"
        content += f"**技能数量**: {len(category_skills)}\n\n"
        
        for skill in sorted(category_skills, key=lambda x: x['name']):
            content += f"### {skill['name']}\n\n"
            content += f"**描述**: {skill['description']}  \n"
            content += f"**版本**: {skill['version']}  \n"
            content += f"**作者**: {skill['author']}  \n"
            content += f"**来源**: {skill['source']}  \n"
            content += f"**路径**: {skill['path']}  \n"
            
            if skill['tags']:
                content += f"**标签**: {', '.join(skill['tags'])}  \n"
            
            if skill.get('deployed_at'):
                content += f"**部署时间**: {skill['deployed_at']}  \n"
            
            content += "\n---\n\n"
    
    # 统计信息
    content += "## 统计信息\n\n"
    content += "| 分类 | 技能数量 |\n"
    content += "|------|----------|\n"
    
    for category, category_skills in sorted(categories.items()):
        content += f"| {category} | {len(category_skills)} |\n"
    
    content += f"\n**总计**: {len(skills)} 个技能\n"
    
    # 写入文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"技能列表文档已生成: {output_file}")


def main():
    """主函数"""
    # 扫描所有技能目录
    all_skills = []
    
    # 扫描示例技能
    example_skills = scan_skills_directory("example_skills")
    all_skills.extend(example_skills)
    
    # 扫描已部署技能
    deployed_skills = load_deployed_skills("deployed_skills")
    all_skills.extend(deployed_skills)
    
    # 去重（按名称）
    unique_skills = {}
    for skill in all_skills:
        name = skill['name']
        if name not in unique_skills:
            unique_skills[name] = skill
        else:
            # 优先保留已部署的技能
            if skill['source'] == '已部署':
                unique_skills[name] = skill
    
    unique_skills_list = list(unique_skills.values())
    
    # 生成文档
    output_file = "docs/skill_list.md"
    generate_skill_document(unique_skills_list, output_file)
    
    # 输出统计信息
    print(f"发现技能总数: {len(all_skills)}")
    print(f"去重后技能数: {len(unique_skills_list)}")
    
    # 按分类统计
    categories = {}
    for skill in unique_skills_list:
        category = skill['category']
        if category not in categories:
            categories[category] = 0
        categories[category] += 1
    
    print("\n分类统计:")
    for category, count in sorted(categories.items()):
        print(f"  {category}: {count} 个技能")


if __name__ == "__main__":
    main()