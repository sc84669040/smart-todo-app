"""
技能加载器 - 负责技能的解析和验证

处理 SKILL.md 文件的 YAML 头部解析、Markdown 内容处理等
"""

import re
import yaml
import logging
from typing import Dict, Any, Optional, List
from pathlib import Path

logger = logging.getLogger(__name__)


class SkillLoader:
    """技能加载器类"""
    
    def __init__(self):
        """初始化技能加载器"""
        self.required_metadata = ['name', 'description']
        self.optional_metadata = ['version', 'author', 'tags', 'category']
    
    def parse_skill_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """
        解析技能文件
        
        Args:
            file_path: 技能文件路径
            
        Returns:
            解析后的技能信息
        """
        try:
            content = file_path.read_text(encoding='utf-8')
            return self.parse_skill_content(content, str(file_path))
        except Exception as e:
            logger.error(f"解析技能文件失败 {file_path}: {e}")
            return None
    
    def parse_skill_content(self, content: str, source: str = "unknown") -> Optional[Dict[str, Any]]:
        """
        解析技能内容
        
        Args:
            content: 技能内容文本
            source: 内容来源标识
            
        Returns:
            解析后的技能信息
        """
        try:
            # 检查是否包含 YAML 头部
            if not content.startswith('---'):
                logger.warning(f"技能内容缺少 YAML 头部: {source}")
                return None
            
            # 分割 YAML 头部和 Markdown 内容
            parts = content.split('---', 2)
            if len(parts) < 3:
                logger.warning(f"技能内容格式不正确: {source}")
                return None
            
            yaml_content = parts[1].strip()
            markdown_content = parts[2].strip()
            
            # 解析 YAML 元数据
            metadata = yaml.safe_load(yaml_content) or {}
            
            # 验证必需字段
            missing_fields = [field for field in self.required_metadata if field not in metadata]
            if missing_fields:
                logger.warning(f"技能缺少必需字段 {missing_fields}: {source}")
                return None
            
            # 提取技能名称（从文件名或元数据）
            skill_name = metadata.get('name', 'unknown')
            
            # 解析 Markdown 内容
            parsed_content = self._parse_markdown_content(markdown_content)
            
            skill_info = {
                'name': skill_name,
                'metadata': metadata,
                'content': markdown_content,
                'parsed_content': parsed_content,
                'source': source
            }
            
            logger.info(f"成功解析技能: {skill_name}")
            return skill_info
            
        except yaml.YAMLError as e:
            logger.error(f"YAML 解析错误 {source}: {e}")
            return None
        except Exception as e:
            logger.error(f"解析技能内容失败 {source}: {e}")
            return None
    
    def _parse_markdown_content(self, content: str) -> Dict[str, Any]:
        """
        解析 Markdown 内容，提取结构化信息
        
        Args:
            content: Markdown 内容
            
        Returns:
            结构化信息字典
        """
        parsed = {
            'sections': [],
            'examples': [],
            'guidelines': [],
            'commands': []
        }
        
        lines = content.split('\n')
        current_section = None
        
        for line in lines:
            # 检测章节标题
            if line.startswith('#'):
                level = len(line) - len(line.lstrip('#'))
                title = line.lstrip('#').strip()
                
                current_section = {
                    'level': level,
                    'title': title,
                    'content': []
                }
                parsed['sections'].append(current_section)
            
            # 检测示例
            elif line.strip().startswith('- Example:'):
                example = line.replace('- Example:', '').strip()
                parsed['examples'].append(example)
            
            # 检测指南
            elif line.strip().startswith('- Guideline:'):
                guideline = line.replace('- Guideline:', '').strip()
                parsed['guidelines'].append(guideline)
            
            # 检测代码块
            elif line.strip().startswith('```'):
                # 这里可以进一步解析代码块内容
                pass
            
            # 添加到当前章节内容
            elif current_section and line.strip():
                current_section['content'].append(line.strip())
        
        return parsed
    
    def validate_skill(self, skill_info: Dict[str, Any]) -> Dict[str, List[str]]:
        """
        验证技能信息的完整性
        
        Args:
            skill_info: 技能信息字典
            
        Returns:
            验证结果 {错误类型: [错误消息]}
        """
        errors = {
            'metadata': [],
            'content': [],
            'structure': []
        }
        
        # 验证元数据
        metadata = skill_info.get('metadata', {})
        for field in self.required_metadata:
            if field not in metadata:
                errors['metadata'].append(f"缺少必需字段: {field}")
        
        # 验证内容
        content = skill_info.get('content', '')
        if not content.strip():
            errors['content'].append("技能内容为空")
        
        # 验证结构
        parsed_content = skill_info.get('parsed_content', {})
        if not parsed_content.get('sections'):
            errors['structure'].append("技能缺少章节结构")
        
        return errors
    
    def extract_skill_commands(self, skill_info: Dict[str, Any]) -> List[str]:
        """
        从技能内容中提取命令模式
        
        Args:
            skill_info: 技能信息
            
        Returns:
            命令模式列表
        """
        commands = []
        content = skill_info.get('content', '')
        
        # 查找命令模式（以 "命令:" 或 "Command:" 开头的行）
        command_patterns = [
            r'命令:\s*(.+)',
            r'Command:\s*(.+)',
            r'Usage:\s*(.+)',
            r'用法:\s*(.+)'
        ]
        
        for pattern in command_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE | re.MULTILINE)
            commands.extend(matches)
        
        return commands


def main():
    """主函数 - 用于测试"""
    loader = SkillLoader()
    
    # 示例技能内容
    sample_skill = """---
name: test-skill
description: 这是一个测试技能
version: 1.0.0
author: 测试作者
---

# 测试技能

这是一个测试技能的说明。

## 示例
- Example: 使用示例1
- Example: 使用示例2

## 指南
- Guideline: 指南1
- Guideline: 指南2
"""
    
    # 解析技能
    skill_info = loader.parse_skill_content(sample_skill, "test")
    if skill_info:
        print(f"技能名称: {skill_info['name']}")
        print(f"技能描述: {skill_info['metadata']['description']}")
        print(f"章节数量: {len(skill_info['parsed_content']['sections'])}")
        
        # 验证技能
        errors = loader.validate_skill(skill_info)
        print(f"验证结果: {errors}")
        
        # 提取命令
        commands = loader.extract_skill_commands(skill_info)
        print(f"提取的命令: {commands}")


if __name__ == "__main__":
    main()