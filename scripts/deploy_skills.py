#!/usr/bin/env python3
"""
技能部署脚本

用于部署 Anthropic Skills 仓库中的所有技能
"""

import sys
import argparse
from pathlib import Path

# 添加 src 目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from skill_manager import SkillManager
from skill_deployer import SkillDeployer
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('skill_deployment.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def deploy_skills(skills_dir: str, deployed_dir: str, specific_skill: str = None) -> bool:
    """
    部署技能
    
    Args:
        skills_dir: 技能仓库目录
        deployed_dir: 已部署技能目录
        specific_skill: 指定部署的单个技能（可选）
        
    Returns:
        部署是否成功
    """
    try:
        # 初始化管理器
        manager = SkillManager(skills_dir, deployed_dir)
        deployer = SkillDeployer(deployed_dir)
        
        # 发现技能
        skills = manager.discover_skills()
        
        if not skills:
            logger.error("未发现任何技能，请检查技能仓库目录")
            return False
        
        logger.info(f"发现 {len(skills)} 个技能")
        
        # 部署技能
        if specific_skill:
            if specific_skill not in skills:
                logger.error(f"指定的技能不存在: {specific_skill}")
                return False
            
            # 部署单个技能
            skill_info = manager.load_skill(specific_skill)
            if not skill_info:
                logger.error(f"无法加载技能: {specific_skill}")
                return False
            
            success = deployer.deploy_skill(Path(skills_dir) / specific_skill, skill_info)
            if success:
                logger.info(f"技能部署成功: {specific_skill}")
            else:
                logger.error(f"技能部署失败: {specific_skill}")
            
            return success
        else:
            # 部署所有技能
            results = {}
            success_count = 0
            
            for skill_name in skills:
                skill_info = manager.load_skill(skill_name)
                if skill_info:
                    success = deployer.deploy_skill(Path(skills_dir) / skill_name, skill_info)
                    results[skill_name] = success
                    if success:
                        success_count += 1
                else:
                    results[skill_name] = False
            
            # 生成部署报告
            logger.info(f"部署完成 - 成功: {success_count}/{len(skills)}")
            
            # 生成技能索引
            deployer.generate_skill_index()
            
            return success_count > 0
            
    except Exception as e:
        logger.error(f"部署过程发生错误: {e}")
        return False


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='部署 Anthropic Skills 仓库中的技能')
    parser.add_argument('--skills-dir', default='skills', help='技能仓库目录')
    parser.add_argument('--deployed-dir', default='deployed_skills', help='已部署技能目录')
    parser.add_argument('--skill', help='指定部署的单个技能名称')
    parser.add_argument('--force', action='store_true', help='强制重新部署')
    
    args = parser.parse_args()
    
    logger.info("开始技能部署过程")
    
    # 检查技能目录是否存在
    skills_path = Path(args.skills_dir)
    if not skills_path.exists():
        logger.error(f"技能仓库目录不存在: {args.skills_dir}")
        logger.info("请先克隆技能仓库或指定正确的目录")
        sys.exit(1)
    
    # 执行部署
    success = deploy_skills(args.skills_dir, args.deployed_dir, args.skill)
    
    if success:
        logger.info("技能部署完成")
        sys.exit(0)
    else:
        logger.error("技能部署失败")
        sys.exit(1)


if __name__ == "__main__":
    main()