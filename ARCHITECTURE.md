# 🎫 Ticket Writer System Architecture

> **AI-Powered Ticket Management with Teams Approval Workflows**

A sophisticated multi-channel ticket management system that converts informal requests into structured tickets with cost estimation, security assessment, and automated approval workflows.

## 🏗️ **System Overview**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           INPUT CHANNELS                                    │
├─────────────────┬─────────────────┬─────────────────┬─────────────────────┤
│   📱 Slack      │   📧 Email      │   🗣️ Voice      │   💬 Chat           │
│   Messages      │   Requests      │   Commands      │   Interface         │
└─────────────────┴─────────────────┴─────────────────┴─────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    🧠 TICKET INTAKE ROUTER                                  │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  • Convert informal → structured data                              │    │
│  │  • Generate title, user story, acceptance criteria                 │    │
│  │  • Assign priority (P1-P4) and labels                             │    │
│  │  • Estimate costs (Azure services $5-140/month)                   │    │
│  │  • Assess security requirements                                    │    │
│  │  • Generate approval tracking ID                                   │    │
│  │  • Route decision: JIRA vs HALO                                   │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                           ┌──────────┴──────────┐
                           │                     │
                           ▼                     ▼
┌─────────────────────────────────┐    ┌─────────────────────────────────┐
│     📋 JIRA INTEGRATION         │    │     🎫 HALO INTEGRATION         │
│  ┌─────────────────────────────┐│    │  ┌─────────────────────────────┐│
│  │ • Engineering work          ││    │  │ • Access requests           ││
│  │ • Infrastructure changes    ││    │  │ • Service requests          ││
│  │ • Code deployments          ││    │  │ • Operational tasks         ││
│  │ • Priority mapping          ││    │  │ • Service desk workflows    ││
│  │ • Atlassian ADF format      ││    │  │ • Cost planning             ││
│  │ • Custom fields integration ││    │  │ • SLA tracking              ││
│  └─────────────────────────────┘│    │  └─────────────────────────────┘│
└─────────────────────────────────┘    └─────────────────────────────────┘
                           │                     │
                           └──────────┬──────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    👥 TEAMS APPROVAL SYSTEM                                 │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │              🎨 TEAMS APPROVAL CARD GENERATOR                       │    │
│  │  • Adaptive Card JSON creation                                     │    │
│  │  • Priority-based color coding                                     │    │
│  │  • Cost visualization                                              │    │
│  │  • Security assessment display                                     │    │
│  │  • Approve/Reject button actions                                   │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │              📤 TEAMS CARD POSTING SERVICE                          │    │
│  │  • Clear Channel webhook integration                               │    │
│  │  • Channel routing (General/specific channels)                     │    │
│  │  • Error handling & retry logic                                    │    │
│  │  • Delivery confirmation                                           │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │              🔄 APPROVAL WORKFLOW ORCHESTRATOR                      │    │
│  │  • End-to-end workflow management                                  │    │
│  │  • Card generation + posting coordination                          │    │
│  │  • Status tracking & notifications                                 │    │
│  │  • Audit trail maintenance                                         │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 📋 **Core Components**

### 🎯 **1. Ticket Intake Router**
**File:** `ticket-intake-router.md`

**Responsibilities:**
- Convert informal requests into structured data
- Generate comprehensive ticket metadata
- Route decisions (JIRA vs HALO)
- Cost & security estimation
- Priority assignment (P1-P4)

**Key Features:**
- **Azure Cost Estimation**: $5-140/month service pricing
- **Security Assessment**: Risk levels with requirement mapping  
- **Smart Routing**: Engineering work → JIRA, Service requests → HALO
- **Approval Tracking**: Unique ID generation (APPR-YYYY-NNN format)

### 📋 **2. JIRA Payload Formatter**  
**File:** `jira-payload-formatting.md`

**Responsibilities:**
- Transform structured data → JIRA API payloads
- Atlassian Document Format (ADF) compliance
- Custom field mapping
- Priority standardization

**Integration Points:**
- **Custom Fields**: Cost estimates, security data
- **Priority Mapping**: P1→Highest, P2→High, P3→Medium, P4→Low
- **Labels Management**: Dynamic tagging system
- **ADF Formatting**: Rich text rendering

### 🎫 **3. HALO Payload Formatter**
**File:** `halo-payload-formatting.md`  

**Responsibilities:**
- Service desk ticket creation
- Cost planning for operational requests
- SLA categorization
- Department routing

**Key Features:**
- **Service Desk Integration**: Request type mapping
- **Cost Planning**: Operational expense tracking
- **Priority Handling**: Service impact assessment
- **Department Routing**: Automated assignment logic

### 🎨 **4. Teams Approval Card Generator**
**File:** `teams-approval-card.md`

**Responsibilities:**
- Microsoft Teams Adaptive Card creation
- Visual cost/security representation  
- Interactive approve/reject buttons
- Priority-based styling

**Card Features:**
- **Dynamic Styling**: Priority-based color themes
- **Cost Visualization**: Azure service breakdown
- **Security Display**: Risk assessment summary
- **Action Buttons**: Approve/Reject with callback URLs

### 📤 **5. Teams Card Posting Service**  
**File:** `teams-post-card.md`

