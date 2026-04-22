---
name: jira-payload-formatting
description: Converts structured work requests into Jira create-issue payloads using Atlassian ADF with acceptance criteria and Definition of Done.
version: 1.0.0
---

# Jira Payload Formatting Skill

## Purpose
Convert a structured work request into a Jira-ready create-issue payload with a rich-text description in Atlassian Document Format (ADF).

## Responsibilities
- Transform structured requests into JIRA-compatible JSON payloads
- Generate Atlassian Document Format (ADF) descriptions with tables
- Map priority levels and labels to JIRA field requirements
- Include cost and security estimates in custom fields and description tables
- Validate all mandatory JIRA fields are properly formatted

## Input
The input will usually be JSON from an intake skill, for example:

{
  "route": "jira",
  "needs_clarification": false,
  "title": "Create Azure storage account for demo environment",
  "user_story": "As a demo team member, I want an Azure storage account provisioned in the demo environment so that I can store and access application data needed for demonstrations.",
  "acceptance_criteria": [
    "Azure storage account is created in the correct subscription and resource group for the demo environment",
    "Storage account name follows organisational naming conventions",
    "Appropriate redundancy tier is selected",
    "Access is restricted to approved users and services",
    "Storage account is tagged with environment, owner, and cost centre tags",
    "Soft delete and basic diagnostic logging is enabled"
  ],
  "priority": "P3",
  "labels": ["ai-generated", "slack-intake", "azure", "storage"],
  "cost_estimate": {
    "effort_hours": "2-4 hours",
    "complexity": "Medium",
    "dependencies": ["Azure subscription access", "Resource group permissions"],
    "azure_monthly_cost": "Estimated monthly cost: $10-25 (assumptions: Standard LRS, 500GB storage, moderate operations)"
  },
  "security_estimate": {
    "risk_level": "Medium",
    "security_requirements": ["RBAC controls", "Private endpoints", "Audit logging"],
    "compliance_impact": "Data residency requirements for demo environment"
  }
}

## Your job
Transform the input into a Jira-ready payload.

## CRITICAL RULES - MUST FOLLOW
- **PRIORITY IS REQUIRED**: Always map the input priority to Jira priority object
- **LABELS ARE REQUIRED**: Always include labels array with at least "ai-generated"
- Keep the summary short and clear.
- Preserve the user story.
- Preserve all request-specific acceptance criteria.
- Always append the Definition of Done section exactly as defined below.
- Use Atlassian ADF for the `description` field.
- Return JSON only.
- Do not create the ticket yourself.
- Do not add commentary outside the JSON payload.

## Priority mapping - MANDATORY
**ALWAYS map the input priority field to the correct Jira priority object:**
- P1 -> {"name":"Highest"}
- P2 -> {"name":"High"}
- P3 -> {"name":"Medium"}
- P4 -> {"name":"Low"}
- **If no priority in input, MUST default to {"name":"Medium"}**
- **Never leave priority empty or null**

## Labels handling - MANDATORY
**ALWAYS include labels array with these requirements:**
- Use all labels from the input `labels` array if present
- **MUST always include "ai-generated" as first label**
- Add relevant technology/domain labels based on the request content
- Common labels: "azure", "aws", "infrastructure", "security", "database", "network"
- **Never leave labels empty or null - minimum: ["ai-generated"]**
## Cost and Security Estimates Handling - REQUIRED FOR JIRA

**Cost Estimate (customfield_10001):**
- Format as structured text with clear separators
- Format: "Effort: [effort] | Complexity: [complexity] | Dependencies: [list] | Azure Cost: [azure_monthly_cost]"
- Example: "Effort: 2-4 hours | Complexity: Medium | Dependencies: Azure access, Resource permissions | Azure Cost: $10-25/month"

**Security Estimate (customfield_10002):**
- Format as structured text with clear separators
- Format: "Risk: [risk] | Requirements: [requirements] | Compliance: [compliance]"
- Example: "Risk: Medium | Requirements: RBAC controls, encryption | Compliance: GDPR considerations"

