#!/usr/bin/env python3
"""
Skills Validation Script for Agentic Automation Garage v2
Validates all skills are properly formatted and complete
"""

import os
import re
import yaml
from pathlib import Path
from typing import Dict, List, Tuple, Optional

def validate_skill_metadata(skill_path: Path) -> Tuple[bool, str, Optional[Dict]]:
    """Validate skill metadata (YAML front matter)"""
    try:
        with open(skill_path / "SKILL.md", 'r') as f:
            content = f.read()
        
        # Extract YAML front matter
        if not content.startswith('---'):
            return False, "No YAML front matter found", None
        
        yaml_end = content.find('---', 3)
        if yaml_end == -1:
            return False, "YAML front matter not properly closed", None
        
        yaml_content = content[3:yaml_end].strip()
        try:
            metadata = yaml.safe_load(yaml_content)
        except yaml.YAMLError as e:
            return False, f"Invalid YAML: {e}", None
        
        # Check required fields
        required_fields = ['name', 'description', 'version']
        missing_fields = [field for field in required_fields if field not in metadata]
        
        if missing_fields:
            return False, f"Missing required fields: {', '.join(missing_fields)}", None
        
        return True, "Valid metadata", metadata
    
    except FileNotFoundError:
        return False, "SKILL.md not found", None
    except Exception as e:
        return False, f"Error reading file: {e}", None

def validate_skill_structure(skill_path: Path) -> Tuple[bool, str]:
    """Validate skill structure and required sections"""
    try:
        with open(skill_path / "SKILL.md", 'r') as f:
            content = f.read()
        
        # Check for required sections
        required_sections = [
            "# ",  # Title
            "## Purpose",
            "## Responsibilities" 
        ]
        
        missing_sections = []
        for section in required_sections:
            if section not in content:
                missing_sections.append(section.replace("## ", "").replace("# ", "Title"))
        
        if missing_sections:
            return False, f"Missing sections: {', '.join(missing_sections)}"
        
        # Check for output format if it's a formatting skill
        if "formatting" in skill_path.name:
            if "## Output Format" not in content and "Output format" not in content:
                return False, "Formatting skill missing Output Format section"
        
        return True, "Valid structure"
    
    except Exception as e:
        return False, f"Error validating structure: {e}"

def validate_skill_dependencies(skill_path: Path, metadata: Dict) -> Tuple[bool, str]:
    """Validate skill dependencies and integration points"""
    try:
        with open(skill_path / "SKILL.md", 'r') as f:
            content = f.read()
        
        skill_name = metadata.get('name', '')
        
        # Check integration requirements for specific skills
        if skill_name == "ticket-intake-router":
            required_patterns = [
                "clarification",
                "duplicate",
                "JIRA",
                "Slack",
                "Output Format"
            ]
        elif skill_name == "jira-payload-formatting":
            required_patterns = [
                "customfield",
                "ADF",
                "priority",
                "labels"
            ]
        elif "slack" in skill_name:
            required_patterns = [
                "Block Kit",
                "webhook",
                "channel"
            ]
        elif "teams" in skill_name:
            required_patterns = [
                "Adaptive Card",
                "webhook",
                "Action.Submit"
            ]
        else:
            required_patterns = []
        
        missing_patterns = []
        for pattern in required_patterns:
            if pattern not in content:
                missing_patterns.append(pattern)
        
        if missing_patterns:
            return False, f"Missing required content: {', '.join(missing_patterns)}"
        
        return True, "Dependencies validated"
    
    except Exception as e:
        return False, f"Error validating dependencies: {e}"

def validate_json_examples(skill_path: Path) -> Tuple[bool, str]:
    """Validate JSON examples in skill documentation"""
    try:
        with open(skill_path / "SKILL.md", 'r') as f:
            content = f.read()
        
        # Find JSON code blocks
        json_blocks = re.findall(r'```json\n(.*?)\n```', content, re.DOTALL)
        
        invalid_json = []
        for i, json_block in enumerate(json_blocks):
            try:
                import json
                json.loads(json_block)
            except json.JSONDecodeError as e:
                invalid_json.append(f"Block {i+1}: {str(e)[:50]}...")
        
        if invalid_json:
            return False, f"Invalid JSON examples: {'; '.join(invalid_json)}"
        
        return True, f"All {len(json_blocks)} JSON examples valid" if json_blocks else "No JSON to validate"
    
    except Exception as e:
        return False, f"Error validating JSON: {e}"

def main():
    """Validate all skills in the skills directory"""
    print("🔍 Agentic Automation Garage v2 - Skills Validation")
    print("=" * 55)
    
    skills_dir = Path("skills")
    if not skills_dir.exists():
        print("❌ Skills directory not found")
        return 1
    
    skill_dirs = [d for d in skills_dir.iterdir() if d.is_dir() and (d / "SKILL.md").exists()]
    
    if not skill_dirs:
        print("❌ No skills found")
        return 1
    
    all_valid = True
    results = []
    
    for skill_dir in sorted(skill_dirs):
        skill_name = skill_dir.name
        print(f"\n📋 Validating: {skill_name}")
        
        # Run all validations
        validations = [
            ("Metadata", lambda: validate_skill_metadata(skill_dir)),
            ("Structure", lambda: validate_skill_structure(skill_dir)),
            ("JSON Examples", lambda: validate_json_examples(skill_dir))
        ]
        
        skill_valid = True
        metadata = None
        
        for val_name, val_func in validations:
            try:
                if val_name == "Metadata":
                    passed, message, metadata = val_func()
                else:
                    passed, message = val_func()
                
                status = "✅" if passed else "❌"
                print(f"  {val_name:15} | {status} {message}")
                
                if not passed:
                    skill_valid = False
                    all_valid = False
            
            except Exception as e:
                print(f"  {val_name:15} | ❌ Error: {str(e)}")
                skill_valid = False
                all_valid = False
        
        # Dependencies validation (requires metadata)
        if metadata:
            try:
                passed, message = validate_skill_dependencies(skill_dir, metadata)
                status = "✅" if passed else "❌"
                print(f"  {'Dependencies':15} | {status} {message}")
                if not passed:
                    skill_valid = False
                    all_valid = False
            except Exception as e:
                print(f"  {'Dependencies':15} | ❌ Error: {str(e)}")
                skill_valid = False
                all_valid = False
        
        results.append((skill_name, skill_valid))
    
    # Summary
    print("\n" + "=" * 55)
    print("📊 Validation Summary:")
    
    valid_count = sum(1 for _, valid in results if valid)
    total_count = len(results)
    
    for skill_name, valid in results:
        status = "✅" if valid else "❌"
        print(f"  {skill_name:25} | {status}")
    
    print(f"\n✅ Valid: {valid_count}/{total_count}")
    
    if all_valid:
        print("🎉 All skills validated successfully!")
        return 0
    else:
        print("❌ Some skills need fixes. See details above.")
        return 1

if __name__ == "__main__":
    exit(main())