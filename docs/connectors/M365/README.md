# The M365 Connector

The [M365 Connector](https://claude.ai/directory/connectors/microsoft-365) grants access to various M365 solutions:

- Teams
- Email
- SharePoint
- OneDrive

More info: [Claude M365 Connector](https://support.claude.com/en/articles/12684923-microsoft-365-connector-security-guide)

## Access / Entra Apps

Users are granted access to this connector by being added to the [AAD_ADM_App_Claude_AI_M365_MCP](https://portal.azure.com/#view/Microsoft_AAD_IAM/GroupDetailsMenuBlade/~/Overview/groupId/bdfdd330-306d-4629-ac37-121cdd2356eb/menuId/) group in Entra.
That group is a member of [M365 MCP Client for Claude](https://portal.azure.com/#view/Microsoft_AAD_IAM/ManagedAppMenuBlade/~/Overview/objectId/9b71a7fa-4072-449a-a67a-f907d5b6402a/appId/08ad6f98-a4f8-4635-bb8d-f1a3044760f0/preferredSingleSignOnMode~/null/servicePrincipalType/Application/fromNav/), an enterprise app for granting user access to this connector.
The app [M365 MCP Server for Claude](https://portal.azure.com/#view/Microsoft_AAD_IAM/ManagedAppMenuBlade/~/Overview/objectId/0b5e3507-e732-409b-b0cb-f17ac703b538/appId/07c030f6-5743-41b7-ba00-0a6e85f37c17/preferredSingleSignOnMode~/null/servicePrincipalType/Application/fromNav/) grants the MS Graph permissions these apps require / is called by the server app.
