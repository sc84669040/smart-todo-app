#!/usr/bin/env python3
"""
技能列表脚本

用于列出已部署的技能和技能仓库中的技能
"""

import sys
import argparse
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich import box

# 添加 src 目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from skill_manager import SkillManager
from skill_deployer import SkillDeployer

console = Console()


def list_skills(skills_dir: str, deployed_dir: str, show_details: bool = False):
    """
    列出技能
    
    Args:
        skills_dir: 技能仓库目录
        deployed_dir: 已部署技能目录
        show_details: 是否显示详细信息
    """
    try:
        # 初始化管理器
        manager = SkillManager(skills_dir, deployed_dir)
        deployer = SkillDeployer(deployed_dir)
        
        # 发现技能仓库中的技能
        available_skills = manager.discover_skills()
        
        # 获取已部署的技能
        deployed_skills = deployer.list_deployed_skills()
        
        # 创建表格
        table = Table(title="技能列表", box=box.ROUNDED, show_header=True, header_style="bold magenta")
        
        table.add_column("技能名称", style="cyan", width=30)
        table.add_column("状态", justify="center", width=10)
        table.add_column("描述", style="green", width=50)
        table.add_column("版本", width=10)
        table.add_column("分类", width=15)
        
        # 处理技能仓库中的技能
        for skill_name in available_skills:
            skill_info = manager.load_skill(skill_name)
            if skill_info:
                metadata = skill_info.get('metadata', {})
                
                # 检查是否已部署
                is_deployed = any(s.get('skill_name') == skill_name for s in deployed_skills)
                status = "✅ 已部署" if is_deployed else "⏳ 未部署"
                
                table.add_row(
                    skill_name,
                    status,
                    metadata.get('description', '暂无描述')[:45] + "...",
                    metadata.get('version', '1.0.0'),
                    metadata.get('category', '未分类')
                )
        
        console.print(table)
        
        # 显示统计信息
        console.print(f"\n[bold]统计信息:[/bold]")
        console.print(f"技能仓库中的技能: {len(available_skills)}")
        console.print(f"已部署的技能: {len(deployed_skills)}")
        
        # 显示详细信息（如果启用）
        if show_details and deployed_skills:
            console.print(f"\n[bold]已部署技能详细信息:[/bold]")
            
            for skill in deployed_skills:
                metadata = skill.get('metadata', {})
                
                detail_table = Table(title=f"技能: {skill.get('skill_name')}", 
                                   box=box.SIMPLE, show_header=False)
                detail_table.add_column("属性", style="bold cyan")
                detail_table.add_column("值", style="white")
                
                detail_table.add_row("描述", metadata.get('description', '暂无'))
                detail_table.add_row("版本", metadata.get('version', '1.0.0'))
                detail_table.add_row("作者", metadata.get('author', '未知'))
                detail_table.add_row("部署时间", skill.get('deployed_at', '未知'))
                detail_table.add_row("文件数量", str(len(skill.get('files_exist', {}))))
                
                console.print(detail_table)
                console.print()
        
        # 生成技能索引
        index = deployer.generate_skill_index()
        if index:
            console.print(f"[bold green]技能索引已生成: config/skill_index.json[/bold green]")
        
    except Exception as e:
        console.print(f"[bold red]错误: {e}[/bold red]")
        sys.exit(1)


def show_skill_index(deployed_dir: str):
    """
    显示技能索引信息
    
    Args:
        deployed_dir: 已部署技能目录
    """
    try:
        deployer = SkillDeployer(deployed_dir)
        index = deployer.generate_skill_index()
        
        if not index:
            console.print("[yellow]暂无技能索引信息[/yellow]")
            return
        
        console.print(f"[bold]技能索引信息[/bold]")
        console.print(f"总技能数: {index.get('total_skills', 0)}")
        console.print(f"最后更新: {index.get('last_updated', '未知')}")
        
        # 显示分类统计
        categories = index.get('categories', {})
        if categories:
            console.print(f"\n[bold]分类统计:[/bold]")
            for category, count in categories.items():
                console.print(f"  {category}: {count} 个技能")
        
    except Exception as e:
        console.print(f"[bold red]错误: {e}[/bold red]")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='列出 Anthropic Skills 仓库中的技能')
    parser.add_argument('--skills-dir', default='skills', help='技能仓库目录')
    parser.add_argument('--deployed-dir', default='deployed_skills', help='已部署技能目录')
    parser.add_argument('--details', action='store_true', help='显示详细信息')
    parser.add_argument('--index', action='store_true', help='显示技能索引信息')
    
    args = parser.parse_args()
    
    if args.index:
        show_skill_index(args.deployed_dir)
    else:
        list_skills(args.skills_dir, args.deployed_dir, args.details)


if __name__ == "__main__":
    main()