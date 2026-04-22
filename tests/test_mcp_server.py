#!/usr/bin/env python3
"""
Test script for Teams MCP Server integration
"""

import asyncio
import json
import sys
import os
from pathlib import Path

# Add mcp-server directory to path
sys.path.append(str(Path(__file__).parent.parent / "mcp-server"))

try:
    from teams_mcp_server import teams_post_approval_card, teams_build_card_payload
except ImportError as e:
    print(f"❌ Cannot import MCP server modules: {e}")
    print("Make sure you're running from the project root and dependencies are installed.")
    sys.exit(1)

async def test_card_generation():
    """Test Adaptive Card generation"""
    print("🧪 Testing Adaptive Card generation...")
    
    test_params = {
        "ticket_key": "TEST-123",
        "ticket_summary": "Test deployment check for MCP server",
        "user_story": "As a developer, I want to test the MCP server deployment so that I can verify it works correctly with Claude.ai",
        "priority": "Medium · P3",
        "effort_hours": "1-2 hours",
        "azure_monthly_cost": "$5-10/mo",
        "risk_level": "Low",
        "acceptance_criteria": [
            "MCP server starts without errors",
            "Adaptive cards generate correctly",
            "Test webhook integration works",
            "Claude.ai can connect successfully"
        ],
        "labels": ["test", "deployment", "mcp-server", "ai-generated"]
    }
    
    try:
        # Test card payload generation
        result = await teams_build_card_payload(test_params)
        
        if result.isError:
            print(f"❌ Card generation failed: {result.content[0].text}")
            return False
        
        print("✅ Card generation successful")
        
        # Parse and validate the JSON structure
        try:
            card_json = json.loads(result.content[0].text)
            
            # Check required structure
            if "attachments" in card_json and len(card_json["attachments"]) > 0:
                adaptive_card = card_json["attachments"][0]["content"]
                
                if "actions" in adaptive_card and len(adaptive_card["actions"]) == 2:
                    print("✅ Approve/Reject buttons found")
                else:
                    print("⚠️  Approve/Reject buttons not found or incorrect count")
                
                if "body" in adaptive_card and len(adaptive_card["body"]) > 0:
                    print("✅ Card body content found")
                else:
                    print("❌ Card body content missing")
                
            else:
                print("❌ Invalid card structure")
                return False
        
        except json.JSONDecodeError:
            print("❌ Card payload is not valid JSON")
            return False
        
        return True
    
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

async def test_webhook_integration():
    """Test webhook integration (dry run)"""
    print("\n🧪 Testing webhook integration...")
    
    # Check environment variables
    teams_webhook = os.getenv("TEAMS_WEBHOOK_URL", "")
    
    if not teams_webhook:
        print("⚠️  TEAMS_WEBHOOK_URL not configured - webhook posting will fail")
        return True  # This is expected for testing
    
    if "webhook.office.com" not in teams_webhook:
        print("⚠️  TEAMS_WEBHOOK_URL doesn't look like a Teams webhook")
        return False
    
    print("✅ Teams webhook URL configured")
    
    # Test actual posting (commented out to avoid spam)
    # Uncomment the following lines to test actual webhook posting:
    
    # test_params = {
    #     "ticket_key": "DEPLOY-TEST",
    #     "ticket_summary": "MCP Server Deployment Test",
    #     "user_story": "Testing MCP server webhook integration",
    #     "acceptance_criteria": ["Webhook posts successfully"]
    # }
    # 
    # result = await teams_post_approval_card(test_params)
    # if result.isError:
    #     print(f"❌ Webhook test failed: {result.content[0].text}")
    #     return False
    # 
    # print("✅ Webhook test successful")
    
    return True

async def test_mcp_tools():
    """Test MCP tool availability"""
    print("\n🧪 Testing MCP tools...")
    
    try:
        # Import MCP server components
        from teams_mcp_server import app
        
        # Check if tools are properly registered
        tools = await app.list_tools()
        
        expected_tools = [
            "teams_post_approval_card",
            "teams_build_card_payload",
            "teams_send_approval_email"
        ]
        
        found_tools = [tool.name for tool in tools]
        
        for expected_tool in expected_tools:
            if expected_tool in found_tools:
                print(f"✅ Tool '{expected_tool}' registered")
            else:
                print(f"❌ Tool '{expected_tool}' not found")
                return False
        
        print(f"✅ All {len(expected_tools)} tools registered successfully")
        return True
    
    except Exception as e:
        print(f"❌ MCP tools test failed: {e}")
        return False

async def main():
    """Run all tests"""
    print("🚀 Agentic Automation Garage v2 - MCP Server Tests")
    print("=" * 55)
    
    tests = [
        ("Card Generation", test_card_generation),
        ("Webhook Integration", test_webhook_integration),
        ("MCP Tools", test_mcp_tools)
    ]
    
    all_passed = True
    
    for test_name, test_func in tests:
        try:
            passed = await test_func()
            if not passed:
                all_passed = False
        except Exception as e:
            print(f"❌ {test_name} failed with error: {e}")
            all_passed = False
    
    print("\n" + "=" * 55)
    
    if all_passed:
        print("🎉 All tests passed! MCP server is ready for Claude.ai")
        print("\nNext steps:")
        print("1. Configure Claude Desktop with the provided config")
        print("2. Start Claude Desktop")
        print("3. Test with Claude: 'Create a test approval card for Azure storage account'")
    else:
        print("❌ Some tests failed. Check the issues above.")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit(asyncio.run(main()))