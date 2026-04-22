#!/usr/bin/env node
/**
 * Post Approval Card to Slack - Hackathon4 Approval Channel
 * 
 * Demonstrates posting a Block Kit approval card to #hackathon4-approval
 */

// Use built-in fetch (Node.js 18+) or fallback to https module
const fetch = globalThis.fetch || (async (url, options) => {
  const https = await import('https');
  const { URL } = await import('url');
  
  return new Promise((resolve, reject) => {
    const parsedUrl = new URL(url);
    const requestOptions = {
      hostname: parsedUrl.hostname,
      port: parsedUrl.port || 443,
      path: parsedUrl.pathname + parsedUrl.search,
      method: options.method || 'GET',
      headers: options.headers || {}
    };
    
    const req = https.request(requestOptions, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        resolve({
          ok: res.statusCode >= 200 && res.statusCode < 300,
          status: res.statusCode,
          text: () => Promise.resolve(data),
          json: () => Promise.resolve(JSON.parse(data))
        });
      });
    });
    
    req.on('error', reject);
    if (options.body) req.write(options.body);
    req.end();
  });
});

// Sample approval card data for demonstration
const sampleTicketData = {
  "route": "jira",
  "title": "Deploy AI Automation Assistant to Azure", 
  "user_story": "As a hackathon team, I want to deploy our AI automation assistant to Azure so that we can demonstrate real-time ticket processing and approval workflows to stakeholders.",
  "acceptance_criteria": [
    "Azure App Service deployed with proper scaling configuration",
    "Database migration completed successfully",
    "Teams and Slack integrations are fully functional",
    "Security scanning and compliance checks pass",
    "Load testing confirms system can handle expected traffic",
    "Monitoring and alerting configured for production readiness"
  ],
  "priority": "P1",
  "labels": ["hackathon", "azure-deployment", "ai-assistant", "production"],
  "cost_estimate": {
    "effort_hours": "4-6 hours",
    "complexity": "High", 
    "azure_monthly_cost": "Estimated monthly cost: $150-300 (App Service, Database, Storage)"
  },
  "security_estimate": {
    "risk_level": "Medium",
    "security_requirements": ["HTTPS enforcement", "Authentication", "API rate limiting", "Data encryption"],
    "compliance_impact": "Production deployment requires security review"
  },
  "requestor": "hackathon-team@company.com",
  "approval_id": "HACK4-2026-001", 
  "ticket_id": "HACK-4567",
  "ticket_url": "https://company.atlassian.net/browse/HACK-4567"
};

// Generate Block Kit message using slack-approval-card skill format
function generateSlackApprovalCard(data) {
  const priorityEmojis = {
    "P1": "🔴",
    "P2": "🟡", 
    "P3": "🔵",
    "P4": "🟢"
  };
  
  const formattedCriteria = data.acceptance_criteria
    .map(criteria => `• ${criteria}`)
    .join('\n');
    
  const securityReqs = Array.isArray(data.security_estimate.security_requirements) 
    ? data.security_estimate.security_requirements.join(', ')
    : data.security_estimate.security_requirements;
    
  const labelsText = data.labels.join(' ');

  return {
    "blocks": [
      {
        "type": "header",
        "text": {
          "type": "plain_text",
          "text": "🎯 Hackathon4 Approval Required"
        }
      },
      {
        "type": "section",
        "text": {
          "type": "mrkdwn",
          "text": `*${priorityEmojis[data.priority]} ${data.priority} | ${data.title}*`
        },
        "accessory": {
          "type": "button",
          "text": {
            "type": "plain_text",
            "text": "View Ticket"
          },
          "url": data.ticket_url,
          "action_id": "view_ticket"
        }
      },
      {
        "type": "divider"
      },
      {
        "type": "section",
        "text": {
          "type": "mrkdwn",
          "text": `*📋 Request Details*\n${data.user_story}`
        }
      },
      {
        "type": "section",
        "fields": [
          {
            "type": "mrkdwn",
            "text": `*💰 Effort & Cost*\n${data.cost_estimate.effort_hours}\n${data.cost_estimate.azure_monthly_cost}`
          },
          {
            "type": "mrkdwn", 
            "text": `*🔒 Security Risk*\n${data.security_estimate.risk_level}\n${securityReqs}`
          }
        ]
      },
      {
        "type": "section",
        "text": {
          "type": "mrkdwn",
          "text": `*✅ Acceptance Criteria*\n${formattedCriteria}`
        }
      },
      {
        "type": "section",
        "text": {
          "type": "mrkdwn",
          "text": `*📊 Labels*\n\`${labelsText}\``
        }
      },
      {
        "type": "divider"
      },
      {
        "type": "actions",
        "elements": [
          {
            "type": "button",
            "text": {
              "type": "plain_text",
              "text": "✅ Approve"
            },
            "style": "primary",
            "action_id": "approve_request",
            "value": data.approval_id
          },
          {
            "type": "button", 
            "text": {
              "type": "plain_text",
              "text": "❌ Reject"
            },
            "style": "danger",
            "action_id": "reject_request",
            "value": data.approval_id
          }
        ]
      },
      {
        "type": "context",
        "elements": [
          {
            "type": "mrkdwn",
            "text": `Requested by: ${data.requestor} | ID: ${data.approval_id} | Ticket: <${data.ticket_url}|${data.ticket_id}>`
          }
        ]
      }
    ]
  };
}

