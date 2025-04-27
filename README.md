# Mealie MCP

A Model Context Protocol (MCP) service for Mealie, the recipe management and meal planning application.

*__Warning__*: This server is undergoing intial development and does not yet implement any sort of authentication. Avoid exposing it on public networks.

## Overview

This project provides a MCP wrapper around the Mealie API, allowing AI assistants to interact with your Mealie instance. It enables functionality like:

- Searching and retrieving recipes
- Managing meal plans
- Working with shopping lists
- Adding meal plan recipe ingredients to shopping lists

## Usage

### Running the MCP Server

```bash
curl -o .env https://raw.githubusercontent.com/lawndoc/mealie-mcp/refs/heads/main/.env.template
vim .env
docker run -d --rm -p 8000:8000 --env-file .env ghcr.io/lawndoc/mealie-mcp:latest
```

### Client Usage Examples

MCP client config:

```json
"mcp": {
    "servers": {
        "mealie-mcp": {
            "type": "sse",
            "url": "http://localhost:8000/sse"
        }
    }
}
```

## Configuration

The application requires the following environment variables:

- `MEALIE_URL`: The base URL of your Mealie instance (e.g. "https://mealie.yourdomain.com")
- `MEALIE_USERNAME`: Your Mealie service account's username
- `MEALIE_PASSWORD`: Your Mealie service account's password

Optional logging configuration:

- `MEALIE_MCP_LOG_LEVEL`: Controls logging verbosity (DEBUG, INFO, WARNING, ERROR, CRITICAL). Defaults to INFO.
- `MEALIE_MCP_LOG_FILE`: Optional path to a log file. If not set, logs will only be output to the console.

Example setup:

```bash
MEALIE_URL="https://mealie.yourdomain.com"
MEALIE_USERNAME="username" 
MEALIE_PASSWORD="example_password"
MEALIE_MCP_LOG_LEVEL="DEBUG"
MEALIE_MCP_LOG_FILE="/var/log/mealie-mcp.log"
```

## Features

### Recipe Management

Tools:

- List all recipes in your Mealie instance
- Get detailed information about specific recipes
- Search recipes by name or ingredients

### Meal Planning

Tools:

- List all meals scheduled on the meal plan
- Add a random recipe to a meal in your plan
- Add specific recipes to a meal in your plan

### Shopping Lists

Tools:

- List all shopping lists
- Get detailed contents of a specific shopping list
- Add a recipe's ingredients to a specific shopping list

## Development

You must use [`uv`](https://docs.astral.sh/uv/) while developing this app.

### Setup

```bash
git clone https://github.com/lawndoc/mealie-mcp
cd mealie-mcp
uv sync
```

## Technical Details

The project implements a custom HTTPX client wrapper that automatically handles authentication and token refreshing. If a request fails due to an expired token, the client will reauthenticate and retry the request transparently.
