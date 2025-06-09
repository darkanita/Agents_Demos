

az ml workspace list --query "[].{name:name, resource_id:id}" --output table
Name                  Resource_id
--------------------  ----------------------------------------------------------------------------------------------------------------------------------------------------------------------
aqmlworkspace         /subscriptions/7a28b21e-0d3e-4435-a686-d92889d4ee96/resourceGroups/AI-FOUNDRY-RG/providers/Microsoft.MachineLearningServices/workspaces/aqmlworkspace
aq-hub                /subscriptions/7a28b21e-0d3e-4435-a686-d92889d4ee96/resourceGroups/rg-AQ-HUB-BASED-PROJECT/providers/Microsoft.MachineLearningServices/workspaces/aq-hub
aq-hub-based-project  /subscriptions/7a28b21e-0d3e-4435-a686-d92889d4ee96/resourceGroups/rg-AQ-HUB-BASED-PROJECT/providers/Microsoft.MachineLearningServices/workspaces/aq-hub-based-project


az resource show \
  --name aq-hub-based-project \
  --resource-group rg-AQ-HUB-BASED-PROJECT \
  --resource-type "Microsoft.MachineLearningServices/workspaces" \
  --query id \
  --output tsv

az ml workspace show --name aq-hub-based-project --resource-group rg-AQ-HUB-BASED-PROJECT --output table

az ml workspace show --name aq-hub-based-project --resource-group rg-AQ-HUB-BASED-PROJECT --output table
Allow_roleassignment_on_rg    Application_insights                                                                                                                       Description    Discovery_url                                   Display_name          Enable_data_isolation    Hbi_workspace    Hub_id                                                                                                                                                    Key_vault                                                                                                                                            Location       Mlflow_tracking_uri                                                                                                                                                                                                       Name                  Public_network_access    ResourceGroup            Resource_group           Storage_account                                                                                                                                             System_datastores_auth_mode
----------------------------  -----------------------------------------------------------------------------------------------------------------------------------------  -------------  ----------------------------------------------  --------------------  -----------------------  ---------------  --------------------------------------------------------------------------------------------------------------------------------------------------------  ---------------------------------------------------------------------------------------------------------------------------------------------------  -------------  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------  --------------------  -----------------------  -----------------------  -----------------------  ----------------------------------------------------------------------------------------------------------------------------------------------------------  -----------------------------
False                         /subscriptions/7a28b21e-0d3e-4435-a686-d92889d4ee96/resourceGroups/AI-FOUNDRY-RG/providers/Microsoft.Insights/components/aq-APPS-INSIGHTS                 https://swedencentral.api.azureml.ms/discovery  AQ-HUB-BASED-PROJECT  True                     False            /subscriptions/7a28b21e-0d3e-4435-a686-d92889d4ee96/resourceGroups/rg-AQ-HUB-BASED-PROJECT/providers/Microsoft.MachineLearningServices/workspaces/aq-hub  /subscriptions/7a28b21e-0d3e-4435-a686-d92889d4ee96/resourceGroups/rg-AQ-HUB-BASED-PROJECT/providers/Microsoft.KeyVault/vaults/kv-aqhub457609176373  swedencentral  azureml://swedencentral.api.azureml.ms/mlflow/v1.0/subscriptions/7a28b21e-0d3e-4435-a686-d92889d4ee96/resourceGroups/rg-AQ-HUB-BASED-PROJECT/providers/Microsoft.MachineLearningServices/workspaces/aq-hub-based-project  aq-hub-based-project  Enabled                  rg-AQ-HUB-BASED-PROJECT  rg-AQ-HUB-BASED-PROJECT  /subscriptions/7a28b21e-0d3e-4435-a686-d92889d4ee96/resourceGroups/rg-AQ-HUB-BASED-PROJECT/providers/Microsoft.Storage/storageAccounts/staqhub457609176373  accesskey


az ml workspace show --name aq-hub --resource-group rg-AQ-HUB-BASED-PROJECT --output table
az ml workspace show --name aq-hub --resource-group rg-AQ-HUB-BASED-PROJECT --output table
Default_resource_group                                                                      Description    Display_name    Enable_data_isolation    Hbi_workspace    Key_vault                                                                                                                                            Location       Name    Public_network_access    ResourceGroup            Resource_group           Storage_account
------------------------------------------------------------------------------------------  -------------  --------------  -----------------------  ---------------  ---------------------------------------------------------------------------------------------------------------------------------------------------  -------------  ------  -----------------------  -----------------------  -----------------------  ----------------------------------------------------------------------------------------------------------------------------------------------------------
/subscriptions/7a28b21e-0d3e-4435-a686-d92889d4ee96/resourceGroups/rg-AQ-HUB-BASED-PROJECT                 AQ-HUB          True                     False            /subscriptions/7a28b21e-0d3e-4435-a686-d92889d4ee96/resourceGroups/rg-AQ-HUB-BASED-PROJECT/providers/Microsoft.KeyVault/vaults/kv-aqhub457609176373  swedencentral  aq-hub  Enabled                  rg-AQ-HUB-BASED-PROJECT  rg-AQ-HUB-BASED-PROJECT  /subscriptions/7a28b21e-0d3e-4435-a686-d92889d4ee96/resourceGroups/rg-AQ-HUB-BASED-PROJECT/providers/Microsoft.Storage/storageAccounts/staqhub457609176373