// Post to Slack using webhook (requires actual webhook URL)
async function postToSlackWebhook(webhookUrl, blockKitMessage) {
  try {
    console.log('🚀 Posting to Slack webhook...');
    console.log(`📍 Target: #hackathon4-approval`);
    console.log(`🔗 Webhook: ${webhookUrl.substring(0, 50)}...`);
    
    const response = await fetch(webhookUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(blockKitMessage)
    });
    
    if (response.ok) {
      return {
        status: "success",
        message: "Block Kit message posted successfully to #hackathon4-approval",
        channel: "#hackathon4-approval",
        workspace: "Hackathon4",
        method: "webhook", 
        posted_at: new Date().toISOString(),
        response_status: response.status,
        blocks_posted: blockKitMessage.blocks.length
      };
    } else {
      const errorText = await response.text();
      return {
        status: "error",
        error_type: "webhook_failure", 
        message: "Failed to post to Slack channel",
        error_details: `HTTP ${response.status}: ${errorText}`,
        channel: "#hackathon4-approval",
        attempted_at: new Date().toISOString()
      };
    }
  } catch (error) {
    return {
      status: "error",
      error_type: "network_error",
      message: "Network error posting to Slack",
      error_details: error.message,
      attempted_at: new Date().toISOString()
    };
  }
}

// Main execution
async function main() {
  console.log('🎯 Hackathon4 Slack Approval Card Poster');
  console.log('=========================================');
  
  // Generate the approval card
  console.log('\n📝 Generating Block Kit approval card...');
  const approvalCard = generateSlackApprovalCard(sampleTicketData);
  console.log(`✅ Generated card with ${approvalCard.blocks.length} blocks`);
  
  // Display card payload for reference
  console.log('\n📋 Generated Block Kit Message:');
  console.log(JSON.stringify(approvalCard, null, 2));
  
  // Check for webhook URL
  const webhookUrl = process.env.HACKATHON4_SLACK_WEBHOOK || 
                     process.env.SLACK_WEBHOOK_URL ||
                     'WEBHOOK_URL_NEEDED';
  
  if (webhookUrl === 'WEBHOOK_URL_NEEDED') {
    console.log('\n⚠️  WEBHOOK URL REQUIRED');
    console.log('==========================================');
    console.log('To post to #hackathon4-approval, set one of:');
    console.log('• HACKATHON4_SLACK_WEBHOOK="https://hooks.slack.com/services/..."');
    console.log('• SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."');
    console.log('');
    console.log('🔧 To get webhook URL:');
    console.log('1. Go to https://api.slack.com/apps');
    console.log('2. Select your app or create new one');
    console.log('3. Go to "Incoming Webhooks"'); 
    console.log('4. Create webhook for #hackathon4-approval channel');
    console.log('5. Copy webhook URL and set environment variable');
    console.log('');
    console.log('📄 Card ready - just need webhook URL to post!');
    return;
  }
  
  // Post to Slack
  console.log('\n📡 Posting to #hackathon4-approval...');
  const result = await postToSlackWebhook(webhookUrl, approvalCard);
  
  console.log('\n📊 Result:');
  console.log(JSON.stringify(result, null, 2));
  
  if (result.status === 'success') {
    console.log('\n🎉 SUCCESS! Approval card posted to #hackathon4-approval');
    console.log(`📅 Posted at: ${result.posted_at}`);
    console.log(`📦 Blocks: ${result.blocks_posted}`);
    console.log('👆 Users can now click Approve/Reject buttons');
  } else {
    console.log('\n❌ FAILED to post to Slack channel');
    console.log(`🔍 Error: ${result.error_details}`);
    console.log('\n🛠️  Troubleshooting:');
    console.log('• Verify webhook URL is correct and active');
    console.log('• Check #hackathon4-approval channel exists');
    console.log('• Ensure webhook is configured for correct channel');
  }
}

if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch(console.error);
}

export { generateSlackApprovalCard, postToSlackWebhook };