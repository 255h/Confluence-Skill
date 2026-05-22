# Confluence Skill

Read and update Confluence pages using the REST API.

## Installation

### Option 1: Download Release Executable
1. Go to the [Releases](https://github.com/your-repo/Confluence-Skill/releases) page
2. Download `confluence-skill-linux.zip` (Linux/macOS) or `confluence-skill-windows.zip` (Windows)
3. Extract and run the executable

### Option 2: Build from Source
```bash
pip install -r scripts/requirements.txt pyinstaller
pyinstaller --onefile --name confluence-skill scripts/confluence.py
```

## Setup

Set required environment variables:

**Linux/macOS:**
```bash
export CONFLUENCE_BASE_URL="https://your-instance.atlassian.net"
export CONFLUENCE_API_KEY="your-api-token"
```

**Windows (Command Prompt):**
```cmd
set CONFLUENCE_BASE_URL=https://your-instance.atlassian.net
set CONFLUENCE_API_KEY=your-api-token
```

**Windows (PowerShell):**
```powershell
$env:CONFLUENCE_BASE_URL="https://your-instance.atlassian.net"
$env:CONFLUENCE_API_KEY="your-api-token"
```

Verify setup:

**Linux/macOS:**
```bash
./confluence-skill check-setup
```

**Windows:**
```bash
confluence-skill.exe check-setup
```

