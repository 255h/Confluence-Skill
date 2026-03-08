#!/usr/bin/env python3
import sys
import os
import requests
import urllib3


BASE_URL_VAR = "CONFLUENCE_BASE_URL"
API_KEY_VAR = "CONFLUENCE_API_KEY"


def env_error(name: str) -> str:
    return f"Error: {name} environment variable not set"


def get_base_url() -> str:
    url = os.environ.get(BASE_URL_VAR)
    if not url:
        print(env_error(BASE_URL_VAR), file=sys.stderr)
        sys.exit(1)
    return url


def get_api_key() -> str:
    key = os.environ.get(API_KEY_VAR)
    if not key:
        print(env_error(API_KEY_VAR), file=sys.stderr)
        sys.exit(1)
    return key


def get_headers() -> dict[str, str]:
    return {
        "X-Atlassian-Token": "no-check",
        "Authorization": f"Bearer {get_api_key()}",
        "Content-Type": "application/json",
    }


def api_request(method: str, path: str, **kwargs) -> requests.Response:
    url = f"{get_base_url()}/rest/api/{path}"
    response = requests.request(method, url, verify=False, **kwargs)

    if response.status_code == 200:
        return response
    print(
        f"Error: API request failed. Status code: {response.status_code}",
        file=sys.stderr,
    )
    print(response.text, file=sys.stderr)
    sys.exit(1)


def get_page_data(page_id: str, expand: str | None = None, version: int | None = None) -> dict:
    params = {}
    if expand:
        params["expand"] = expand
    if version:
        params["version"] = version
    return api_request(
        "get", f"content/{page_id}", headers=get_headers(), params=params
    ).json()


def put_page_data(page_id: str, title:str, version:int, content: str | None = None) -> dict:
    body = {
        "id": page_id,
        "type": "page",
        "title": title,
        "version": {"number": version},
    }
    if content is not None:
        body["body"] = {
            "storage": {"value": content, "representation": "storage"},
        }
    return api_request(
        "put", f"content/{page_id}", headers=get_headers(), json=body
    ).json()


def search_pages_by_content(text: str) -> dict:
    params = {}
    cql = f'text~"{text}" and type="page"'
    params["cql"] = cql
    params["limit"] = 25

    return api_request(
        "get", "content/search", headers=get_headers(), params=params
    ).json()


def print_usage() -> None:
    print("Usage: confluence <command> [arguments]", file=sys.stderr)
    print("Commands:", file=sys.stderr)
    print("  get-content <page_id> [version] Get page content (HTML)", file=sys.stderr)
    print(
        "  set-content <page_id> <file>   Set page content from HTML file",
        file=sys.stderr,
    )
    print(
        "  get-version <page_id>          Get current version number", file=sys.stderr
    )
    print("  get-title <page_id>            Get page title", file=sys.stderr)
    print("  set-title <page_id> <title>    Set page title", file=sys.stderr)
    print(
        "  search-text <text>             Get pages objects, containing text",
        file=sys.stderr,
    )
    print(
        "  check-setup                    Check if environment variables are set",
        file=sys.stderr,
    )


def cmd_get_content(args: list[str]) -> None:
    if len(args) < 1 or len(args) > 2:
        print("Usage: confluence get-content <page_id> [version]", file=sys.stderr)
        sys.exit(1)
    page_id = args[0]
    
    try:
        version = int(args[1]) if len(args) == 2 else None
    except ValueError:
        print(f"Error: Version must be a number, but got '{args[1]}'", file=sys.stderr)
        sys.exit(1)
    
    data = get_page_data(page_id, "body.storage", version)
    print(data["body"]["storage"]["value"])


def cmd_set_content(args: list[str]) -> None:
    if len(args) != 2:
        print("Usage: confluence set-content <page_id> <html_file>", file=sys.stderr)
        sys.exit(1)
    page_id, html_file = args
    with open(html_file, "r") as f:
        content = f.read()
    data = get_page_data(page_id, "body.storage,version,title")
    version = int(data["version"]["number"]) + 1
    put_page_data(page_id, data["title"], version, content)


def cmd_get_version(args: list[str]) -> None:
    if len(args) != 1:
        print("Usage: confluence get-version <page_id>", file=sys.stderr)
        sys.exit(1)
    page_id = args[0]
    data = get_page_data(page_id, "version")
    print(data["version"]["number"])


def cmd_get_title(args: list[str]) -> None:
    if len(args) != 1:
        print("Usage: confluence get-title <page_id>", file=sys.stderr)
        sys.exit(1)
    page_id = args[0]
    data = get_page_data(page_id, "title")
    print(data["title"])


def cmd_set_title(args: list[str]) -> None:
    if len(args) != 2:
        print("Usage: confluence set-title <page_id> <title>", file=sys.stderr)
        sys.exit(1)
    page_id, title = args
    data = get_page_data(page_id, "version")
    version = int(data["version"]["number"]) + 1
    put_page_data(page_id, title, version)


def cmd_search_text(args: list[str]) -> None:
    if len(args) != 1:
        print("Usage: confluence search-text <text>", file=sys.stderr)
        sys.exit(1)
    text = args[0]

    data = search_pages_by_content(text)
    results = data["results"]
    print(f"Found {len(results)} pages:\n")

    for item in results:
        page_id = item.get("id", "N/A")
        title = item.get("title", "N/A")
        print(f"ID: {page_id}; Title: {title}")


def cmd_check_setup(args: list[str]) -> None:
    if args:
        print("Usage: confluence check-setup", file=sys.stderr)
        sys.exit(1)
    errors = []
    if not os.environ.get(BASE_URL_VAR):
        errors.append(BASE_URL_VAR)
    if not os.environ.get(API_KEY_VAR):
        errors.append(API_KEY_VAR)
    if errors:
        print(
            "Error: Missing environment variables:", ", ".join(errors), file=sys.stderr
        )
        sys.exit(1)
    print("OK: Environment variables are set")
    print(f"Base URL: {get_base_url()}")
    key = get_api_key()
    print(f"API Key: {key[:4]}...{key[-4:]}")


def main() -> None:
    urllib3.disable_warnings()
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)
    command = sys.argv[1]
    args = sys.argv[2:]
    commands = {
        "get-content": cmd_get_content,
        "set-content": cmd_set_content,
        "get-version": cmd_get_version,
        "get-title": cmd_get_title,
        "set-title": cmd_set_title,
        "check-setup": cmd_check_setup,
        "search-text": cmd_search_text,
    }
    if command in commands:
        commands[command](args)
    else:
        print(f'Error: Unknown command "{command}"', file=sys.stderr)
        print_usage()
        sys.exit(1)


if __name__ == "__main__":
    main()
