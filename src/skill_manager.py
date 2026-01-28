"""
技能管理器 - 核心技能管理功能

负责技能的加载、验证、部署和管理
"""

import os
import yaml
import logging
from typing import Dict, List, Optional, Any
from pathlib import Path

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class SkillManager:
    """技能管理器类"""
    
    def __init__(self, skills_dir: str = "skills", deployed_dir: str = "deployed_skills"):
        """
        初始化技能管理器
        
        Args:
            skills_dir: 技能仓库目录
            deployed_dir: 已部署技能目录
        """
        self.skills_dir = Path(skills_dir)
        self.deployed_dir = Path(deployed_dir)
        self.skills: Dict[str, Dict[str, Any]] = {}
        
        # 创建必要的目录
        self.skills_dir.mkdir(exist_ok=True)
        self.deployed_dir.mkdir(exist_ok=True)
        
        logger.info(f"技能管理器初始化完成 - 技能目录: {self.skills_dir}")
    
    def discover_skills(self) -> List[str]:
        """
        发现技能仓库中的所有技能
        
        Returns:
            技能名称列表
        """
        skills = []
        
        if not self.skills_dir.exists():
            logger.warning(f"技能目录不存在: {self.skills_dir}")
            return skills
        
        # 遍历技能目录，寻找包含 SKILL.md 的文件夹
        for item in self.skills_dir.iterdir():
            if item.is_dir():
                skill_file = item / "SKILL.md"
                if skill_file.exists():
                    skills.append(item.name)
                    logger.debug(f"发现技能: {item.name}")
        
        logger.info(f"共发现 {len(skills)} 个技能")
        return skills
    
    def load_skill(self, skill_name: str) -> Optional[Dict[str, Any]]:
        """
        加载单个技能的信息
        
        Args:
            skill_name: 技能名称
            
        Returns:
            技能信息字典，包含元数据和内容
        """
        skill_path = self.skills_dir / skill_name
        skill_file = skill_path / "SKILL.md"
        
        if not skill_file.exists():
            logger.error(f"技能文件不存在: {skill_file}")
            return None
        
        try:
            # 读取技能文件
            content = skill_file.read_text(encoding='utf-8')
            
            # 解析 YAML 头部和 Markdown 内容
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    yaml_content = parts[1].strip()
                    markdown_content = parts[2].strip()
                    
                    # 解析 YAML
                    metadata = yaml.safe_load(yaml_content) or {}
                    
                    skill_info = {
                        'name': skill_name,
                        'metadata': metadata,
                        'content': markdown_content,
                        'path': str(skill_path),
                        'resources': self._discover_resources(skill_path)
                    }
                    
                    logger.info(f"成功加载技能: {skill_name}")
                    return skill_info
                
            logger.warning(f"技能文件格式不正确: {skill_file}")
            return None
            
        except Exception as e:
            logger.error(f"加载技能失败 {skill_name}: {e}")
            return None
    
    def _discover_resources(self, skill_path: Path) -> List[str]:
        """
        发现技能的资源文件
        
        Args:
            skill_path: 技能路径
            
        Returns:
            资源文件列表
        """
        resources = []
        
        # 常见的资源目录
        resource_dirs = ['scripts', 'resources', 'examples', 'templates']
        
        for resource_dir in resource_dirs:
            resource_path = skill_path / resource_dir
            if resource_path.exists() and resource_path.is_dir():
                # 递归收集所有文件
                for file_path in resource_path.rglob('*'):
                    if file_path.is_file():
                        relative_path = file_path.relative_to(skill_path)
                        resources.append(str(relative_path))
        
        return resources
    
    def deploy_skill(self, skill_name: str) -> bool:
        """
        部署单个技能到已部署目录
        
        Args:
            skill_name: 技能名称
            
        Returns:
            部署是否成功
        """
        skill_info = self.load_skill(skill_name)
        if not skill_info:
            logger.error(f"无法加载技能，部署失败: {skill_name}")
            return False
        
        try:
            # 创建部署目录
            deploy_path = self.deployed_dir / skill_name
            deploy_path.mkdir(exist_ok=True)
            
            # 复制技能文件
            skill_file = self.skills_dir / skill_name / "SKILL.md"
            deploy_file = deploy_path / "SKILL.md"
            
            # 复制主文件
            deploy_file.write_text(skill_file.read_text(encoding='utf-8'), encoding='utf-8')
            
            # 复制资源文件
            for resource in skill_info['resources']:
                src_path = self.skills_dir / skill_name / resource
                dst_path = deploy_path / resource
                
                # 创建目标目录
                dst_path.parent.mkdir(parents=True, exist_ok=True)
                
                # 复制文件
                dst_path.write_bytes(src_path.read_bytes())
            
            # 创建部署标记文件
            deploy_marker = deploy_path / ".deployed"
            deploy_marker.write_text(f"deployed_at: {os.path.getmtime(str(skill_file))}")
            
            logger.info(f"技能部署成功: {skill_name}")
            return True
            
        except Exception as e:
            logger.error(f"技能部署失败 {skill_name}: {e}")
            return False
    
    def deploy_all_skills(self) -> Dict[str, bool]:
        """
        部署所有发现的技能
        
        Returns:
            部署结果字典 {技能名: 是否成功}
        """
        skills = self.discover_skills()
        results = {}
        
        logger.info(f"开始部署 {len(skills)} 个技能")
        
        for skill_name in skills:
            results[skill_name] = self.deploy_skill(skill_name)
        
        # 统计结果
        success_count = sum(1 for result in results.values() if result)
        logger.info(f"技能部署完成 - 成功: {success_count}/{len(skills)}")
        
        return results
    
    def list_deployed_skills(self) -> List[Dict[str, Any]]:
        """
        列出所有已部署的技能
        
        Returns:
            已部署技能信息列表
        """
        deployed_skills = []
        
        if not self.deployed_dir.exists():
            return deployed_skills
        
        for item in self.deployed_dir.iterdir():
            if item.is_dir():
                skill_file = item / "SKILL.md"
                if skill_file.exists():
                    skill_info = self.load_skill(item.name)
                    if skill_info:
                        deployed_skills.append(skill_info)
        
        return deployed_skills


def main():
    """主函数 - 用于测试"""
    manager = SkillManager()
    
    # 发现技能
    skills = manager.discover_skills()
    print(f"发现的技能: {skills}")
    
    # 部署技能
    if skills:
        results = manager.deploy_all_skills()
        print(f"部署结果: {results}")
    
    # 列出已部署技能
    deployed = manager.list_deployed_skills()
    print(f"已部署技能数量: {len(deployed)}")


if __name__ == "__main__":
    main()