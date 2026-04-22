---
name: email-approval-card
description: Converts Teams approval card into an email format and sends to Outlook shared mailbox for approval workflows
version: 1.0.0
---

# Email Approval Card Skill

## Purpose
Convert a Teams approval card into an HTML email format and send it to an Outlook shared mailbox for approval workflows.

## Input
The input should be JSON containing the approval card data and email configuration:

{
  "request_data": {
    "route": "jira",
    "title": "Create Azure storage account for demo environment",
    "user_story": "As a demo team member, I want an Azure storage account...",
    "acceptance_criteria": ["Criterion 1", "Criterion 2"],
    "priority": "P2",
    "labels": ["ai-generated", "slack-intake", "azure"],
    "cost_estimate": {
      "effort_hours": "2-4 hours",
      "complexity": "Medium",
      "azure_monthly_cost": "$15-30"
    },
    "security_estimate": {
      "risk_level": "Medium",
      "security_requirements": ["RBAC", "Private endpoints"]
    },
    "requestor": "user@company.com",
    "approval_id": "APPR-2026-045"
  },
  "email_config": {
    "shared_mailbox": "cloudplatformteam@bauermediaoutdoor.com",
    "from_address": "sandeep.singh@bauermediaoutdoor.com",
    "smtp_server": "smtp.office365.com",
    "smtp_port": 587
  }
}

## Your job
Convert the approval card data into an HTML email and send it to the Outlook shared mailbox with approve/reject functionality.

## Rules
- Generate HTML email with approval card content
- Include priority-based styling and color coding
- Add approve/reject buttons with callback URLs
- Use professional email template design
- Set appropriate email subject line
- Include all cost and security information
- Add email headers for proper threading
- Use SMTP authentication for Office 365

