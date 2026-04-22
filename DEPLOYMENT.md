# 🚀 Claude.ai Deployment Guide

## Quick Deployment Steps

### 1. Install Python Dependencies
```bash
cd mcp-server
pip3 install -r requirements.txt
```

### 2. Configure Environment
```bash
# Edit webhook URLs in .env file
nano .env
```

### 3. Test MCP Server
```bash
python3 tests/test_mcp_server.py
```

### 4. Configure Claude Desktop

Add this to your Claude Desktop configuration file:

**Location**: 
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

**Configuration**:
```json
{
  "mcpServers": {
    "agentic-automation-garage-v2": {
      "command": "python3",
      "args": ["teams_mcp_server.py"],
      "cwd": "/Users/ukcci1ssi/CCI/Hackathon/agentic-automation-garage-v2/mcp-server",
      "env": {
        "TEAMS_WEBHOOK_URL": "https://your-teams-webhook-url",
        "SLACK_WEBHOOK_URL": "https://your-slack-webhook-url",
        "APPROVAL_EMAIL": "your-email@company.com"
      }
    }
  }
}
```

### 5. Restart Claude Desktop

After adding the configuration, restart Claude Desktop completely.

### 6. Test Integration

In Claude, try: *"Create an approval card for creating an Azure storage account"*

## Available Commands

Once deployed, you can use these commands with Claude:

### Enterprise Workflow Commands
- *"Create a ticket for [request description]"*
- *"Generate JIRA ticket with cost estimates for [infrastructure request]"*  
- *"Post approval card to Teams for [request]"*
- *"Check for duplicate tickets before creating [request]"*
- *"Route this request: [description]"*

### Approval Workflow Commands
- *"Create Teams approval card with approve/reject buttons"*
- *"Post Slack approval message to #hackathon4-approval"*
- *"Generate cost estimate for Azure [service type]"*
- *"Assess security risk for [system change]"*

### Example Conversations

**Request Processing**:
```
User: "I need an Azure storage account for the mobile app in development"

Claude: "I'll process this request through our enterprise workflow:

1. First, let me check if this request has sufficient detail...
   ✅ Clear what is needed (Azure storage account)
   ✅ Environment specified (development)  
   ✅ Purpose clear (mobile app)

2. Checking for duplicate tickets in JIRA...
   ✅ No similar recent requests found

3. Generating structured ticket with cost/security estimates...
   💰 Cost Estimate: $10-25/month (Standard LRS, 500GB storage)
   🔒 Security Risk: Medium (requires RBAC controls, audit logging)

4. Creating Teams approval card with interactive buttons...
   ✅ Posted to Teams channel with approve/reject actions

5. Creating Slack approval message...  
   ✅ Posted to #hackathon4-approval channel

The request has been processed and sent for approval!"
```

## Troubleshooting

### Common Issues

1. **"MCP server not found"**
   - Check Claude Desktop configuration file path
   - Verify `cwd` path is correct for your system
   - Restart Claude Desktop after configuration changes

2. **"Import errors"**
   - Run: `pip3 install -r mcp-server/requirements.txt`
   - Check Python version: `python3 --version` (3.8+ required)

3. **"Webhook failed"**
   - Verify webhook URLs in `.env` file
   - Test webhooks manually with curl
   - Check Teams/Slack channel permissions

4. **"Skills not working"**  
   - Run: `python3 scripts/validate-skills.py`
   - Check skills directory structure
   - Verify SKILL.md files are properly formatted

### Debug Mode

Enable debug mode in `.env`:
```bash
DEBUG=true
LOG_LEVEL=DEBUG
```

### Validation Commands

```bash
# Check deployment readiness
python3 scripts/deployment-check.py

# Validate all skills
python3 scripts/validate-skills.py  

# Test MCP server
python3 tests/test_mcp_server.py
```

## Integration Status

- ✅ **Teams Integration**: Adaptive Cards with approve/reject buttons
- ✅ **Slack Integration**: Block Kit approval messages  
- ✅ **JIRA Integration**: Structured tickets with cost/security tables
- ✅ **Duplicate Prevention**: JIRA search integration
- ✅ **Cost Estimation**: Automatic Azure service cost calculation
- ✅ **Security Assessment**: Risk analysis and compliance checking
- ✅ **Skills Library**: 10 enterprise workflow skills
- ✅ **Claude.ai Ready**: Full MCP protocol implementation

## Next Steps After Deployment

1. **Team Onboarding**: Train team members on Claude commands
2. **Webhook Configuration**: Set up production webhook URLs
3. **JIRA Integration**: Configure JIRA API access for duplicate detection
4. **Monitoring**: Set up logging and error tracking
5. **Customization**: Add organization-specific skills and workflows

---

**🎉 Ready for Enterprise Deployment with Claude.ai!**