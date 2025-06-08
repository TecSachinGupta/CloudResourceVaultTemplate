# src/providers/base.py
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union

from src.core.config import CloudConfig
from src.core.exceptions import ProviderError


class CloudResource(ABC):
    """Base abstract class for all cloud resources."""
    
    def __init__(self, name: str, config: CloudConfig):
        """
        Initialize a cloud resource.
        
        Args:
            name: The name of the resource
            config: Configuration for the cloud provider
        """
        self.name = name
        self.config = config
        self.resource_id: Optional[str] = None
        
    @abstractmethod
    async def create(self, **kwargs) -> str:
        """
        Create the resource in the cloud provider.
        
        Returns:
            str: The ID of the created resource
        """
        pass
    
    @abstractmethod
    async def update(self, **kwargs) -> bool:
        """
        Update the resource in the cloud provider.
        
        Returns:
            bool: True if the update was successful
        """
        pass
    
    @abstractmethod
    async def delete(self) -> bool:
        """
        Delete the resource from the cloud provider.
        
        Returns:
            bool: True if the deletion was successful
        """
        pass
    
    @abstractmethod
    async def get_status(self) -> Dict[str, Any]:
        """
        Get the current status of the resource.
        
        Returns:
            Dict[str, Any]: Status information about the resource
        """
        pass


class DataProcessingResource(CloudResource):
    """Base class for data processing resources like Azure Data Factory, AWS Glue, etc."""
    
    @abstractmethod
    async def run_job(self, job_name: str, parameters: Dict[str, Any] = None) -> str:
        """
        Run a data processing job.
        
        Args:
            job_name: The name of the job to run
            parameters: Parameters to pass to the job
            
        Returns:
            str: The job run ID
        """
        pass
    
    @abstractmethod
    async def get_job_status(self, job_run_id: str) -> Dict[str, Any]:
        """
        Get the status of a job run.
        
        Args:
            job_run_id: The ID of the job run
            
        Returns:
            Dict[str, Any]: Status information about the job run
        """
        pass


class AnalyticsResource(CloudResource):
    """Base class for analytics resources like Azure Synapse, AWS Redshift, GCP BigQuery."""
    
    @abstractmethod
    async def execute_query(self, query: str, parameters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Execute a query against the analytics resource.
        
        Args:
            query: The query to execute
            parameters: Parameters to pass to the query
            
        Returns:
            List[Dict[str, Any]]: Query results
        """
        pass
    
    @abstractmethod
    async def create_table(self, table_name: str, schema: Dict[str, str]) -> bool:
        """
        Create a table in the analytics resource.
        
        Args:
            table_name: The name of the table to create
            schema: The schema of the table
            
        Returns:
            bool: True if the table was created successfully
        """
        pass


class MessagingResource(CloudResource):
    """Base class for messaging resources like Azure Service Bus, AWS SQS, GCP Pub/Sub."""
    
    @abstractmethod
    async def send_message(self, message: Union[str, Dict[str, Any]], queue_name: str) -> str:
        """
        Send a message to a queue or topic.
        
        Args:
            message: The message to send
            queue_name: The name of the queue or topic
            
        Returns:
            str: The message ID
        """
        pass
    
    @abstractmethod
    async def receive_messages(self, queue_name: str, max_messages: int = 10, wait_time: int = 10) -> List[Dict[str, Any]]:
        """
        Receive messages from a queue or subscription.
        
        Args:
            queue_name: The name of the queue or subscription
            max_messages: The maximum number of messages to receive
            wait_time: The time to wait for messages in seconds
            
        Returns:
            List[Dict[str, Any]]: The received messages
        """
        pass