## Email Template Structure
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Approval Request: {title}</title>
    <style>
        /* Priority-based color schemes */
        .priority-p1 { border-left: 5px solid #FF4444; background-color: #FFF5F5; }
        .priority-p2 { border-left: 5px solid #FF8C00; background-color: #FFF8F0; }
        .priority-p3 { border-left: 5px solid #32CD32; background-color: #F5FFF5; }
        .priority-p4 { border-left: 5px solid #1E90FF; background-color: #F0F8FF; }
        
        .container { max-width: 600px; margin: 0 auto; padding: 20px; font-family: Arial, sans-serif; }
        .header { background-color: #0078d4; color: white; padding: 15px; border-radius: 5px 5px 0 0; }
        .content { padding: 20px; border: 1px solid #ddd; border-radius: 0 0 5px 5px; }
        .cost-box { background-color: #f0f8ff; padding: 10px; border-radius: 5px; margin: 10px 0; }
        .security-box { background-color: #fff8dc; padding: 10px; border-radius: 5px; margin: 10px 0; }
        .actions { text-align: center; padding: 20px; }
        .approve-btn { background-color: #28a745; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 10px; display: inline-block; }
        .reject-btn { background-color: #dc3545; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 10px; display: inline-block; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>🎫 Approval Request: {title}</h2>
            <p>Priority: {priority} | ID: {approval_id}</p>
        </div>
        <div class="content priority-{priority_class}">
            <h3>📋 Request Details</h3>
            <p><strong>User Story:</strong> {user_story}</p>
            
            <h4>✅ Acceptance Criteria</h4>
            <ul>{acceptance_criteria_list}</ul>
            
            <div class="cost-box">
                <h4>💰 Cost Estimate</h4>
                <p><strong>Effort:</strong> {effort_hours}</p>
                <p><strong>Complexity:</strong> {complexity}</p>
                <p><strong>Azure Monthly Cost:</strong> {azure_monthly_cost}</p>
            </div>
            
            <div class="security-box">
                <h4>🔒 Security Assessment</h4>
                <p><strong>Risk Level:</strong> {risk_level}</p>
                <p><strong>Requirements:</strong> {security_requirements}</p>
            </div>
            
            <p><strong>Requestor:</strong> {requestor}</p>
            <p><strong>Labels:</strong> {labels}</p>
        </div>
        
        <div class="actions">
            <a href="{approve_url}" class="approve-btn">✅ APPROVE</a>
            <a href="{reject_url}" class="reject-btn">❌ REJECT</a>
        </div>
        
        <div style="font-size: 12px; color: #666; text-align: center; margin-top: 20px;">
            <p>This is an automated approval request. Click the buttons above to approve or reject.</p>
            <p>Approval ID: {approval_id} | Generated on {timestamp}</p>
        </div>
    </div>
</body>
</html>
```

## Email Subject Line Format
- **P1 (Critical)**: 🚨 URGENT APPROVAL NEEDED: {title}
- **P2 (High)**: ⚡ APPROVAL REQUIRED: {title}
- **P3 (Medium)**: 📋 Approval Request: {title}
- **P4 (Low)**: 📝 Review Request: {title}

## SMTP Configuration
```javascript
const smtpConfig = {
  host: 'smtp.office365.com',
  port: 587,
  secure: false, // true for 465, false for other ports
  auth: {
    user: process.env.BAUER_EMAIL,
    pass: process.env.BAUER_APP_PASSWORD
  },
  tls: {
    ciphers: 'SSLv3'
  }
};
```

## Approval URL Configuration
Generate callback URLs for approve/reject actions:
- **Approve URL**: `https://approvals.bauermediaoutdoor.com/api/approve?id={approval_id}&token={security_token}`
- **Reject URL**: `https://approvals.bauermediaoutdoor.com/api/reject?id={approval_id}&token={security_token}`

## Output format
Return JSON status with email details:

Success response:
{
  "status": "success",
  "message": "Approval email sent successfully to shared mailbox",
  "email_details": {
    "to": "cloudplatformteam@bauermediaoutdoor.com",
    "subject": "📋 Approval Request: Create Azure storage account",
    "message_id": "12345@bauermediaoutdoor.com",
    "sent_at": "2026-04-21T10:30:00Z"
  },
  "approval_urls": {
    "approve": "https://approvals.bauermediaoutdoor.com/api/approve?id=APPR-2026-045&token=abc123",
    "reject": "https://approvals.bauermediaoutdoor.com/api/reject?id=APPR-2026-045&token=abc123"
  }
}

Failure response:
{
  "status": "error",
  "error_type": "smtp_failure",
  "message": "Failed to send approval email",
  "error_details": "SMTP authentication failed - check credentials",
  "attempted_at": "2026-04-21T10:30:00Z",
  "troubleshooting": "Verify SMTP settings and app password for shared mailbox"
}

## Error Handling
- **SMTP Authentication Error**: Check app password and shared mailbox permissions
- **Email Format Error**: Validate HTML template and variable substitution
- **Network Timeout**: Retry with exponential backoff
- **Rate Limiting**: Implement sending delays for bulk emails
- **Invalid Email Address**: Validate email format before sending

## Environment Variables
Required environment variables:
- `BAUER_EMAIL` - Shared mailbox email address (cloudplatformteam@bauermediaoutdoor.com)
- `BAUER_APP_PASSWORD` - App-specific password for authentication
- `APPROVAL_BASE_URL` - Base URL for approval callbacks  
- `APPROVAL_SECURITY_TOKEN` - Token for URL security

## Integration Notes
- Works with Office 365 shared mailboxes
- Supports HTML email with embedded styling
- Includes approve/reject callback URLs
- Can be chained after ticket creation
- Maintains audit trail through email threading
- Supports priority-based visual styling

## Security Considerations
- Use app-specific passwords for SMTP authentication
- Include security tokens in approval URLs
- Validate callback URL signatures
- Log all approval email activity
- Encrypt sensitive data in email content
- Use HTTPS for all callback URLs

## Usage Example
```javascript
// 1. Generate approval email
const emailResult = await sendApprovalEmail({
  request_data: structuredTicketData,
  email_config: {
    shared_mailbox: "cloudplatformteam@bauermediaoutdoor.com",
    from_address: "sandeep.singh@bauermediaoutdoor.com"
  }
});

// 2. Handle result
if (emailResult.status === "success") {
  console.log("Approval email sent:", emailResult.email_details.message_id);
} else {
  console.error("Failed to send email:", emailResult.error_details);
}
```