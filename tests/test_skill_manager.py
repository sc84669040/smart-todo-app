"""
技能管理器测试
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from src.skill_manager import SkillManager


class TestSkillManager:
    """技能管理器测试类"""
    
    def setup_method(self):
        """测试设置"""
        self.temp_dir = tempfile.mkdtemp()
        self.skills_dir = Path(self.temp_dir) / "skills"
        self.deployed_dir = Path(self.temp_dir) / "deployed"
        
        # 创建测试技能
        self._create_test_skills()
    
    def teardown_method(self):
        """测试清理"""
        shutil.rmtree(self.temp_dir)
    
    def _create_test_skills(self):
        """创建测试技能"""
        # 创建有效的技能
        valid_skill_dir = self.skills_dir / "valid-skill"
        valid_skill_dir.mkdir(parents=True)
        
        skill_content = """---
name: valid-skill
description: 这是一个有效的测试技能
version: 1.0.0
author: 测试作者
---

# 有效技能

这是一个有效的测试技能。
"""
        
        (valid_skill_dir / "SKILL.md").write_text(skill_content, encoding='utf-8')
        
        # 创建无效的技能（缺少 SKILL.md）
        invalid_skill_dir = self.skills_dir / "invalid-skill"
        invalid_skill_dir.mkdir(parents=True)
    
    def test_discover_skills(self):
        """测试发现技能"""
        manager = SkillManager(str(self.skills_dir), str(self.deployed_dir))
        skills = manager.discover_skills()
        
        assert "valid-skill" in skills
        assert "invalid-skill" not in skills  # 缺少 SKILL.md
        assert len(skills) == 1
    
    def test_load_skill_success(self):
        """测试成功加载技能"""
        manager = SkillManager(str(self.skills_dir), str(self.deployed_dir))
        skill_info = manager.load_skill("valid-skill")
        
        assert skill_info is not None
        assert skill_info['name'] == "valid-skill"
        assert 'metadata' in skill_info
        assert 'content' in skill_info
        assert skill_info['metadata']['description'] == "这是一个有效的测试技能"
    
    def test_load_skill_failure(self):
        """测试加载不存在的技能"""
        manager = SkillManager(str(self.skills_dir), str(self.deployed_dir))
        skill_info = manager.load_skill("nonexistent-skill")
        
        assert skill_info is None
    
    def test_deploy_skill(self):
        """测试部署技能"""
        manager = SkillManager(str(self.skills_dir), str(self.deployed_dir))
        
        # 部署技能
        result = manager.deploy_skill("valid-skill")
        assert result is True
        
        # 检查部署目录
        deploy_path = self.deployed_dir / "valid-skill"
        assert deploy_path.exists()
        assert (deploy_path / "SKILL.md").exists()
        assert (deploy_path / ".deployed").exists()
    
    def test_deploy_all_skills(self):
        """测试部署所有技能"""
        manager = SkillManager(str(self.skills_dir), str(self.deployed_dir))
        
        results = manager.deploy_all_skills()
        
        assert "valid-skill" in results
        assert results["valid-skill"] is True
        assert len(results) == 1
    
    def test_list_deployed_skills(self):
        """测试列出已部署技能"""
        manager = SkillManager(str(self.skills_dir), str(self.deployed_dir))
        
        # 先部署一个技能
        manager.deploy_skill("valid-skill")
        
        # 列出已部署技能
        deployed = manager.list_deployed_skills()
        
        assert len(deployed) == 1
        assert deployed[0]['name'] == "valid-skill"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])