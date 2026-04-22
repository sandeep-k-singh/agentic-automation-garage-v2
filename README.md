# Agentic Automation Garage v2

## 🎯 Purpose
Multi-agentic automation platform for enterprise workflow management with Claude.ai integration.

## 🏗️ Architecture
- **MCP Server**: Python-based Model Context Protocol server for Claude.ai
- **Skills**: Modular workflow skills for ticket routing, approvals, and integrations  
- **Integrations**: Teams, Slack, JIRA, Halo service management
- **Deployment**: Ready for Claude Desktop and Claude.ai connector deployment

## 📦 Components

### Core MCP Server (`/mcp-server/`)
- **Python MCP Server**: Production-ready server with 3 core tools
- **Teams Integration**: Adaptive Cards approval workflow
- **Slack Integration**: Block Kit approval messages  
- **Service Management**: JIRA and Halo ticket creation

### Skills Library (`/skills/`)
- **ticket-intake-router**: Converts requests to structured tickets with duplicate checking
- **jira-payload-formatting**: JIRA ticket creation with cost/security estimates
- **halo-payload-formatting**: Halo service request formatting
- **Slack Approval Workflow**: Complete Slack integration skills
- **Teams Approval Workflow**: Microsoft Teams integration skills

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Claude Desktop installed
- Azure/Teams webhook configured (optional)
- Slack webhook configured (optional)

### Installation

1. **Clone and Setup**:
   ```bash
   cd agentic-automation-garage-v2
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r mcp-server/requirements.txt
   ```

2. **Configure Environment**:
   ```bash
   cp mcp-server/.env.example mcp-server/.env
   # Edit .env with your webhook URLs and API keys
   ```

3. **Configure Claude Desktop**:
   - Add MCP server configuration to Claude Desktop settings
   - See `claude-desktop-config.json` for example configuration

4. **Start MCP Server**:
   ```bash
   cd mcp-server
   python -m teams_mcp_server
   ```

### Claude Desktop Configuration

Add to your Claude Desktop `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "agentic-automation-garage-v2": {
      "command": "python",
      "args": ["-m", "teams_mcp_server"],
      "cwd": "/path/to/agentic-automation-garage-v2/mcp-server",
      "env": {
        "TEAMS_WEBHOOK_URL": "your-teams-webhook-url",
        "SLACK_WEBHOOK_URL": "your-slack-webhook-url"
      }
    }
  }
}
```

## 🔧 Configuration

### Environment Variables
- `TEAMS_WEBHOOK_URL`: Microsoft Teams incoming webhook URL
- `SLACK_WEBHOOK_URL`: Slack incoming webhook URL  
- `JIRA_API_TOKEN`: JIRA API token (optional)
- `HALO_API_KEY`: Halo PSA API key (optional)

### Webhook Setup
- **Teams**: Create incoming webhook in Teams channel
- **Slack**: Create incoming webhook in Slack workspace
- **Testing**: Use provided test scripts to verify integration

## 📚 Skills Documentation

Each skill in `/skills/` contains:
- `SKILL.md`: Detailed usage instructions
- Implementation examples
- Integration requirements
- Validation rules

### Key Skills:
- **ticket-intake-router**: Main entry point for all requests
- **jira-payload-formatting**: Enterprise JIRA integration
- **slack-approval-workflow**: Complete Slack approval process

## 🧪 Testing

### Test Scripts:
- `test-teams-integration.py`: Verify Teams webhook
- `test-slack-integration.js`: Verify Slack webhook  
- `test-complete-workflow.py`: End-to-end workflow testing

### Run Tests:
```bash
python test-teams-integration.py
node test-slack-integration.js
```

## 🔄 Workflow Examples

### 1. Simple Request Processing:
```
User: "Create an Azure storage account for dev environment"
→ ticket-intake-router (clarification check, duplicate check)
→ jira-payload-formatting (structured ticket with cost/security estimates)
→ Slack approval workflow (post to #hackathon4-approval)
→ Teams notification (adaptive card with approve/reject)
```

### 2. Access Request:
```
User: "I need access to production database"
→ ticket-intake-router (routes to Halo)
→ halo-payload-formatting (service request format)
→ Teams approval workflow
```

## 🏢 Enterprise Features

- **Cost Estimation**: Automatic Azure service cost calculation
- **Security Assessment**: Risk analysis and compliance checking
- **Duplicate Prevention**: JIRA integration for duplicate ticket detection
- **Approval Workflows**: Multi-channel approval processes
- **Audit Trail**: Complete tracking from request to completion

## 📋 Status

- ✅ Teams MCP Server (95% success rate)
- ✅ Python MCP Server (Production ready)
- ✅ Slack Integration (Block Kit approval cards)
- ✅ JIRA Integration (Cost/security estimates in tables)
- ✅ Duplicate Detection (JIRA search integration)
- ✅ Claude.ai Connector Ready

## 🚨 Troubleshooting

### Common Issues:
1. **MCP Server Connection**: Check Claude Desktop configuration and Python path
2. **Webhook Failures**: Verify webhook URLs and permissions
3. **Skill Validation**: Review skill documentation for required parameters

### Debug Mode:
```bash
export DEBUG=1
python -m teams_mcp_server
```

## 📈 Roadmap

- [ ] Azure deployment automation
- [ ] Enhanced JIRA field mapping
- [ ] ServiceNow integration
- [ ] Advanced workflow orchestration
- [ ] Multi-tenant configuration

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new functionality  
4. Update skill documentation
5. Submit pull request

## 📄 License

MIT License - See LICENSE file for details

---

**Ready for enterprise deployment with Claude.ai integration** 🚀