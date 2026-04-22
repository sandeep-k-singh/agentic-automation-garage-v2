---
name: halo-payload-formatting
description: Converts structured service requests into Halo ITSM create-ticket payloads with proper categorization and service desk formatting.
version: 1.0.0
---

# Halo Payload Formatting Skill

## Purpose
Convert a structured service request into a Halo ITSM-ready create-ticket payload for access requests, support requests, and operational tasks.

## Responsibilities
- Transform structured requests into Halo ITSM-compatible payloads
- Map service request fields to Halo ticket structure
- Apply appropriate Halo categories, priorities, and assignment rules
- Generate payloads ready for Halo API submission
- Handle access requests, support tickets, and operational task formatting

## Input
The input will usually be JSON from an intake skill, for example:

{
  "route": "halo",
  "needs_clarification": false,
  "title": "Grant Azure DevOps access for new team member",
  "user_story": "As a team lead, I want to grant Azure DevOps access to a new team member so that they can contribute to our project repositories and pipelines.",
  "acceptance_criteria": [
    "User account is added to the correct Azure DevOps organization",
    "User is assigned to appropriate project teams",
    "User has correct permission levels (Contributor/Reader as appropriate)",
    "User can access assigned repositories",
    "User can view and run build pipelines",
    "Access is documented in team access registry"
  ],
  "priority": "P3",
  "labels": ["ai-generated", "slack-intake", "access-request", "azure-devops"],
  "cost_estimate": {
    "effort_hours": "1-2 hours",
    "complexity": "Low",
    "dependencies": ["Azure DevOps admin access", "Team lead approval"],
    "service_cost": "No additional cost - existing license utilization"
  }
}

## Your job
Transform the input into a Halo-ready ticket payload.

## Rules
- Keep the summary short and clear.
- Preserve the user story as the description.
- Convert acceptance criteria to actionable service desk steps.
- Map priority correctly using Halo priority levels.
- Use appropriate Halo categories and request types.
- Include proper urgency and impact levels.
- Include cost estimate for service planning and budget tracking.
- Return JSON only.
- Do not create the ticket yourself.
- Do not add commentary outside the JSON payload.

## Priority mapping
Always map the input priority field to the correct Halo priority:
- P1 -> 1 (Critical)
- P2 -> 2 (High)
- P3 -> 3 (Medium)
- P4 -> 4 (Low)
- If no priority in input, default to 3 (Medium)

## Category mapping
Map based on request type:
- Access requests -> "Access Management"
- Software requests -> "Software & Licensing"
- Hardware requests -> "Hardware & Equipment"
- Infrastructure requests -> "Infrastructure Services"
- Support requests -> "General Support"
- Account requests -> "Account Management"

## Request type mapping
- access -> "Service Request"
- support -> "Incident"
- infrastructure -> "Service Request"
- operational -> "Service Request"

## Urgency/Impact levels
- P1: Urgency=1, Impact=1 (Critical business impact)
- P2: Urgency=2, Impact=2 (High business impact)
- P3: Urgency=3, Impact=3 (Medium business impact)
- P4: Urgency=4, Impact=3 (Low business impact)

## Service Desk Cost Estimation
For service requests, provide cost planning:
- **Effort estimation**: Time required for service desk to fulfill request
- **Complexity assessment**: Simple, moderate, or complex process
- **Service costs**: Any licensing, software, or resource costs involved
- **Dependencies**: Required approvals or external resources

**Common service costs:**
- **Software licensing**: Per-user costs for applications ($5-50/month typical)
- **Hardware provisioning**: Equipment costs and setup time ($200-2000 typical)
- **Cloud services**: Monthly subscription costs (varies by service)
- **Access management**: Usually no additional cost (existing systems)
- **Training/setup**: Time investment only (1-4 hours typical)

**Format as**: "[effort] ([complexity]) - Service cost: [amount/description] - Dependencies: [list]"

## Output format
Return JSON only in this shape (priority, category, and urgency/impact should be mapped from input):

{
  "summary": "Grant Azure DevOps access for new team member",
  "details": "As a team lead, I want to grant Azure DevOps access to a new team member so that they can contribute to our project repositories and pipelines.",
  "category_1": "Access Management",
  "category_2": "Azure Services", 
  "priority": 3,
  "urgency": 3,
  "impact": 3,
  "requesttype": "Service Request",
  "assignedtoteam": "IT Service Desk",
  "tags": ["ai-generated", "slack-intake", "access-request", "azure-devops"],
  "servicecost": "1-2 hours (Low complexity) - Service cost: No additional cost - existing license - Dependencies: Azure DevOps admin access, Team lead approval",
  "customfields": [
    {
      "name": "Acceptance Criteria",
      "value": "1. User account is added to the correct Azure DevOps organization\\n2. User is assigned to appropriate project teams\\n3. User has correct permission levels (Contributor/Reader as appropriate)\\n4. User can access assigned repositories\\n5. User can view and run build pipelines\\n6. Access is documented in team access registry"
    }
  ]
}

## Important rules
- Each acceptance criterion should be numbered in the customfields value.
- Use \\n for line breaks in the acceptance criteria.
- Always include "ai-generated" in tags if not present.
- Map categories based on the request content and type.
- Include servicecost field with formatted cost estimate from input.
- If the input is missing critical information, return:
{
  "needs_clarification": true,
  "clarifying_question": "One short question"
}
- Do not include any prose outside the JSON payload.
- If output is not valid JSON, regenerate it.

## Common categories by request type
- **Access requests**: "Access Management", "Account Management"
- **Software requests**: "Software & Licensing", "Application Support"
- **Infrastructure requests**: "Infrastructure Services", "Cloud Services"
- **Azure requests**: "Cloud Services", "Azure Services"
- **Network requests**: "Network Services", "Infrastructure Services" 
- **Security requests**: "Security Services", "Access Management"