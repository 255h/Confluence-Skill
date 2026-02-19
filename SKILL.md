---
name: confluence
description: Read/Update confluence page. Use when asked to "read confluence page", "update confluence page", "review confluence page"
---

# Confluence Page Management

## Table of Contents

- [Purpose](#purpose)
- [When to Use This Skill](#when-to-use-this-skill)
- [Prerequisites](#prerequisites)
- [Quick Reference](#quick-reference)
- [Detailed Usage](#detailed-usage)
- [Storage Format](#storage-format)
- [Examples](#examples)

## Purpose

This skill enables reading and updating Confluence pages using the API. It supports:

- **Reading**: Get page content, title, and version information
- **Updating**: Modify page content, title, or both

## When to Use This Skill

**Activate for:**

- Read page content (e.g., "Get the content of page 12345")
- Read page title (e.g., "What is the title of page 12345?")
- Update page content (e.g., "Update page 1234 with new content")
- Update page title (e.g., "Rename page 1234 to 'New Title'")
- Update both content and title in a single operation

**Activate when:**

- User explicitly mentions "Confluence page" with read/write intent
- User wants to review or modify existing Confluence documentation
- User needs to programmatically update Confluence content
- User provided link to confluence page (e.g., "https://<site>/spaces/<space>/pages/<number>")

**Do not activate for:**

- General Confluence questions without specific page operations
- Creating new pages from scratch (unless content update is implied)
- Managing Confluence spaces or permissions

## Prerequisites

Before using this skill, verify environment variables are set:

```bash
python3 scripts/confluence.py check-setup
```

**Required environment variables:**

| Variable | Description | Get from |
|----------|-------------|----------|
| `CONFLUENCE_BASE_URL` | Your Confluence instance URL | Confluence Settings → Advanced Settings |
| `CONFLUENCE_API_KEY` | API authentication token | Atlassian Account → API Tokens |

**Note:** The script uses `verify=False` for SSL verification. In production, consider setting up proper SSL certificates or using `curl -k` equivalent.

## Quick Reference


| Command | Description | Example |
|---------|-------------|---------|
| `get-content <page_id>` | Get page content (HTML storage format) | `confluence get-content 123456` |
| `set-content <page_id> <file>` | Update page content from HTML file | `confluence set-content 123456 content.html` |
| `get-title <page_id>` | Get page title | `confluence get-title 123456` |
| `set-title <page_id> <title>` | Update page title | `confluence set-title 123456 "New Title"` |
| `get-version <page_id>` | Get current version number | `confluence get-version 123456` |
| `check-setup` | Verify environment variables | `confluence check-setup` |

## Detailed Usage

Store all temporary files (pages/diagrams/renders) in current project directory.

### Extracting page id from url

When presented with url that contains 'spaces/<space>/pages/<number>'  number after 'pages/' is page_id

### Reading Page Content

Get the page content in Confluence Storage Format (XHTML):

```bash
python3 scripts/confluence.py get-content <page_id>
```

Example:
```bash
python3 scripts/confluence.py get-content 123456
```

Output: HTML storage format content

### Reading Page Title

Get the page title:

```bash
python3 scripts/confluence.py get-title <page_id>
```

Example:
```bash
python3 scripts/confluence.py get-title 123456
```

Output: `Page Title`

### Reading Version Information

Get the current version number (required before updating):

```bash
python3 scripts/confluence.py get-version <page_id>
```

Example:
```bash
python3 scripts/confluence.py get-version 123456
```

Output: `5` (current version number)

### Updating Page Content

Update page content from an HTML file:

```bash
python3 scripts/confluence.py set-content <page_id> <html_file>
```

The script automatically:
1. Fetches current page data (title, current version)
2. Increments version number
3. Updates content

Example:
```bash
# Get current content, modify it, save to file
python3 scripts/confluence.py get-content 123456 > content.html

# Edit content.html with your changes
# ...

# Upload updated content
python3 scripts/confluence.py set-content 123456 content.html
```

### Updating Page Title

Update the page title:

```bash
python3 scripts/confluence.py set-title <page_id> <new_title>
```

Example:
```bash
python3 scripts/confluence.py set-title 123456 "Updated Project Documentation"
```

### Updating Both Content and Title

To update both content and title:

1. Update content first:
```bash
python3 scripts/confluence.py set-content 123456 new_content.html
```

2. Then update title:
```bash
python3 scripts/confluence.py set-title 123456 "New Title"
```

**Note:** Each update increments the version number independently.

## Storage Format

Confluence pages use **Storage Format** - an XHTML-based XML format for storing pages, templates, comments, and blog posts.

This skill accepts content in Storage Format. For detailed reference, see `references/storage-format-reference.md` which covers:

- **Headings**: `<h1>` through `<h6>`
- **Text formatting**: `<strong>`, `<em>`, `<code>`, `<span>`
- **Lists**: Ordered `<ol>`, unordered `<ul>`, task lists `<ac:task-list>`
- **Links**: Internal pages `<ac:link>`, external URLs `<a>`
- **Images**: `<ac:image>` with `<ri:attachment>` or `<ri:url>`
- **Tables**: `<table>`, `<tr>`, `<td>`, `<th>` with rowspan/colspan
- **Page layouts**: `<ac:layout>`, `<ac:layout-section>`, `<ac:layout-cell>`
- **Macros**: Structured macros like PlantUML `<ac:structured-macro>`
- **Template variables**: `<at:var>`, `<at:declarations>`

### Basic Storage Format Structure

```xml
<h1>Page Title</h1>
<p>Page content goes here.</p>

<h2>Section</h2>
<ul>
  <li>List item 1</li>
  <li>List item 2</li>
</ul>
```

See `references/storage-format-reference.md` for complete syntax and examples.

## Examples

### Example 1: Read and Display Page

```bash
# Get page information
python3 scripts/confluence.py get-title 123456
python3 scripts/confluence.py get-version 123456
python3 scripts/confluence.py get-content 123456
```

### Example 2: Update Page Content Only

```bash
# Get current content
python3 scripts/confluence.py get-content 123456 > page.html

# Edit page.html with your changes
# ...

# Update content (version auto-increments)
python3 scripts/confluence.py set-content 123456 page.html
```

### Example 3: Rename Page

```bash
# Get current information
python3 scripts/confluence.py get-title 123456

# Update title (version auto-increments)
python3 scripts/confluence.py set-title 123456 "New Project Name"

# Verify update
python3 scripts/confluence.py get-title 123456
```

### Example 4: Full Page Update (Title + Content)

```bash
# Step 1: Get current content and title
python3 scripts/confluence.py get-content 123456 > content.html
python3 scripts/confluence.py get-title 123456

# Step 2: Edit content.html and prepare new title

# Step 3: Update content
python3 scripts/confluence.py set-content 123456 content.html

# Step 4: Update title
python3 scripts/confluence.py set-title 123456 "Updated Title"

# Step 5: Verify
python3 scripts/confluence.py get-title 123456
python3 scripts/confluence.py get-version 123456
```

### Example 5: Working with Template Variables

To create/update pages with template variables:

1. Create HTML content with Confluence template syntax
2. Use Storage Format for `<at:declarations>` section
3. Upload using `set-content`

See `references/storage-format-reference.md` → "Template Variables" section for syntax.

### Example 6: Add PlantUML Diagram

To embed a PlantUML diagram:

1. Generate diagram 
2. Check it syntax 
3. Embed PlantUML macro:

```xml
<ac:structured-macro ac:name="plantuml" ac:schema-version="1">
  <ac:parameter ac:name="atlassian-macro-output-type">INLINE</ac:parameter>
  <ac:plain-text-body>
    <![CDATA[
@startuml
Alice -> Bob: Hello
@enduml
    ]]>
  </ac:plain-text-body>
</ac:structured-macro>
```

See `references/storage-format-reference.md` → "UML macros" section.
Do not attempt to attach image file.

## Troubleshooting

### Common Errors

| Error | Solution |
|-------|----------|
| `CONFLUENCE_BASE_URL environment variable not set` | Set environment variable: `export CONFLUENCE_BASE_URL=https://your-instance.atlassian.net` |
| `CONFLUENCE_API_KEY environment variable not set` | Set environment variable: `export CONFLUENCE_API_KEY=your-api-token` |
| `Error: API request failed. Status code: 403` | Verify API token has correct permissions |
| `Error: API request failed. Status code: 404` | Check page ID is correct |
| `Error: API request failed. Status code: 409` | Version conflict - get latest version before updating |

### Debug Mode

To see full API responses, check the script output. The script outputs errors to stderr.


## References

- **Storage Format**: `references/storage-format-reference.md` - Complete Confluence Storage Format syntax
- **Confluence REST API**: https://developer.atlassian.com/cloud/confluence/rest/
- **API Token Setup**: https://developer.atlassian.com/cloud/confluence/building-connections-to-confluence/
