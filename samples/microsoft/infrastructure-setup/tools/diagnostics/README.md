# Diagnostics tools

Utility scripts that help inspect Azure AI Foundry agent deployments. These scripts are not required for the core infrastructure templates but can simplify troubleshooting.

## Scripts

- `check_cap_hosts.py` – lists capability hosts defined at the account and project scopes. Requires the Azure identity and requests packages and the environment variables documented inside the script.

## Usage

1. Create and activate a Python environment (for example, `python -m venv .venv && .venv\Scripts\activate`).
2. Install dependencies: `pip install azure-identity requests`.
3. Export the environment variables referenced by the script.
4. Run the desired script from this folder.
