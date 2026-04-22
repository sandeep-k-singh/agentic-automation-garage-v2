#!/usr/bin/env python3
"""
Teams MCP Server - Claude.ai Connector

A Model Context Protocol (MCP) server for posting Adaptive Cards to Microsoft Teams
and generating email notifications for Jira tickets.

Optimized for Claude.ai MCP connector deployment.
"""

import asyncio
import json
import logging
import os
from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass

try:
    import httpx
    from pydantic import BaseModel, Field
    DEPENDENCIES_OK = True
except ImportError:
    print("Missing dependencies. Install with: pip install httpx pydantic python-dotenv")
    DEPENDENCIES_OK = False
    exit(1)

try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import (
        CallToolResult,
        TextContent,
    )
    MCP_SDK_AVAILABLE = True
except ImportError:
    print("MCP SDK not available. This version provides core functionality only.")
    MCP_SDK_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration from environment variables
TEAMS_WEBHOOK_URL = os.getenv(
    "TEAMS_WEBHOOK_URL",
    "https://clearchannelint.webhook.office.com/webhookb2/eefeea19-a884-453f-862f-9b990ea5763b@1623e08b-aca1-49c6-b577-89c5bd4aa7b4/IncomingWebhook/9a1e2caf6bb940ac9829939638697dd9/f2c771bb-566e-48b5-91ae-d077c9e81035/V28x-tIx4FYXndxqW1eQ3jW9wWXkD4u_5xsdeo7rI2mDE1"
)

APPROVAL_EMAIL = os.getenv("APPROVAL_EMAIL", "sandeep.singh@bauermediaoutdoor.com")
JIRA_BASE_URL = os.getenv("JIRA_BASE_URL", "https://cci-clearchannel.atlassian.net/browse")

# Data Models
@dataclass
class TeamsCard:
    ticket_key: str
    ticket_summary: str
    user_story: str
    priority: str
    effort_hours: str
    azure_monthly_cost: str
    risk_level: str
    acceptance_criteria: List[str]
    labels: List[str]
    jira_url: str
    date: str

class TicketCardParams(BaseModel):
    ticket_key: str = Field(..., description="Jira ticket key e.g. TCLOUD-2721")
    ticket_summary: str = Field(..., description="Short summary of the ticket")
    user_story: str = Field(..., description="Full user story text")
    priority: str = Field(default="Medium · P2", description="Priority label e.g. 'Medium · P2'")
    effort_hours: str = Field(default="2–4 hours", description="Effort estimate e.g. '2–4 hours'")
    azure_monthly_cost: str = Field(default="$5–$20 / mo", description="Azure monthly cost estimate")
    risk_level: str = Field(default="Low", description="Risk level: Low / Medium / High / Critical")
    acceptance_criteria: List[str] = Field(..., description="List of acceptance criteria strings")
    labels: List[str] = Field(default=["ai-generated"], description="List of labels e.g. ['azure', 'storage', 'ai-generated']")
    webhook_url: Optional[str] = Field(None, description="Override Teams webhook URL. Falls back to TEAMS_WEBHOOK_URL env var if omitted.")
    date: Optional[str] = Field(None, description="Date string for the card. Defaults to today.")
    recipient_email: Optional[str] = Field(None, description="Override recipient email for email tool")

# Business Logic Functions
def build_card(params: TicketCardParams) -> TeamsCard:
    """Build TeamsCard object from parameters"""
    today = datetime.now().strftime("%d %b %Y")
    
    return TeamsCard(
        ticket_key=params.ticket_key,
        ticket_summary=params.ticket_summary,
        user_story=params.user_story,
        priority=params.priority,
        effort_hours=params.effort_hours,
        azure_monthly_cost=params.azure_monthly_cost,
        risk_level=params.risk_level,
        acceptance_criteria=params.acceptance_criteria,
        labels=params.labels,
        jira_url=f"{JIRA_BASE_URL}/{params.ticket_key}",
        date=params.date or today,
    )

