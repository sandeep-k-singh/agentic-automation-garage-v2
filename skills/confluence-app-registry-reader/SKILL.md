---
name: confluence-app-registry-reader
description: Use this skill whenever a service desk ticket, Jira issue, or user question references a specific business application, integration, or system and Claude needs to look up operational documentation from the organisation's Confluence-based application registry. Trigger on mentions of specific app names, "how do I...", "who owns...", "what servers run...", "is this a known issue...", "how do we recover...", "what's the audit procedure for...", or any interface/integration between two systems. Also trigger when a Jira ticket needs to be enriched with application context (owners, environments, known issues) before responding. The registry uses page labels (pagetype-application, pagetype-howto, pagetype-knownissue, pagetype-audittask, pagetype-dr, pagetype-apparchitecture, pagetype-integration) to categorise content, and this skill knows how to navigate that structure, extract the right information (and assess how much to trust it based on the page's last-updated date; given much of the documentation there is stale).  Note; longer term the Halo CMDB would likely be a better source for such info; at which point this skill could be replaced by a Halo-centric alternative.
---

# Confluence Application Registry

This skill helps Claude retrieve and reason over operational documentation stored in the organisation's Confluence space, which functions as a pseudo-CMDB and application registry. The documentation quality varies significantly between teams, so a core part of this skill is calibrating confidence based on freshness and being transparent about that calibration when presenting answers.

## The registry structure

Each application has a parent page labelled `pagetype-application`. Child pages hang off it with one of the following labels:

| Label | Purpose |
|---|---|
| `pagetype-howto` | Step-by-step guides for common operational tasks |
| `pagetype-knownissue` | Recognised incident patterns and their resolution steps |
| `pagetype-audittask` | Procedures for compliance activities (e.g. SOX user access exports) |
| `pagetype-dr` | Disaster recovery and business continuity procedures |
| `pagetype-apparchitecture` | Servers, service accounts, databases per environment |
| `pagetype-integration` | End-to-end interface documentation - source, middleware, destination, and per-system config |

Integration pages are special: they live under the destination system's application page but describe a flow that spans multiple systems. A single integration (e.g. "new customers from AIDA -> LogicApps -> D365FO") may be referenced from both the source and destination applications' pages under Integrations > Inbound and Integrations > Oubound headings.

All of these pages can be found in the Confluence Space with key: `Apps`.
There are other spaces which may be useful sources of knowledge; but those are typically adhoc in structure & freetext, so harder to programmatically navigate / provide consistent guidance for appropriate usage.

## How to use this skill

### Step 1: Identify what the user is actually asking for

Before querying anything, work out which page type(s) are relevant. Don't fetch indiscriminately; a targeted CQL query is far better than pulling in ten pages and sifting.

Map the intent:

- *"How do I reset a password for X?"* -> `pagetype-howto` under app X
- *"Users are getting error Y in app X"* -> `pagetype-knownissue` under app X, then `pagetype-howto` as fallback
- *"Who owns app X?"* -> `pagetype-application` for app X
- *"What DB does app X use?"* -> `pagetype-apparchitecture` under app X
- *"How does the X-to-Y interface work?"* -> `pagetype-integration`, searched by both app names
- *"Where can I find the DR recovery steps for app X?"* -> `pagetype-dr` under app X
- *"I need to do the quarterly user access review for X"* -> `pagetype-audittask` under app X

If the question is ambiguous (e.g. "tell me about app X"), start with the `pagetype-application` parent page and surface a summary of what child pages exist, rather than guessing.

### Step 2: Query Confluence

Use the Atlassian MCP integration's search/CQL capability. Prefer label + ancestor filters over full-text search when you know the app:

```
space = "Apps" AND label = "pagetype-knownissue" AND ancestor = "<app-page-id>"
```

If the user named a system but you don't know its page ID, resolve it first:

```
space = "Apps" AND label = "pagetype-application" AND title ~ "<app name>"
```

For integration queries involving two systems, search by label plus text:

```
space = "Apps" AND label = "pagetype-integration" AND (text ~ "<system A>" AND text ~ "<system B>")
```

