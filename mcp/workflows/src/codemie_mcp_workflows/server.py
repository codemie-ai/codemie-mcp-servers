"""Workflow execution MCP server implementation."""

import sys
from typing import Dict, Any

from mcp.server.fastmcp import FastMCP

from codemie_sdk import CodeMieClient
from .model import (
    WorkflowExecutionRequest,
    WorkflowExecutionResponse,
    WorkflowSettings
)

# Initialize settings at module level
try:
    settings = WorkflowSettings()
except Exception as e:
    print(f"Error initializing settings: {str(e)}", file=sys.stderr)
    sys.exit(1)


def get_client() -> CodeMieClient:
    """Gets authenticated CodeMie client instance."""
    try:
        client = CodeMieClient(
            username=settings.auth.username,
            password=settings.auth.password,
            auth_client_id=settings.auth.client_id,
            auth_client_secret=settings.auth.client_secret,
            verify_ssl=settings.verify_ssl,
            auth_realm_name=settings.auth_realm_name,
            auth_server_url=settings.auth_server_url,
            codemie_api_domain=settings.api_domain,
        )

        if not client.token:
            print("Failed to obtain authentication token", file=sys.stderr)
            raise ValueError("Failed to obtain authentication token")

        print("Successfully initialized CodeMie client", file=sys.stderr)
        return client
    except Exception as e:
        print(f"Error initializing client: {str(e)}", file=sys.stderr)
        raise

# Initialize FastMCP server
mcp = FastMCP("codemie-workflows")


@mcp.tool()
async def execute_workflow(workflow_id: str, user_input: str = "") -> Dict[str, Any]:
    """
    Execute a workflow with the given ID and optional user input.
    
    Args:
        workflow_id: ID of the workflow to execute
        user_input: Optional user input/prompt for the workflow
    
    Returns:
        Dictionary containing execution details including:
        - id: Workflow identifier
        - execution_id: Unique identifier for this execution
        - workflow_id: Source workflow ID
        - status: Current execution status
        - date: Creation timestamp
        - prompt: User input that triggered the execution
        - updated_date: Last update timestamp (if available)
    
    Raises:
        ValueError: If workflow_id is invalid or missing
        Exception: For other execution errors
    """
    try:
        # Input validation
        request = WorkflowExecutionRequest(
            workflow_id=workflow_id,
            user_input=user_input
        )
        
        # Get client and execute workflow
        client = get_client()
        response = client.workflows.run(
            workflow_id=request.workflow_id,
            user_input=request.user_input
        )
        
        # Validate and return response
        execution_response = WorkflowExecutionResponse.model_validate(response)
        return execution_response.model_dump(exclude_none=True)
        
    except ValueError as ve:
        print(f"Validation error: {str(ve)}", file=sys.stderr)
        raise
    except Exception as e:
        print(f"Error executing workflow {workflow_id}: {str(e)}", file=sys.stderr)
        raise

def main():
    try:
        print("Starting CodeMie Workflows MCP server", file=sys.stderr)
        # Initialize and run the server
        mcp.run(transport="stdio")
    except Exception as e:
        print(f"Error starting MCP server: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
