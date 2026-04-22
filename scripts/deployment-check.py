#!/usr/bin/env python3
"""
Deployment Check Script for Agentic Automation Garage v2
Validates Claude.ai deployment readiness
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple

def check_python_version() -> Tuple[bool, str]:
    """Check if Python version is 3.11+"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 11:
        return True, f"✅ Python {version.major}.{version.minor}.{version.micro}"
    return False, f"❌ Python {version.major}.{version.minor}.{version.micro} (requires 3.11+)"

def check_dependencies() -> Tuple[bool, str]:
    """Check if required Python packages are available"""
    required = ["httpx", "pydantic", "mcp"]
    missing = []
    
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        return False, f"❌ Missing packages: {', '.join(missing)}"
    return True, "✅ All dependencies available"

def check_mcp_server() -> Tuple[bool, str]:
    """Check if MCP server file exists and is executable"""
    mcp_file = Path("mcp-server/teams_mcp_server.py")
    if not mcp_file.exists():
        return False, "❌ MCP server file not found"
    
    if not os.access(mcp_file, os.R_OK):
        return False, "❌ MCP server file not readable"
    
    return True, "✅ MCP server file ready"

def check_requirements() -> Tuple[bool, str]:
    """Check if requirements.txt exists"""
    req_file = Path("mcp-server/requirements.txt")
    if not req_file.exists():
        return False, "❌ requirements.txt not found"
    return True, "✅ Requirements file found"

def check_claude_config() -> Tuple[bool, str]:
    """Check if Claude Desktop config exists"""
    config_file = Path("claude-desktop-config.json")
    if not config_file.exists():
        return False, "❌ Claude Desktop config not found"
    
    try:
        with open(config_file) as f:
            config = json.load(f)
        
        if "mcpServers" not in config:
            return False, "❌ No mcpServers in Claude config"
        
        if "agentic-automation-garage-v2" not in config["mcpServers"]:
            return False, "❌ MCP server not configured in Claude config"
        
        return True, "✅ Claude Desktop config valid"
    except json.JSONDecodeError:
        return False, "❌ Claude Desktop config invalid JSON"

def check_skills() -> Tuple[bool, str]:
    """Check if skills directory and key skills exist"""
    skills_dir = Path("skills")
    if not skills_dir.exists():
        return False, "❌ Skills directory not found"
    
    key_skills = [
        "ticket-intake-router/SKILL.md",
        "jira-payload-formatting/SKILL.md",
        "slack-approval-workflow/SKILL.md"
    ]
    
    missing_skills = []
    for skill in key_skills:
        if not (skills_dir / skill).exists():
            missing_skills.append(skill)
    
    if missing_skills:
        return False, f"❌ Missing key skills: {', '.join(missing_skills)}"
    
    return True, "✅ All key skills present"

def check_environment() -> Tuple[bool, str]:
    """Check if environment variables can be loaded"""
    env_file = Path("mcp-server/.env.example")
    if not env_file.exists():
        return False, "❌ .env.example not found"
    
    # Check if user has created .env file
    user_env = Path("mcp-server/.env")
    if not user_env.exists():
        return False, "⚠️  .env file not created (copy from .env.example)"
    
    return True, "✅ Environment configuration ready"

def check_webhooks() -> Tuple[bool, str]:
    """Check if webhook URLs are configured"""
    env_file = Path("mcp-server/.env")
    if not env_file.exists():
        return False, "⚠️  No .env file to check webhook URLs"
    
    with open(env_file) as f:
        content = f.read()
    
    teams_configured = "TEAMS_WEBHOOK_URL=" in content and "https://" in content
    slack_configured = "SLACK_WEBHOOK_URL=" in content and "hooks.slack.com" in content
    
    if teams_configured and slack_configured:
        return True, "✅ Both Teams and Slack webhooks configured"
    elif teams_configured:
        return True, "⚠️  Teams webhook configured, Slack webhook missing"
    elif slack_configured:
        return True, "⚠️  Slack webhook configured, Teams webhook missing"
    else:
        return False, "❌ No webhooks configured"

def main():
    """Run all deployment checks"""
    print("🚀 Agentic Automation Garage v2 - Deployment Check")
    print("=" * 55)
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("MCP Server", check_mcp_server),
        ("Requirements", check_requirements),
        ("Claude Config", check_claude_config),
        ("Skills", check_skills),
        ("Environment", check_environment),
        ("Webhooks", check_webhooks),
    ]
    
    all_passed = True
    results = []
    
    for name, check_func in checks:
        try:
            passed, message = check_func()
            results.append((name, passed, message))
            if not passed and not message.startswith("⚠️"):
                all_passed = False
        except Exception as e:
            results.append((name, False, f"❌ Error: {str(e)}"))
            all_passed = False
    
    # Display results
    for name, passed, message in results:
        print(f"{name:15} | {message}")
    
    print("\n" + "=" * 55)
    
    if all_passed:
        print("🎉 All checks passed! Ready for Claude.ai deployment")
        print("\nNext steps:")
        print("1. Copy claude-desktop-config.json to your Claude Desktop settings")
        print("2. Restart Claude Desktop")
        print("3. Start using the MCP server with Claude")
        return 0
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("- Run: pip install -r mcp-server/requirements.txt")
        print("- Copy: cp mcp-server/.env.example mcp-server/.env")
        print("- Edit .env file with your webhook URLs")
        return 1

if __name__ == "__main__":
    exit(main())