**Responsibilities:**
- Teams webhook integration
- Channel routing logic
- Delivery confirmation
- Error handling & retries

**Integration:**
- **Clear Channel Webhook**: Production Teams environment
- **Channel Routing**: Smart channel selection
- **Delivery Tracking**: Success/failure monitoring
- **Retry Logic**: Resilient posting mechanism

### 🔄 **6. Teams Approval Workflow Orchestrator**
**File:** `teams-approval-workflow.md`

**Responsibilities:**
- End-to-end workflow coordination  
- Card generation + posting pipeline
- Status tracking & notifications
- Audit trail management

**Workflow Steps:**
1. **Card Generation**: Invoke teams-approval-card skill
2. **Channel Posting**: Execute teams-post-card skill  
3. **Status Tracking**: Monitor approval responses
4. **Notification**: Update requestors & stakeholders

## 🔄 **Data Flow Architecture**

### **Phase 1: Input Processing**
```
Informal Request → Ticket Intake Router → Structured Data
```

**Data Transformation:**
```json
{
  "route": "jira|halo",
  "title": "Generated title",
  "user_story": "As a [user], I want [goal]...",
  "acceptance_criteria": ["Criterion 1", "Criterion 2"],
  "priority": "P1|P2|P3|P4", 
  "labels": ["ai-generated", "slack-intake", "azure"],
  "cost_estimate": {
    "effort_hours": "2-4 hours",
    "complexity": "Low|Medium|High",
    "azure_monthly_cost": "$15-30"
  },
  "security_estimate": {
    "risk_level": "Low|Medium|High",
    "security_requirements": ["RBAC", "Private endpoints"]
  },
  "requestor": "user@company.com",
  "approval_id": "APPR-2026-045"
}
```

### **Phase 2: Ticket Creation** 
```
Structured Data → [JIRA|HALO] Payload Formatter → Service API
```

### **Phase 3: Approval Workflow**
```
Ticket Created → Teams Card Generator → Teams Posting → User Approval
```

## 🛠️ **Integration Points**

### **External Services**
- **JIRA Cloud**: Atlassian API integration
- **HALO Service Desk**: Service management platform  
- **Microsoft Teams**: Clear Channel webhook
- **Azure Services**: Cost estimation API

### **Webhook Configuration**
```
Clear Channel Teams Webhook:
https://clearchannelint.webhook.office.com/webhookb2/...
```

### **Authentication**
- Service principal authentication for Azure APIs
- API tokens for JIRA/HALO integration  
- Webhook security for Teams integration

## 💰 **Cost Estimation Framework**

### **Azure Service Pricing** (Monthly estimates)
- **Storage Account**: $5-20/month
- **Key Vault**: $5-15/month  
- **Virtual Machines**: $31-140/month
- **App Service**: $13-55/month
- **Container Instances**: $10-40/month

### **Effort Estimation**
- **Low Complexity**: 1-2 hours
- **Medium Complexity**: 2-4 hours  
- **High Complexity**: 4-8 hours

## 🔒 **Security Assessment**

### **Risk Levels**
- **Low**: Standard configurations, no sensitive data
- **Medium**: Network changes, access modifications
- **High**: Security configurations, compliance requirements

### **Security Requirements Mapping**
- **RBAC Controls**: Identity and access management
- **Private Endpoints**: Network security  
- **Encryption**: Data protection requirements
- **Compliance**: Regulatory alignment

## 🚦 **Priority System**

| Priority | Description | SLA Target | Escalation |
|----------|-------------|------------|------------|
| **P1** | Critical/Outage | 4 hours | Immediate |
| **P2** | Important/Blocking | 24 hours | Next day |  
| **P3** | Normal | 5 days | Weekly |
| **P4** | Low | 10 days | Monthly |

## 📊 **Monitoring & Observability**

### **Key Metrics**
- Ticket processing time (intake → creation)
- Approval response rates  
- Cost estimation accuracy
- System integration success rates

### **Audit Trail**
- Request source tracking
- Approval decision logging
- Cost estimate tracking  
- Security assessment history

## 🔧 **Configuration Management**

### **Environment Variables**
```bash
JIRA_API_URL=https://company.atlassian.net
JIRA_API_TOKEN=xxx
HALO_API_URL=https://company.halopsa.com
HALO_API_KEY=xxx  
TEAMS_WEBHOOK_URL=https://clearchannelint.webhook...
```

### **Skill Configuration**
Each skill operates independently with standardized input/output interfaces enabling:
- **Modular Architecture**: Skills can be updated independently
- **Testing Isolation**: Individual skill validation
- **Workflow Flexibility**: Custom orchestration patterns

## 🎯 **Use Cases**

### **Engineering Requests**
```
"Can you create an Azure storage account for our demo environment?"
↓
JIRA ticket + Teams approval + Azure cost estimate
```

### **Access Requests**  
```
"I need access to the production database"
↓  
HALO ticket + Teams approval + Security assessment
```

### **Infrastructure Changes**
```
"Deploy a new VM for the staging environment"  
↓
JIRA ticket + Priority P2 + Cost estimate ($31-140/month) + Teams approval
```

---

**🚀 Ready for deployment with comprehensive ticket management, cost planning, and approval workflows!**