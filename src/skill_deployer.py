"""
技能部署器 - 负责技能的部署和配置管理

处理技能的部署、配置生成、环境设置等
"""

import os
import json
import shutil
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class SkillDeployer:
    """技能部署器类"""
    
    def __init__(self, deployed_dir: str = "deployed_skills", config_dir: str = "config"):
        """
        初始化技能部署器
        
        Args:
            deployed_dir: 已部署技能目录
            config_dir: 配置目录
        """
        self.deployed_dir = Path(deployed_dir)
        self.config_dir = Path(config_dir)
        
        # 创建必要的目录
        self.deployed_dir.mkdir(exist_ok=True)
        self.config_dir.mkdir(exist_ok=True)
        
        logger.info(f"技能部署器初始化完成")
    
    def deploy_skill(self, skill_path: Path, skill_info: Dict[str, Any]) -> bool:
        """
        部署单个技能
        
        Args:
            skill_path: 技能源路径
            skill_info: 技能信息
            
        Returns:
            部署是否成功
        """
        skill_name = skill_info['name']
        deploy_path = self.deployed_dir / skill_name
        
        try:
            # 清理旧的部署（如果存在）
            if deploy_path.exists():
                shutil.rmtree(deploy_path)
            
            # 创建部署目录
            deploy_path.mkdir(parents=True, exist_ok=True)
            
            # 复制技能文件
            self._copy_skill_files(skill_path, deploy_path)
            
            # 生成部署配置
            self._generate_deployment_config(deploy_path, skill_info)
            
            # 生成使用说明
            self._generate_usage_guide(deploy_path, skill_info)
            
            logger.info(f"技能部署成功: {skill_name}")
            return True
            
        except Exception as e:
            logger.error(f"技能部署失败 {skill_name}: {e}")
            return False
    
    def _copy_skill_files(self, src_path: Path, dst_path: Path):
        """
        复制技能文件
        
        Args:
            src_path: 源路径
            dst_path: 目标路径
        """
        # 复制 SKILL.md 文件
        skill_file = src_path / "SKILL.md"
        if skill_file.exists():
            shutil.copy2(skill_file, dst_path / "SKILL.md")
        
        # 复制资源文件
        resource_dirs = ['scripts', 'resources', 'examples', 'templates']
        
        for resource_dir in resource_dirs:
            resource_src = src_path / resource_dir
            if resource_src.exists() and resource_src.is_dir():
                resource_dst = dst_path / resource_dir
                shutil.copytree(resource_src, resource_dst, dirs_exist_ok=True)
    
    def _generate_deployment_config(self, deploy_path: Path, skill_info: Dict[str, Any]):
        """
        生成部署配置
        
        Args:
            deploy_path: 部署路径
            skill_info: 技能信息
        """
        config = {
            'skill_name': skill_info['name'],
            'metadata': skill_info.get('metadata', {}),
            'deployed_at': str(Path(deploy_path).stat().st_ctime),
            'source': skill_info.get('source', 'unknown'),
            'resources': self._discover_deployed_resources(deploy_path)
        }
        
        config_file = deploy_path / "deployment.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    
    def _discover_deployed_resources(self, deploy_path: Path) -> List[str]:
        """
        发现已部署的资源文件
        
        Args:
            deploy_path: 部署路径
            
        Returns:
            资源文件列表
        """
        resources = []
        
        for file_path in deploy_path.rglob('*'):
            if file_path.is_file() and file_path.name != "deployment.json":
                relative_path = file_path.relative_to(deploy_path)
                resources.append(str(relative_path))
        
        return resources
    
    def _generate_usage_guide(self, deploy_path: Path, skill_info: Dict[str, Any]):
        """
        生成使用说明文件
        
        Args:
            deploy_path: 部署路径
            skill_info: 技能信息
        """
        metadata = skill_info.get('metadata', {})
        content = skill_info.get('content', '')
        
        usage_content = f"""# {metadata.get('name', 'Unknown Skill')} 使用指南

## 技能描述
{metadata.get('description', '暂无描述')}

## 版本信息
- 版本: {metadata.get('version', '1.0.0')}
- 作者: {metadata.get('author', '未知')}
- 部署时间: {Path(deploy_path).stat().st_ctime}

## 技能内容
{content}

## 使用方法

1. 确保已安装必要的依赖
2. 按照技能说明进行操作
3. 如有问题，请参考技能文档

## 文件结构

```
{deploy_path.name}/
├── SKILL.md          # 技能主文件
├── deployment.json   # 部署配置
└── [其他资源文件]     # 技能相关资源
```
"""
        
        usage_file = deploy_path / "USAGE.md"
        usage_file.write_text(usage_content, encoding='utf-8')
    
    def get_deployment_status(self, skill_name: str) -> Optional[Dict[str, Any]]:
        """
        获取技能的部署状态
        
        Args:
            skill_name: 技能名称
            
        Returns:
            部署状态信息
        """
        deploy_path = self.deployed_dir / skill_name
        config_file = deploy_path / "deployment.json"
        
        if not config_file.exists():
            return None
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # 检查文件完整性
            config['files_exist'] = self._check_files_exist(deploy_path, config.get('resources', []))
            config['deploy_path'] = str(deploy_path)
            
            return config
            
        except Exception as e:
            logger.error(f"读取部署状态失败 {skill_name}: {e}")
            return None
    
    def _check_files_exist(self, deploy_path: Path, expected_files: List[str]) -> Dict[str, bool]:
        """
        检查文件是否存在
        
        Args:
            deploy_path: 部署路径
            expected_files: 期望的文件列表
            
        Returns:
            文件存在状态字典
        """
        file_status = {}
        
        for file_path in expected_files:
            full_path = deploy_path / file_path
            file_status[file_path] = full_path.exists()
        
        return file_status
    
    def undeploy_skill(self, skill_name: str) -> bool:
        """
        卸载技能
        
        Args:
            skill_name: 技能名称
            
        Returns:
            卸载是否成功
        """
        deploy_path = self.deployed_dir / skill_name
        
        if not deploy_path.exists():
            logger.warning(f"技能未部署: {skill_name}")
            return True
        
        try:
            shutil.rmtree(deploy_path)
            logger.info(f"技能卸载成功: {skill_name}")
            return True
            
        except Exception as e:
            logger.error(f"技能卸载失败 {skill_name}: {e}")
            return False
    
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
                status = self.get_deployment_status(item.name)
                if status:
                    deployed_skills.append(status)
        
        return deployed_skills
    
    def generate_skill_index(self) -> Dict[str, Any]:
        """
        生成技能索引
        
        Returns:
            技能索引信息
        """
        deployed_skills = self.list_deployed_skills()
        
        index = {
            'total_skills': len(deployed_skills),
            'skills': [],
            'categories': {},
            'last_updated': str(Path(self.deployed_dir).stat().st_mtime)
        }
        
        for skill in deployed_skills:
            skill_info = {
                'name': skill.get('skill_name'),
                'metadata': skill.get('metadata', {}),
                'deployed_at': skill.get('deployed_at'),
                'files_exist': skill.get('files_exist', {})
            }
            
            index['skills'].append(skill_info)
            
            # 按分类统计
            category = skill.get('metadata', {}).get('category', 'uncategorized')
            if category not in index['categories']:
                index['categories'][category] = 0
            index['categories'][category] += 1
        
        # 保存索引文件
        index_file = self.config_dir / "skill_index.json"
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2, ensure_ascii=False)
        
        return index


def main():
    """主函数 - 用于测试"""
    deployer = SkillDeployer()
    
    # 生成技能索引
    index = deployer.generate_skill_index()
    print(f"技能索引: {index}")
    
    # 列出已部署技能
    deployed = deployer.list_deployed_skills()
    print(f"已部署技能数量: {len(deployed)}")


if __name__ == "__main__":
    main()