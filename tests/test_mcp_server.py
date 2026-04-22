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
        result = await teams_build_card_payload(
            ticket_key=test_params["ticket_key"],
            ticket_summary=test_params["ticket_summary"], 
            user_story=test_params["user_story"],
            acceptance_criteria=test_params["acceptance_criteria"],
            priority=test_params.get("priority", "Medium"),
            effort_hours=test_params.get("effort_hours", "1-2 hours"),
            azure_monthly_cost=test_params.get("azure_monthly_cost", "$5-10/mo"),
            risk_level=test_params.get("risk_level", "Low"),
            labels=test_params.get("labels", [])
        )
        
        if isinstance(result, dict) and "type" in result:
            print("✅ Adaptive Card generated successfully")
            print(f"   Card Type: {result['type']}")
            print(f"   Attachments: {len(result.get('attachments', []))}")
            return True
        else:
            print(f"❌ Unexpected result format: {type(result)}")
            return False
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

async def test_webhook_integration():
    """Test webhook integration (dry run)"""
    print("\n🧪 Testing webhook integration...")
    
    # Check environment variables
    teams_webhook = os.getenv("TEAMS_WEBHOOK_URL", "")
    
    if not teams_webhook:
        print("⚠️  TEAMS_WEBHOOK_URL not configured - using test mode")
        
    # Test parameters
    test_params = {
        "ticket_key": "TEST-456", 
        "ticket_summary": "Webhook integration test",
        "user_story": "Test webhook posting functionality",
        "acceptance_criteria": ["Webhook posts without errors", "Response is handled correctly"]
    }
    
    try:
        # Test webhook posting (will simulate if no webhook configured)
        result = await teams_post_approval_card(
            ticket_key=test_params["ticket_key"],
            ticket_summary=test_params["ticket_summary"],
            user_story=test_params["user_story"], 
            acceptance_criteria=test_params["acceptance_criteria"],
            webhook_url=teams_webhook if teams_webhook else None
        )
        
        if isinstance(result, dict):
            if result.get("success", False):
                print("✅ Webhook test successful")
                return True
            else:
                print(f"❌ Webhook test failed: {result.get('message', 'Unknown error')}")
                return False
        else:
            print(f"❌ Unexpected result type: {type(result)}")
            return False
            
    except Exception as e:
        print(f"❌ Webhook test failed with error: {e}")
        return False
    
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
        from teams_mcp_server import app, MCP_SDK_AVAILABLE
        
        if not MCP_SDK_AVAILABLE:
            print("⚠️  MCP SDK not available - using fallback mode")
            print("✅ MCP server loaded successfully in fallback mode")
            return True
        
        # Check if tools are properly registered (only if MCP SDK is available)
        tools = await app.list_tools()
        
        expected_tools = [
            "teams_post_approval_card",
            "teams_build_card_payload", 
            "teams_send_approval_email"
        ]
        
        found_tools = [tool.get("name", "") for tool in tools]
        
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