**ADF Description Tables:**
- Include Cost Estimate Table after Acceptance Criteria
- Include Security Assessment Table after Cost Estimate
- Use ADF table format for structured data presentation
## Issue type mapping
- delivery item -> Story or Task
- bug -> Bug
- request -> Task

## Required Definition of Done
Always include these items in the description:

- Implementation of technology follows vendor and industry best practice
- Work has been tested
- Work has been reviewed by peer
- Requestor agrees the work item has met the acceptance criteria in the ticket; agreed at the start of work
- Documentation, guides, and FAQs completed as required
- Knowledge transfer to team for new technology which other team members are not aware of
- Presentation to team preferably recorded and recording uploaded in Teams channel "Team Knowledge Transfers"

## ADF formatting rules
The Jira `description` must be a valid ADF document with this structure:

1. Heading: User Story
2. Paragraph: the user story text
3. Heading: Acceptance Criteria
4. Bullet list: each acceptance criterion as a separate bullet
5. Heading: Cost Estimate
6. Table: cost estimate details in tabular format
7. Heading: Security Assessment
8. Table: security assessment details in tabular format
9. Heading: Definition of Done
10. Bullet list: each DoD item as a separate bullet

## Output format
**REQUIRED FIELDS - ALL MUST BE PRESENT:**

{
  "fields": {
    "project": { "key": "CLOUDREQ" },
    "summary": "Create Azure storage account for demo environment",
    "issuetype": { "name": "Story" },
    "priority": { "name": "Medium" },
    "labels": ["ai-generated", "slack-intake", "azure", "storage"],
    "description": {
      "type": "doc",
      "version": 1,
      "content": []
    },
    "customfield_10001": "Effort: 2-4 hours | Complexity: Medium | Dependencies: Azure access, Resource group permissions | Azure Cost: $10-25/month (Standard LRS, 500GB storage)",
    "customfield_10002": "Risk: Medium | Requirements: RBAC controls, Private endpoints, Audit logging | Compliance: Data residency requirements"
  }
}

## VALIDATION CHECKLIST
Before returning JSON, verify:
- ✅ priority field contains valid Jira priority object with "name" property
- ✅ labels field contains array with at least ["ai-generated"]  
- ✅ summary is present and not empty
- ✅ description contains valid ADF structure
- ✅ customfield_10001 contains formatted cost estimate from input (including Azure costs if applicable)
- ✅ customfield_10002 contains formatted security estimate from input
- ❌ NEVER return empty priority or labels

## ADF template
Use this exact structure for `description`:

