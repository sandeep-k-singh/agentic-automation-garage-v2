# 🔐 Configuration Setup Guide

## Required Configuration

After cloning this repository, you need to configure your environment:

### 1. Create Environment File
```bash
cd mcp-server
cp .env.example .env
```

### 2. Configure Webhook URLs

Edit `mcp-server/.env` with your actual webhook URLs:

```bash
# Replace with your actual Teams webhook URL
TEAMS_WEBHOOK_URL=https://your-organization.webhook.office.com/webhookb2/your-webhook-id

# Replace with your actual Slack webhook URL  
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK

# Replace with your actual email
APPROVAL_EMAIL=your-email@company.com
```

### 3. Configure Claude Desktop

Edit your Claude Desktop configuration file with your actual paths:

**Location**:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

**Update the `cwd` path** to your actual directory:
```json
{
  "mcpServers": {
    "agentic-automation-garage-v2": {
      "command": "python3",
      "args": ["teams_mcp_server.py"],
      "cwd": "/your/actual/path/to/agentic-automation-garage-v2/mcp-server",
      "env": {
        "TEAMS_WEBHOOK_URL": "your-actual-teams-webhook-url",
        "SLACK_WEBHOOK_URL": "your-actual-slack-webhook-url", 
        "APPROVAL_EMAIL": "your-email@company.com"
      }
    }
  }
}
```

## Security Notes

- **Never commit webhook URLs** or sensitive data to git
- The `.env` file is ignored by git for security
- Use `.env.example` as a template for configuration
- All example URLs in the repository are placeholders

## Getting Webhook URLs

### Teams Webhook:
1. Go to your Teams channel
2. Click "..." → "Connectors" → "Incoming Webhook"
3. Create new webhook and copy the URL

### Slack Webhook:
1. Go to https://api.slack.com/apps
2. Create new app → "Incoming Webhooks"
3. Activate and create webhook for your channel
4. Copy the webhook URL

## Quick Start

```bash
# 1. Configure environment
cp mcp-server/.env.example mcp-server/.env
nano mcp-server/.env

# 2. Install dependencies  
cd mcp-server
pip3 install -r requirements.txt

# 3. Test MCP server
python3 ../tests/test_mcp_server.py

# 4. Configure Claude Desktop
# (Edit claude_desktop_config.json as shown above)

# 5. Restart Claude Desktop and test!
```

## Support

If you encounter issues:
1. Run `python3 scripts/deployment-check.py` to validate setup
2. Check webhook URLs are correct and active
3. Verify Python dependencies are installed
4. Ensure Claude Desktop configuration is valid JSON

---

**🚀 Ready for enterprise deployment!**