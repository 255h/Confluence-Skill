# Confluence Skill

Read and update Confluence pages using the REST API.

## Installation

```bash
pip install -r scripts/requirements.txt
```

## Setup

Set required environment variables:

```bash
export CONFLUENCE_BASE_URL="https://your-instance.atlassian.net"
export CONFLUENCE_API_KEY="your-api-token"
```

Verify setup:

```bash
python3 scripts/confluence.py check-setup
```

