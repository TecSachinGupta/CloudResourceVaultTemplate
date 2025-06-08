class CloudVaultError(Exception):
    """Base class for all custom exceptions."""
    pass

class ProviderNotSupportedError(CloudVaultError):
    """Raised when a cloud provider is not supported."""
    pass
