---
name: teams-approval-workflow  
description: Complete workflow skill that generates Teams approval cards and sends them via email to Outlook shared mailbox
version: 2.0.0
---

# Teams Approval Workflow Skill

## Purpose
Orchestrate the complete approval workflow: generate approval card + send via email to Outlook shared mailbox in one skill.

## Input
The input should be the structured request data plus email configuration:

{
  "route": "jira",
  "title": "Create Azure storage account for demo environment", 
  "user_story": "As a demo team member, I want an Azure storage account...",
  "acceptance_criteria": [...],
  "priority": "P2",
  "labels": ["ai-generated", "slack-intake", "azure"],
  "cost_estimate": {
    "effort_hours": "2-4 hours",
    "complexity": "Medium", 
    "azure_monthly_cost": "$15-30"
  },
  "security_estimate": {
    "risk_level": "Medium",
    "security_requirements": ["RBAC controls", "Private endpoints"]
  },
  "requestor": "john.doe@company.com",
  "approval_id": "APPR-2026-045",
  "ticket_id": "CLOUDREQ-1234",
  "ticket_url": "https://company.atlassian.net/browse/CLOUDREQ-1234",
  "email_config": {
    "shared_mailbox": "cloudplatformteam@bauermediaoutdoor.com",
    "from_address": "sandeep.singh@bauermediaoutdoor.com",
    "smtp_server": "smtp.office365.com",
    "smtp_port": 587
  }
}

## Your job
1. Generate Teams approval card using teams-approval-card skill
2. Send the card via email using email-approval-card skill  
3. Return combined workflow status

## Rules
- Chain both skills in sequence
- Pass request data to teams-approval-card skill first
- Take generated card and send via email using email-approval-card skill
- Handle failures at each step gracefully
- Return comprehensive workflow status
- Include card generation AND email sending results
- Provide clear error messages for troubleshooting

## Email Routing Logic
Route approval emails based on:
- **Priority**: P1 requests → Include URGENT in subject line and CC management
- **Labels**: Infrastructure requests → CC infrastructure team  
- **Cost**: High-cost requests (>$100/month) → CC finance team
- **Default**: Standard shared mailbox (cloudplatformteam@bauermediaoutdoor.com)

## Output format
Success response:
{
  "workflow_status": "success",
  "message": "Approval card generated and sent via email successfully",
  "card_generation": {
    "status": "success", 
    "card_type": "adaptive_card",
    "priority_color": "warning"
  },
  "email_sending": {
    "status": "success",
    "to": "cloudplatformteam@bauermediaoutdoor.com", 
    "subject": "📋 Approval Request: Create Azure storage account",
    "message_id": "12345@bauermediaoutdoor.com",
    "sent_at": "2026-04-21T10:30:00Z"
  },
  "approval_tracking": {
    "approval_id": "APPR-2026-045",
    "ticket_id": "CLOUDREQ-1234",
    "approval_urls": {
      "approve": "https://approvals.bauermediaoutdoor.com/api/approve?id=APPR-2026-045",
      "reject": "https://approvals.bauermediaoutdoor.com/api/reject?id=APPR-2026-045"
    }
  }
}

Failure response:
{
  "workflow_status": "error",
  "failed_at": "card_generation | email_sending",
  "message": "Failed to complete email approval workflow",
  "card_generation": {
    "status": "success | error",
    "error_details": "..."
  },
  "email_sending": {
    "status": "error", 
    "error_type": "smtp_failure",
    "error_details": "SMTP authentication failed"
  },
  "troubleshooting": "Check email configuration and SMTP credentials"
}

## Workflow Steps
1. **Validate Input**: Check required fields and Teams configuration
2. **Generate Card**: Use teams-approval-card skill to create adaptive card
3. **Route Channel**: Determine target channel based on routing logic  
4. **Post Card**: Use teams-post-card skill to send to Teams
5. **Return Status**: Provide complete workflow results

## Channel Routing Examples
```javascript
// Priority-based routing
if (priority === "P1") {
  webhook_url = process.env.TEAMS_URGENT_WEBHOOK;
  channel_name = "Urgent-Approvals";
}

// Label-based routing  
if (labels.includes("infrastructure")) {
  webhook_url = process.env.TEAMS_INFRASTRUCTURE_WEBHOOK;
  channel_name = "Infrastructure-Requests";
}

// Cost-based routing
const monthlyCost = extractCostAmount(cost_estimate.azure_monthly_cost);
if (monthlyCost > 100) {
  webhook_url = process.env.TEAMS_MANAGEMENT_WEBHOOK;
  channel_name = "High-Cost-Approvals";
}
```

## Error Recovery
- If card generation fails → Return card error details
- If Teams posting fails → Return webhook error + retry suggestion
- If both succeed → Return success with tracking info
- Log all steps for debugging workflow issues

## Integration Usage
```javascript
// Complete approval workflow in one call
const workflowResult = await runEmailApprovalWorkflow({
  ...structuredRequest,
  email_config: {
    shared_mailbox: "cloudplatformteam@bauermediaoutdoor.com",
    from_address: "sandeep.singh@bauermediaoutdoor.com",
    smtp_server: "smtp.office365.com"
  }
});

if (workflowResult.workflow_status === "success") {
  console.log(`Approval email sent to ${workflowResult.email_sending.to}`);
} else {
  console.error(`Workflow failed at: ${workflowResult.failed_at}`);
}
```

## Environment Dependencies
- SMTP configuration for Bauer Media Outdoor email system
- Approval callback endpoints for button actions  
- Access to teams-approval-card and email-approval-card skills

**Example Configuration:**
```bash
# Email configuration (Bauer Media Outdoor)
BAUER_EMAIL="cloudplatformteam@bauermediaoutdoor.com"
BAUER_APP_PASSWORD="your-app-specific-password"
APPROVAL_BASE_URL="https://approvals.bauermediaoutdoor.com"

# Additional email addresses (configure as needed) 
BAUER_URGENT_EMAIL="urgent@bauermediaoutdoor.com"
BAUER_INFRASTRUCTURE_EMAIL="infrastructure@bauermediaoutdoor.com"
```

## Best Practices
- Always validate email configuration before attempting to send
- Include approval_id in all tracking for correlation
- Route emails to appropriate addresses based on request type
- Provide clear error messages for troubleshooting
- Log workflow steps for audit and debugging purposes