def build_adaptive_card(card: TeamsCard) -> Dict[str, Any]:
    """Build Adaptive Card JSON payload"""
    ac_items = [
        {
            "type": "TableRow",
            "cells": [
                {
                    "type": "TableCell",
                    "items": [{"type": "TextBlock", "text": ac, "wrap": True, "size": "Small"}],
                }
            ],
        }
        for ac in card.acceptance_criteria
    ]

    return {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "type": "AdaptiveCard",
                    "version": "1.4",
                    "body": [
                        {
                            "type": "Container",
                            "style": "emphasis",
                            "bleed": True,
                            "items": [
                                {
                                    "type": "ColumnSet",
                                    "columns": [
                                        {
                                            "type": "Column",
                                            "width": "stretch",
                                            "items": [
                                                {
                                                    "type": "TextBlock",
                                                    "text": "New ticket approval request",
                                                    "weight": "Bolder",
                                                    "size": "Medium",
                                                    "color": "Light",
                                                },
                                                {
                                                    "type": "TextBlock",
                                                    "text": f"Tech-Cloud · {card.ticket_key} · {card.date}",
                                                    "size": "Small",
                                                    "color": "Light",
                                                    "spacing": "None",
                                                },
                                            ],
                                        }
                                    ],
                                }
                            ],
                        },
                        {
                            "type": "Container",
                            "items": [
                                {
                                    "type": "TextBlock",
                                    "text": card.ticket_summary,
                                    "weight": "Bolder",
                                    "size": "Medium",
                                    "wrap": True,
                                },
                                {
                                    "type": "TextBlock",
                                    "text": card.user_story,
                                    "wrap": True,
                                    "isSubtle": True,
                                    "size": "Small",
                                    "spacing": "Small",
                                },
                            ],
                        },
                        {
                            "type": "FactSet",
                            "facts": [
                                {"title": "Priority", "value": card.priority},
                                {"title": "Effort", "value": card.effort_hours},
                                {"title": "Est. monthly cost", "value": card.azure_monthly_cost},
                                {"title": "Risk level", "value": card.risk_level},
                                {"title": "Labels", "value": ", ".join(card.labels)},
                            ],
                        },
                        {
                            "type": "Container",
                            "items": [
                                {
                                    "type": "TextBlock",
                                    "text": "Acceptance criteria",
                                    "weight": "Bolder",
                                    "size": "Small",
                                    "spacing": "Medium",
                                },
                                {
                                    "type": "Table",
                                    "gridStyle": "accent",
                                    "firstRowAsHeader": False,
                                    "columns": [{"width": 1}],
                                    "rows": ac_items,
                                },
                            ],
                        },
                    ],
                    "actions": [
                        {
                            "type": "Action.Submit",
                            "title": "✅ Approve",
                            "style": "positive",
                            "data": {
                                "action": "approve",
                                "ticket_key": card.ticket_key,
                                "timestamp": card.date
                            }
                        },
                        {
                            "type": "Action.Submit",
                            "title": "❌ Reject",
                            "style": "destructive",
                            "data": {
                                "action": "reject",
                                "ticket_key": card.ticket_key,
                                "timestamp": card.date
                            }
                        },
                        {
                            "type": "Action.OpenUrl",
                            "title": "🔗 View in Jira",
                            "url": card.jira_url,
                        }
                    ],
                    "msteams": {"width": "Full"},
                },
            }
        ],
    }

async def post_card_to_teams(webhook_url: str, card: TeamsCard) -> Dict[str, Any]:
    """Post Adaptive Card to Teams webhook"""
    payload = build_adaptive_card(card)
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                webhook_url,
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200 and response.text.strip() == "1":
                return {
                    "success": True,
                    "message": f"Card successfully posted to Teams for {card.ticket_key}",
                    "webhook_url": webhook_url[:50] + "...",
                }
            
            return {
                "success": False,
                "message": f"Unexpected response from Teams webhook: {response.status_code} - {response.text}",
            }
            
    except httpx.RequestError as e:
        return {
            "success": False,
            "message": f"Failed to post to Teams: {str(e)}",
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Unexpected error posting to Teams: {str(e)}",
        }

