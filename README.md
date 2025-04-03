# CloudResourceVaultTemplate
A template to store assets for Azure Cloud but can be used with any other cloud provider to store the assets for Data Engineerig and Data Science.

## Folder Structure

```
.
│   .gitignore
│   LICENSE
│   README.md
│
├───DataFactory
│   ├───Pipelines
│   │       CopyProcessAndDeleteFile.json
│   │
│   └───Triggers
│           TR_SC_CopyProcessAndDeleteFile.json
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
└───Synapse
        DataDebug.sql
```

## Folder Description

|Folder|Parent|Description|
|------|------|-----------|
|AAA|bbbb|aaaaa|
| |AAA|asasasas|
||||


## Setup

1. Create a classic personal access token and provide the following access
	repo -> all
	admin:org -> read:org
2. Add the PAT in the repos secrect with named MY_CLASSIC_PAT
	Repo -> Setting -> Secrets and variables -> Actions