Always retrieve the page's `version.when` (last published date) and the last editor - these drive the confidence assessment in step 4.

### Step 3: Extract the answer

Read the page content and extract only what's needed to answer the question. Don't dump whole pages back to the user. For architecture/ownership questions, structured fields (environment -> server -> DB -> service account) are often in tables - preserve that structure when summarising.

For **integration pages**, the flow matters: source -> middleware -> destination. Keep that shape when explaining, and call out per-system configuration separately from the overall process description.

### Step 4: Apply a freshness/confidence assessment

The registry is not uniformly maintained. Before presenting any answer, check the page's last-published date and classify it:

| Age since last update | Default confidence band |
|---|---|
| < 1 year | **Fresh** - treat as authoritative |
| 1-3 years | **Stale** - likely still useful but flag that it hasn't been touched recently |
| > 3 years | **Very stale** - surface the content but lead with a caveat; recommend verifying with the app owner before acting |

Additional confidence signals to look for:

- Pages with TODO / FIXME / "needs review" markers -> reduce confidence regardless of date
- Pages that reference decommissioned infrastructure (old server names, retired cloud regions) -> flag explicitly
- Pages that are archived or reference archived/deleted pages -> flag explicitly
- Pages which reference users who no longer exist (e.g. show `@Former user (Deleted)`) -> flag explicitly
- Pages with no clear technical owner field -> mention this as a caveat

### Step 5: Present the answer

Structure the response for a human agent who will review before acting; though this skill may also be used in agent-agent collaborations:

1. **The answer itself**, in the most useful form for the task (steps for a how-to, a table for architecture, a flow diagram description for an integration)
2. **Source**: link to the Confluence page(s) used, with page titles
3. **Confidence note**: "This page was last updated [date] by [user]. Treating as **[Fresh/Stale/Very stale]** for this query type." Keep it to one or two sentences unless the confidence is low, in which case be explicit about what to re-verify.
4. **Gaps**: if the documentation didn't fully answer the question, say what's missing rather than inventing. Suggest who to ask (app's technical owner from the app's  page, or the page's last editor).

### Step 6: Never fabricate

If no relevant page exists, say so plainly. Don't generate plausible-sounding architecture details or DR procedures from general knowledge - for a CMDB-style lookup, a confident wrong answer is worse than "I couldn't find this documented; the parent app page lists [X] as the owner, suggest checking with them."

## When *not* to use the registry

Some things this skill is not for:

- General technical how-tos that aren't app-specific (e.g. "how do I write a Kusto query") - answer from general knowledge
- Live system state (whether a service is up, current user count, etc.) - the registry is documentation, not telemetry
- Ticket history, change records, or incident post-mortems - those live elsewhere (ITSM/Jira), not in the registry

## Example interactions

**Example 1 - Known issue lookup:**
> User: "Users of DemoOpsApp are seeing a 503 when exporting reports."
>
> Skill: Resolves the DemoOpsApp page, queries for `pagetype-knownissue` children, finds "503 on report export - IIS app pool recycle needed". Page last updated 3 months ago. Returns the resolution steps with a "Fresh" confidence note and a link to the source page.

**Example 2 - Architecture lookup with staleness concern:**
> User: "What DB server does the InventoryApp production environment use?"
>
> Skill: Finds `pagetype-apparchitecture` page for InventoryApp, last updated 5 years ago. Returns the DB server name in a table, but - because this page is older than our threshold of 3 years leads with: "This page hasn't been updated in 5 yearswhich is considered stale. The page lists SQLPROD07 as the prod DB; worth confirming such a database still exists / checking the documentation's validity with the app owner before relying on this information."

**Example 3 - Integration lookup:**
> User: "New customers are not appearing in FinanceSystem"
>
> Skill: Searches `pagetype-integration` for pages mentioning FinanceSystem as a destintion and new customers. Returns source/middleware/destination summary, per-system config notes, and confidence based on the integration page's date *plus* the most recent update date of either endpoint app.  Also searches for `pagetype-knownissue` for FinanceSystem and for any of the source/middleware systems referenced on the `pagetype-integration` page for issues related to `new customer` interfaces/integraions.