az ml connection list --resource-group rg-AQ-HUB-BASED-PROJECT \
                      --workspace-name aq-hub-based-project \
                      --output table


Command group 'ml connection' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
Name                           Target
-----------------------------  -----------------------------------------------------------------
ai-aqhub457609176373_aoai      https://ai-aqhub457609176373.openai.azure.com/
ai-aqhub457609176373           https://ai-aqhub457609176373.cognitiveservices.azure.com/
aqaoaiSWEDENCENTRAL            https://aq-aoai-swedencentral.openai.azure.com/
aqaifoundrySwedenCentral_aoai  https://aq-ai-foundry-sweden-central.openai.azure.com/
aqaifoundrySwedenCentral       https://aq-ai-foundry-sweden-central.cognitiveservices.azure.com/
adminmbi8doqseastus2_aoai      https://admin-mbi8doqs-eastus2.openai.azure.com/
adminmbi8doqseastus2           https://admin-mbi8doqs-eastus2.cognitiveservices.azure.com/
adminmbi8gghuwestus3_aoai      https://admin-mbi8gghu-westus3.openai.azure.com/
adminmbi8gghuwestus3           https://admin-mbi8gghu-westus3.cognitiveservices.azure.com/
aiaqhub457609176373_aoai       https://ai-aqhub457609176373.openai.azure.com/
aiaqhub457609176373            https://ai-aqhub457609176373.cognitiveservices.azure.com/
aqbinggrounding001             https://api.bing.microsoft.com/



az ml connection show --resource-group rg-AQ-HUB-BASED-PROJECT --name aqbinggrounding001 --workspace-name aq-hub-based-project --populate-secrets

az ml connection show --resource-group rg-AQ-HUB-BASED-PROJECT --name aqbinggrounding001 --workspace-name aq-hub-based-project --populate-secrets
Command group 'ml connection' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
Api_base                         Api_key                           Is_shared    Name                ResourceGroup            Target
-------------------------------  --------------------------------  -----------  ------------------  -----------------------  -------------------------------
https://api.bing.microsoft.com/  76bf771750a54c5183eff84150d756ed  False        aqbinggrounding001  rg-AQ-HUB-BASED-PROJECT  https://api.bing.microsoft.com/






/subscriptions/7a28b21e-0d3e-4435-a686-d92889d4ee96/resourceGroups/AI-FOUNDRY-RG/providers/Microsoft.CognitiveServices/accounts/aq-ai-foundry-Sweden-Central/projects/firstProject/connections/aqbinggrounding001

az resource list --resource-type "Microsoft.CognitiveServices/accounts" --output table

Name                          ResourceGroup            Location       Type                                  Status
----------------------------  -----------------------  -------------  ------------------------------------  --------
aq-computer-vision-001        Computer-Vision          canadacentral  Microsoft.CognitiveServices/accounts
aq-ai-foundry-Sweden-Central  AI-FOUNDRY-RG            swedencentral  Microsoft.CognitiveServices/accounts
aq-aoai-SWEDENCENTRAL         AQ-AOAI-RG               swedencentral  Microsoft.CognitiveServices/accounts
admin-mbi8doqs-eastus2        aq-aoai-rg               eastus2        Microsoft.CognitiveServices/accounts
admin-mbi8gghu-westus3        aq-aoai-rg               westus3        Microsoft.CognitiveServices/accounts
ai-aqhub457609176373          rg-AQ-HUB-BASED-PROJECT  swedencentral  Microsoft.CognitiveServices/accounts

az resource list --resource-type "Microsoft.CognitiveServices/accounts/projects" --output table
Name                                       ResourceGroup    Location       Type                                           Status
-----------------------------------------  ---------------  -------------  ---------------------------------------------  --------
aq-ai-foundry-Sweden-Central/firstProject  AI-FOUNDRY-RG    swedencentral  Microsoft.CognitiveServices/accounts/projects






az ml connection list --resource-group rg-AQ-HUB-BASED-PROJECT \
                      --workspace-name aq-hub-based-project \
                      --output table

# https://learn.microsoft.com/en-us/azure/ai-services/agents/how-to/tools/bing-code-samples?pivots=python
Your connection ID needs to be in this format: 
/subscriptions/<subscription_id>/resourceGroups/<resource_group_name>/providers/Microsoft.CognitiveServices/accounts/<ai_service_name>/projects/<project_name>/connections/<connection_name>

# https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-agents/samples/agents_tools/sample_agents_bing_grounding.py
3) AZURE_BING_CONNECTION_ID - The ID of the Bing connection, in the format of:
/subscriptions/{subscription-id}/resourceGroups/{resource-group-name}/providers/Microsoft.MachineLearningServices/workspaces/{workspace-name}/connections/{connection-name}