def build_approval_email_html(card: TeamsCard) -> str:
    """Build HTML email for approval notification"""
    ac_items = "".join(
        f'<li style="margin-bottom:4px">{ac}</li>' 
        for ac in card.acceptance_criteria
    )
    
    labels = "".join(
        f'<span style="display:inline-block;background:#f1f0f0;border-radius:4px;padding:2px 8px;font-size:11px;margin-right:4px;color:#555">{label}</span>'
        for label in card.labels
    )
    
    return f"""
<div style="font-family:sans-serif;max-width:600px;margin:0 auto;border:1px solid #e0e0e0;border-radius:8px;overflow:hidden">
  <div style="background:#464EB8;padding:16px 20px">
    <p style="margin:0;font-size:15px;font-weight:bold;color:#fff">New ticket approval request</p>
    <p style="margin:4px 0 0;font-size:12px;color:#AFA9EC">Tech-Cloud · {card.ticket_key} · {card.date}</p>
  </div>
  <div style="padding:20px">
    <p style="font-size:16px;font-weight:bold;margin:0 0 6px;color:#1a1a1a">{card.ticket_summary}</p>
    <p style="font-size:13px;color:#666;margin:0 0 16px;line-height:1.5">{card.user_story}</p>
    
    <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:16px">
      <tr style="border-bottom:1px solid #f0f0f0">
        <td style="padding:8px 0;color:#888;width:160px">Priority</td>
        <td style="padding:8px 0;font-weight:500;color:#1a1a1a">{card.priority}</td>
      </tr>
      <tr style="border-bottom:1px solid #f0f0f0">
        <td style="padding:8px 0;color:#888">Effort</td>
        <td style="padding:8px 0;color:#1a1a1a">{card.effort_hours}</td>
      </tr>
      <tr style="border-bottom:1px solid #f0f0f0">
        <td style="padding:8px 0;color:#888">Est. monthly cost</td>
        <td style="padding:8px 0;color:#1a1a1a">{card.azure_monthly_cost}</td>
      </tr>
      <tr style="border-bottom:1px solid #f0f0f0">
        <td style="padding:8px 0;color:#888">Risk level</td>
        <td style="padding:8px 0;color:#1a1a1a">{card.risk_level}</td>
      </tr>
    </table>
    
    <div style="margin-bottom:16px">
      <p style="font-size:12px;color:#888;text-transform:uppercase;letter-spacing:0.05em;margin:0 0 8px">Acceptance criteria</p>
      <ul style="margin:0;padding-left:18px;font-size:13px;color:#333;line-height:1.6">{ac_items}</ul>
    </div>
    
    <div style="margin-bottom:20px">{labels}</div>
    
    <a href="{card.jira_url}" style="display:inline-block;padding:10px 24px;background:#464EB8;color:#fff;text-decoration:none;border-radius:6px;font-size:13px;font-weight:500">View in Jira →</a>
  </div>
  <div style="background:#f9f9f9;padding:12px 20px;font-size:11px;color:#aaa;border-top:1px solid #e0e0e0">
    Generated by Teams MCP Server · {card.date} · Reply to add a comment to the Jira ticket
  </div>
</div>""".strip()

# MCP Server Setup
app = Server("teams-mcp-server")

@app.list_tools()
async def list_tools() -> list:
    """List available MCP tools"""
    return [
        {
            "name": "teams_post_approval_card",
            "description": "Posts an Adaptive Card approval notification to a Microsoft Teams channel via an incoming webhook. Use this tool after a Jira ticket is created to notify the team and request approval.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "ticket_key": {"type": "string", "description": "Jira ticket key e.g. TCLOUD-2721"},
                    "ticket_summary": {"type": "string", "description": "Short summary of the ticket"},
                    "user_story": {"type": "string", "description": "Full user story text"},
                    "priority": {"type": "string", "default": "Medium · P2", "description": "Priority label e.g. 'Medium · P2'"},
                    "effort_hours": {"type": "string", "default": "2–4 hours", "description": "Effort estimate e.g. '2–4 hours'"},
                    "azure_monthly_cost": {"type": "string", "default": "$5–$20 / mo", "description": "Azure monthly cost estimate"},
                    "risk_level": {"type": "string", "default": "Low", "description": "Risk level: Low / Medium / High / Critical"},
                    "acceptance_criteria": {"type": "array", "items": {"type": "string"}, "description": "List of acceptance criteria strings"},
                    "labels": {"type": "array", "items": {"type": "string"}, "default": ["ai-generated"], "description": "List of labels"},
                    "webhook_url": {"type": "string", "description": "Override Teams webhook URL"},
                    "date": {"type": "string", "description": "Date string for the card. Defaults to today."}
                },
                "required": ["ticket_key", "ticket_summary", "user_story", "acceptance_criteria"]
            }
        },
        {
            "name": "teams_build_card_payload",
            "description": "Builds and returns the raw Adaptive Card JSON payload without posting it. Useful for previewing, debugging, or posting via an external tool.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "ticket_key": {"type": "string", "description": "Jira ticket key e.g. TCLOUD-2721"},
                    "ticket_summary": {"type": "string", "description": "Short summary of the ticket"},
                    "user_story": {"type": "string", "description": "Full user story text"},
                    "priority": {"type": "string", "default": "Medium · P2", "description": "Priority label e.g. 'Medium · P2'"},
                    "effort_hours": {"type": "string", "default": "2–4 hours", "description": "Effort estimate e.g. '2–4 hours'"},
                    "azure_monthly_cost": {"type": "string", "default": "$5–$20 / mo", "description": "Azure monthly cost estimate"},
                    "risk_level": {"type": "string", "default": "Low", "description": "Risk level: Low / Medium / High / Critical"},
                    "acceptance_criteria": {"type": "array", "items": {"type": "string"}, "description": "List of acceptance criteria strings"},
                    "labels": {"type": "array", "items": {"type": "string"}, "default": ["ai-generated"], "description": "List of labels"},
                    "date": {"type": "string", "description": "Date string for the card. Defaults to today."}
                },
                "required": ["ticket_key", "ticket_summary", "user_story", "acceptance_criteria"]
            }
        },
        {
            "name": "teams_send_approval_email",
            "description": "Sends an HTML approval email for a ticket to the configured recipient. Currently requires Mail.Send permission on the M365 connector. If not available, returns the HTML body for manual sending.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "ticket_key": {"type": "string", "description": "Jira ticket key e.g. TCLOUD-2721"},
                    "ticket_summary": {"type": "string", "description": "Short summary of the ticket"},
                    "user_story": {"type": "string", "description": "Full user story text"},
                    "priority": {"type": "string", "default": "Medium · P2", "description": "Priority label e.g. 'Medium · P2'"},
                    "effort_hours": {"type": "string", "default": "2–4 hours", "description": "Effort estimate e.g. '2–4 hours'"},
                    "azure_monthly_cost": {"type": "string", "default": "$5–$20 / mo", "description": "Azure monthly cost estimate"},
                    "risk_level": {"type": "string", "default": "Low", "description": "Risk level: Low / Medium / High / Critical"},
                    "acceptance_criteria": {"type": "array", "items": {"type": "string"}, "description": "List of acceptance criteria strings"},
                    "labels": {"type": "array", "items": {"type": "string"}, "default": ["ai-generated"], "description": "List of labels"},
                    "recipient_email": {"type": "string", "description": "Override recipient email. Falls back to APPROVAL_EMAIL env var."},
                    "date": {"type": "string", "description": "Date string for the card. Defaults to today."}
                },
                "required": ["ticket_key", "ticket_summary", "user_story", "acceptance_criteria"]
            }
        }
    ]

