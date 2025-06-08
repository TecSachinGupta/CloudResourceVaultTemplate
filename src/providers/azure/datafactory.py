# src/providers/azure/datafactory.py
import asyncio
import logging
from typing import Any, Dict, List, Optional

from azure.identity import DefaultAzureCredential
from azure.mgmt.datafactory import DataFactoryManagementClient
from azure.mgmt.datafactory.models import (
    Factory,
    PipelineResource,
    PipelineRun,
    CreateRunResponse
)

from src.core.config import CloudConfig
from src.core.exceptions import ProviderError
from src.providers.base import DataProcessingResource

logger = logging.getLogger(__name__)


class AzureDataFactory(DataProcessingResource):
    """Azure Data Factory implementation of DataProcessingResource."""
    
    def __init__(self, name: str, config: CloudConfig):
        """
        Initialize Azure Data Factory resource.
        
        Args:
            name: The name of the Data Factory
            config: Configuration for Azure
        """
        super().__init__(name, config)
        self.resource_group = config.get("resource_group")
        self.region = config.get("region", "East US")
        self.client = None
        self._initialize_client()
        
    def _initialize_client(self):
        """Initialize the Azure Data Factory client."""
        try:
            credential = DefaultAzureCredential()
            self.client = DataFactoryManagementClient(
                credential=credential,
                subscription_id=self.config.get("subscription_id")
            )
        except Exception as e:
            logger.error(f"Failed to initialize Azure Data Factory client: {str(e)}")
            raise ProviderError(f"Failed to initialize client: {str(e)}")
    
    async def create(self, **kwargs) -> str:
        """
        Create an Azure Data Factory.
        
        Returns:
            str: The ID of the created Data Factory
        """
        try:
            factory = Factory(location=self.region)
            operation = self.client.factories.begin_create_or_update(
                self.resource_group,
                self.name,
                factory
            )
            result = operation.result()
            self.resource_id = result.id
            logger.info(f"Created Azure Data Factory: {self.resource_id}")
            return self.resource_id
        except Exception as e:
            logger.error(f"Failed to create Azure Data Factory: {str(e)}")
            raise ProviderError(f"Failed to create resource: {str(e)}")
    
    async def update(self, **kwargs) -> bool:
        """
        Update the Azure Data Factory.
        
        Returns:
            bool: True if the update was successful
        """
        try:
            # Get the current factory
            factory = self.client.factories.get(self.resource_group, self.name)
            
            # Update tags if provided
            if "tags" in kwargs:
                factory.tags = kwargs["tags"]
            
            # Perform the update
            operation = self.client.factories.begin_create_or_update(
                self.resource_group,
                self.name,
                factory
            )
            operation.result()
            logger.info(f"Updated Azure Data Factory: {self.resource_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to update Azure Data Factory: {str(e)}")
            raise ProviderError(f"Failed to update resource: {str(e)}")
    
    async def delete(self) -> bool:
        """
        Delete the Azure Data Factory.
        
        Returns:
            bool: True if the deletion was successful
        """
        try:
            operation = self.client.factories.begin_delete(
                self.resource_group,
                self.name
            )
            operation.result()
            logger.info(f"Deleted Azure Data Factory: {self.resource_id}")
            self.resource_id = None
            return True
        except Exception as e:
            logger.error(f"Failed to delete Azure Data Factory: {str(e)}")
            raise ProviderError(f"Failed to delete resource: {str(e)}")
    
    async def get_status(self) -> Dict[str, Any]:
        """
        Get the current status of the Data Factory.
        
        Returns:
            Dict[str, Any]: Status information about the Data Factory
        """
        try:
            factory = self.client.factories.get(self.resource_group, self.name)
            return {
                "id": factory.id,
                "name": factory.name,
                "type": factory.type,
                "location": factory.location,
                "provisioning_state": factory.provisioning_state,
                "created_time": factory.created_time.isoformat() if factory.created_time else None,
                "tags": factory.tags
            }
        except Exception as e:
            logger.error(f"Failed to get Azure Data Factory status: {str(e)}")
            raise ProviderError(f"Failed to get resource status: {str(e)}")
    
    async def run_job(self, pipeline_name: str, parameters: Dict[str, Any] = None) -> str:
        """
        Run an Azure Data Factory pipeline.
        
        Args:
            pipeline_name: The name of the pipeline to run
            parameters: Parameters to pass to the pipeline
            
        Returns:
            str: The pipeline run ID
        """
        try:
            response: CreateRunResponse = self.client.pipelines.create_run(
                self.resource_group,
                self.name,
                pipeline_name,
                parameters=parameters or {}
            )
            logger.info(f"Started pipeline run: {response.run_id}")
            return response.run_id
        except Exception as e:
            logger.error(f"Failed to run Azure Data Factory pipeline: {str(e)}")
            raise ProviderError(f"Failed to run job: {str(e)}")
    
    async def get_job_status(self, run_id: str) -> Dict[str, Any]:
        """
        Get the status of a pipeline run.
        
        Args:
            run_id: The ID of the pipeline run
            
        Returns:
            Dict[str, Any]: Status information about the pipeline run
        """
        try:
            pipeline_run: PipelineRun = self.client.pipeline_runs.get(
                self.resource_group,
                self.name,
                run_id
            )
            return {
                "run_id": pipeline_run.run_id,
                "pipeline_name": pipeline_run.pipeline_name,
                "status": pipeline_run.status,
                "start_time": pipeline_run.run_start.isoformat() if pipeline_run.run_start else None,
                "end_time": pipeline_run.run_end.isoformat() if pipeline_run.run_end else None,
                "duration_in_ms": pipeline_run.duration_in_ms,
                "parameters": pipeline_run.parameters
            }
        except Exception as e:
            logger.error(f"Failed to get Azure Data Factory pipeline run status: {str(e)}")
            raise ProviderError(f"Failed to get job status: {str(e)}")
    
    async def create_pipeline(self, pipeline_name: str, pipeline_definition: Dict[str, Any]) -> str:
        """
        Create a pipeline in the Data Factory.
        
        Args:
            pipeline_name: The name of the pipeline to create
            pipeline_definition: The definition of the pipeline
            
        Returns:
            str: The ID of the created pipeline
        """
        try:
            pipeline = PipelineResource(
                activities=pipeline_definition.get("activities", []),
                parameters=pipeline_definition.get("parameters", {})
            )
            
            result = self.client.pipelines.create_or_update(
                self.resource_group,
                self.name,
                pipeline_name,
                pipeline
            )
            
            logger.info(f"Created pipeline: {result.id}")
            return result.id
        except Exception as e:
            logger.error(f"Failed to create Azure Data Factory pipeline: {str(e)}")
            raise ProviderError(f"Failed to create pipeline: {str(e)}")