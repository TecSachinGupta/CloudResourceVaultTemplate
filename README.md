# CloudResourceVaultTemplate
A template to store assets for Azure Cloud but can be used with any other cloud provider to store the assets for Data Engineerig and Data Science.

## Folder Structure

```
.
│   .gitignore
│   LICENSE
│   README.md
│
├───.github
│   └───workflows
│           github-action-sync-repo.yml
│           main.yml
│
├───Notebooks
│   │   DevPlayGround.py
│   │
│   ├───configs
│   │       DefaultConfigs.py
│   │       SourceQueries.py
│   │
│   └───utils
│           GeneralFunctions.py
│           MongoDBFunctions.py
│           RelationalDatabaseFunctions.py
│
├───Scripts
│   ├───Bash
│   │       ExecutePipeline.sh
│   │
│   └───PowerShell
│           ExecutePipeline.ps
│
├───Storage
│   └───config
│           sourceConnectionDetails.json
│
├───Warehouse
│       DataDebug.sql
│
└───WorkFlows
    ├───Pipelines
    │       CopyProcessAndDeleteFile.json
    │
    └───Triggers
            TR_SC_CopyProcessAndDeleteFile.json
```

## Folder Description

|Folder|Parent|Description|
|------|------|-----------|
|Notebooks| |To stor the ETL code either Databricks or any other|
||||
|Scripts||To store different scripts to run from gt shell or powershell etc.|
||||
|Storage||TO store the static file in the Storage|
||||
|Warehouse||To strore the Analyical or Sql scripts created on top of the Data layer|
||||
|WorkFlows||Tp store the ETL pipeline and trigger details.|
||||


## Setup

1. Create a classic personal access token and provide the following access
	repo -> all
	admin:org -> read:org
2. Add the PAT in the repos secrect with named MY_CLASSIC_PAT
	Repo -> Setting -> Secrets and variables -> Actions