@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
    """Handle tool calls"""
    try:
        if name == "teams_post_approval_card":
            # Validate and parse parameters
            params = TicketCardParams(**arguments)
            card = build_card(params)
            webhook_url = params.webhook_url or TEAMS_WEBHOOK_URL
            
            if not webhook_url:
                return CallToolResult(
                    content=[
                        TextContent(
                            type="text",
                            text=json.dumps({
                                "success": False,
                                "message": "Teams webhook URL not configured. Set TEAMS_WEBHOOK_URL environment variable or provide webhook_url parameter.",
                            }, indent=2)
                        )
                    ]
                )
            
            # Post to Teams
            result = await post_card_to_teams(webhook_url, card)
            
            output = {
                "success": result["success"],
                "message": result["message"],
                "ticket_key": card.ticket_key,
                "webhook_used": result.get("webhook_url"),
                "card_posted_at": datetime.now().isoformat(),
            }
            
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=json.dumps(output, indent=2)
                    )
                ]
            )
            
        elif name == "teams_build_card_payload":
            # Validate and parse parameters
            params = TicketCardParams(**arguments)
            card = build_card(params)
            payload = build_adaptive_card(card)
            
            output = {
                "success": True,
                "ticket_key": card.ticket_key,
                "payload": payload,
                "payload_size": len(json.dumps(payload)),
                "generated_at": datetime.now().isoformat(),
            }
            
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=json.dumps(output, indent=2)
                    )
                ]
            )
            
        elif name == "teams_send_approval_email":
            # Validate and parse parameters
            params = TicketCardParams(**arguments)
            card = build_card(params)
            recipient = params.recipient_email or APPROVAL_EMAIL
            html_body = build_approval_email_html(card)
            
            output = {
                "success": False,  # Email sending requires Graph permissions
                "message": "Email sending requires Microsoft Graph Mail.Send permission. HTML body returned for manual sending.",
                "ticket_key": card.ticket_key,
                "recipient": recipient,
                "subject": f"[Approval Required] {card.ticket_key} – {card.ticket_summary}",
                "html_body": html_body,
                "html_size": len(html_body),
                "generated_at": datetime.now().isoformat(),
            }
            
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=json.dumps(output, indent=2)
                    )
                ]
            )
            
        else:
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=json.dumps({
                            "success": False,
                            "message": f"Unknown tool: {name}",
                        }, indent=2)
                    )
                ]
            )
            
    except Exception as e:
        logger.error(f"Tool call error: {e}")
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=json.dumps({
                        "success": False,
                        "message": f"Error executing tool: {str(e)}",
                    }, indent=2)
                )
            ]
        )

async def main():
    """Run the MCP server"""
    logger.info("Starting Teams MCP Server (Python)")
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

def cli_main():
    """Entry point for console scripts"""
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)

if __name__ == "__main__":
    cli_main()