{
  "type": "doc",
  "version": 1,
  "content": [
    {
      "type": "heading",
      "attrs": { "level": 2 },
      "content": [
        { "type": "text", "text": "User Story" }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        { "type": "text", "text": "As a demo team member, I want an Azure storage account provisioned in the demo environment so that I can store and access application data needed for demonstrations." }
      ]
    },
    {
      "type": "heading",
      "attrs": { "level": 2 },
      "content": [
        { "type": "text", "text": "Acceptance Criteria" }
      ]
    },
    {
      "type": "bulletList",
      "content": [
        {
          "type": "listItem",
          "content": [
            {
              "type": "paragraph",
              "content": [
                { "type": "text", "text": "Azure storage account is created in the correct subscription and resource group for the demo environment" }
              ]
            }
          ]
        },
        {
          "type": "listItem",
          "content": [
            {
              "type": "paragraph",
              "content": [
                { "type": "text", "text": "Storage account name follows organisational naming conventions" }
              ]
            }
          ]
        },
        {
          "type": "listItem",
          "content": [
            {
              "type": "paragraph",
              "content": [
                { "type": "text", "text": "Appropriate redundancy tier is selected" }
              ]
            }
          ]
        },
        {
          "type": "listItem",
          "content": [
            {
              "type": "paragraph",
              "content": [
                { "type": "text", "text": "Access is restricted to approved users and services" }
              ]
            }
          ]
        },
        {
          "type": "listItem",
          "content": [
            {
              "type": "paragraph",
              "content": [
                { "type": "text", "text": "Storage account is tagged with environment, owner, and cost centre tags" }
              ]
            }
          ]
        },
        {
          "type": "listItem",
          "content": [
            {
              "type": "paragraph",
              "content": [
                { "type": "text", "text": "Soft delete and basic diagnostic logging is enabled" }
              ]
            }
          ]
        }
      ]
    },
    {
      "type": "heading",
      "attrs": { "level": 2 },
      "content": [
        { "type": "text", "text": "Cost Estimate" }
      ]
    },
    {
      "type": "table",
      "attrs": {
        "isNumberColumnEnabled": false,
        "layout": "default"
      },
      "content": [
        {
          "type": "tableRow",
          "content": [
            {
              "type": "tableHeader",
              "attrs": {},
              "content": [
                {
                  "type": "paragraph",
                  "content": [
                    { "type": "text", "text": "Category", "marks": [{ "type": "strong" }] }
                  ]
                }
              ]
            },
            {
              "type": "tableHeader",
              "attrs": {},
              "content": [
                {
                  "type": "paragraph",
                  "content": [
                    { "type": "text", "text": "Estimate", "marks": [{ "type": "strong" }] }
                  ]
                }
              ]
            }
          ]
        },
        {
          "type": "tableRow",
          "content": [
            {
              "type": "tableCell",
              "attrs": {},
              "content": [
                {
                  "type": "paragraph",
                  "content": [
                    { "type": "text", "text": "Effort Hours" }
                  ]
                }
              ]
            },
            {
              "type": "tableCell",
              "attrs": {},
              "content": [
                {
                  "type": "paragraph",
                  "content": [
                    { "type": "text", "text": "2-4 hours" }
                  ]
                }
              ]
            }
          ]
        },
        {
          "type": "tableRow",
          "content": [
            {
              "type": "tableCell",
              "attrs": {},
              "content": [
                {
                  "type": "paragraph",
                  "content": [
                    { "type": "text", "text": "Complexity" }
                  ]
                }
              ]
            },
            {
              "type": "tableCell",
              "attrs": {},
              "content": [
                {
                  "type": "paragraph",
                  "content": [
                    { "type": "text", "text": "Medium" }
                  ]
                }
              ]
            }
          ]
        },
        {
          "type": "tableRow",
          "content": [
            {
              "type": "tableCell",
              "attrs": {},
              "content": [
                {
                  "type": "paragraph",
                  "content": [
                    { "type": "text", "text": "Dependencies" }
                  ]
                }
              ]
            },
            {
              "type": "tableCell",
              "attrs": {},
              "content": [
                {
                  "type": "paragraph",
                  "content": [
                    { "type": "text", "text": "Azure subscription access, Resource group permissions" }
                  ]
                }
              ]
            }
          ]
        },
        {
          "type": "tableRow",
          "content": [
            {
              "type": "tableCell",
              "attrs": {},
              "content": [
                {
                  "type": "paragraph",
                  "content": [
                    { "type": "text", "text": "Azure Monthly Cost" }
                  ]
                }
              ]
            },
            {
              "type": "tableCell",
              "attrs": {},
              "content": [
                {
                  "type": "paragraph",
                  "content": [
                    { "type": "text", "text": "$10-25 (Standard LRS, 500GB storage, moderate operations)" }
                  ]
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "type": "heading",
      "attrs": { "level": 2 },
      "content": [
        { "type": "text", "text": "Security Assessment" }
      ]
    },
    {
      "type": "table",
      "attrs": {
        "isNumberColumnEnabled": false,
        "layout": "default"
      },
      "content": [
        {
          "type": "tableRow",
          "content": [
            {
              "type": "tableHeader",
              "attrs": {},
              "content": [
                {
                  "type": "paragraph",
                  "content": [
                    { "type": "text", "text": "Category", "marks": [{ "type": "strong" }] }
                  ]
                }
              ]
            },
            {
              "type": "tableHeader",
              "attrs": {},
              "content": [
                {
                  "type": "paragraph",
                  "content": [
                    { "type": "text", "text": "Assessment", "marks": [{ "type": "strong" }] }
                  ]
                }
              ]
            }
          ]
        },
        {
          "type": "tableRow",
          "content": [
            {
              "type": "tableCell",
              "attrs": {},
              "content": [
                {
                  "type": "paragraph",
                  "content": [
                    { "type": "text", "text": "Risk Level" }
                  ]
                }
              ]
            },
            {
              "type": "tableCell",
              "attrs": {},
              "content": [
                {
                  "type": "paragraph",
                  "content": [
                    { "type": "text", "text": "Medium" }
                  ]
                }
              ]
            }
          ]
        },
        {
          "type": "tableRow",
          "content": [
            {
              "type": "tableCell",
              "attrs": {},
              "content": [
                {
                  "type": "paragraph",
                  "content": [
                    { "type": "text", "text": "Security Requirements" }
                  ]
                }
              ]
            },
            {
              "type": "tableCell",
              "attrs": {},
              "content": [
                {
                  "type": "paragraph",
                  "content": [
                    { "type": "text", "text": "RBAC controls, Private endpoints, Audit logging" }
                  ]
                }
              ]
            }
          ]
        },
        {
          "type": "tableRow",
          "content": [
            {
              "type": "tableCell",
              "attrs": {},
              "content": [
                {
                  "type": "paragraph",
                  "content": [
                    { "type": "text", "text": "Compliance Impact" }
                  ]
                }
              ]
            },
            {
              "type": "tableCell",
              "attrs": {},
              "content": [
                {
                  "type": "paragraph",
                  "content": [
                    { "type": "text", "text": "Data residency requirements for demo environment" }
                  ]
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "type": "heading",
      "attrs": { "level": 2 },
      "content": [
        { "type": "text", "text": "Definition of Done" }
      ]
    },
    {
      "type": "bulletList",
      "content": [
        {
          "type": "listItem",
          "content": [
            {
              "type": "paragraph",
              "content": [
                { "type": "text", "text": "Implementation of technology follows vendor and industry best practice" }
              ]
            }
          ]
        },
        {
          "type": "listItem",
          "content": [
            {
              "type": "paragraph",
              "content": [
                { "type": "text", "text": "Work has been tested" }
              ]
            }
          ]
        },
        {
          "type": "listItem",
          "content": [
            {
              "type": "paragraph",
              "content": [
                { "type": "text", "text": "Work has been reviewed by peer" }
              ]
            }
          ]
        },
        {
          "type": "listItem",
          "content": [
            {
              "type": "paragraph",
              "content": [
                { "type": "text", "text": "Requestor agrees the work item has met the acceptance criteria in the ticket; agreed at the start of work" }
              ]
            }
          ]
        },
        {
          "type": "listItem",
          "content": [
            {
              "type": "paragraph",
              "content": [
                { "type": "text", "text": "Documentation, guides, and FAQs completed as required" }
              ]
            }
          ]
        },
        {
          "type": "listItem",
          "content": [
            {
              "type": "paragraph",
              "content": [
                { "type": "text", "text": "Knowledge transfer to team for new technology which other team members are not aware of" }
              ]
            }
          ]
        },
        {
          "type": "listItem",
          "content": [
            {
              "type": "paragraph",
              "content": [
                { "type": "text", "text": "Presentation to team preferably recorded and recording uploaded in Teams channel \"Team Knowledge Transfers\"" }
              ]
            }
          ]
        }
      ]
    }
  ]
}

## Important rules
- Each acceptance criterion must be a separate bullet item in ADF.
- Each Definition of Done item must be a separate bullet item in ADF.
- If the input is missing critical information, return:
{
  "needs_clarification": true,
  "clarifying_question": "One short question"
}
- Do not include any prose outside the JSON payload.
- If output is not valid JSON, regenerate it.