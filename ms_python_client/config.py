from typing import Optional


# pylint: disable=C0103
class Config:
    TOKEN_CACHE_FILE: str = "token_cache.bin"
    AZURE_AUTHORITY: str
    AZURE_CLIENT_ID: str
    AZURE_SCOPE: list[str] = []

    def __init__(
        self,
        token_cache_file: Optional[str] = None,
        azure_authority: Optional[str] = None,
        azure_client_id: Optional[str] = None,
        azure_scope: Optional[list[str]] = None,
    ):
        if token_cache_file:
            self.TOKEN_CACHE_FILE = token_cache_file

        if azure_authority:
            self.AZURE_AUTHORITY = azure_authority
        else:
            raise ValueError("Azure authority is not set")

        if azure_client_id:
            self.AZURE_CLIENT_ID = azure_client_id
        else:
            raise ValueError("Azure client id is not set")
        if azure_scope:
            self.AZURE_SCOPE = azure_scope
        else:
            raise ValueError("Azure scope is not set")
