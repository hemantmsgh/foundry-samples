"""
List capability hosts for an Azure AI Foundry account and project.

Prereqs:
    pip install azure-identity requests
    (Run from an environment where DefaultAzureCredential can fetch a token.)
"""

import os
from typing import Iterable

import requests
from azure.identity import DefaultAzureCredential


API_VERSION = "2025-04-01-preview"
MGMT_SCOPE = "https://management.azure.com/.default"
BASE_URL = "https://management.azure.com"


def get_capability_hosts(url: str, credential: DefaultAzureCredential) -> Iterable[dict]:
    token = credential.get_token(MGMT_SCOPE)
    headers = {
        "Authorization": f"Bearer {token.token}",
        "Content-Type": "application/json",
    }
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json().get("value", [])


def main() -> None:

    subscription_id = os.environ["AZ_SUBSCRIPTION_ID"]
    resource_group = os.environ["AZ_RG_NAME"]
    account_name = os.environ["AZ_AI_ACCOUNT_NAME"]
    project_name = os.environ["AZ_AI_PROJECT_NAME"]

    credential = DefaultAzureCredential()

    account_caps_url = (
        f"{BASE_URL}/subscriptions/{subscription_id}/resourceGroups/{resource_group}"
        f"/providers/Microsoft.CognitiveServices/accounts/{account_name}/capabilityHosts"
        f"?api-version={API_VERSION}"
    )
    project_caps_url = (
        f"{BASE_URL}/subscriptions/{subscription_id}/resourceGroups/{resource_group}"
        f"/providers/Microsoft.CognitiveServices/accounts/{account_name}"
        f"/projects/{project_name}/capabilityHosts?api-version={API_VERSION}"
    )

    account_caps = list(get_capability_hosts(account_caps_url, credential))
    project_caps = list(get_capability_hosts(project_caps_url, credential))

    print("\n=== Account-level capability hosts ===")
    if not account_caps:
        print("No account capability hosts found.")
    for host in account_caps:
        print(f"- {host.get('name')} (kind: {host.get('properties', {}).get('capabilityHostKind')})")

    print("\n=== Project-level capability hosts ===")
    if not project_caps:
        print("No project capability hosts found.")
    for host in project_caps:
        props = host.get("properties", {})
        print(f"- {host.get('name')} (kind: {props.get('capabilityHostKind')})")
        print(f"  storageConnections: {props.get('storageConnections')}")
        print(f"  vectorStoreConnections: {props.get('vectorStoreConnections')}")
        print(f"  threadStorageConnections: {props.get('threadStorageConnections')}")

    print("\nDone.")


if __name__ == "__main__":
    main()