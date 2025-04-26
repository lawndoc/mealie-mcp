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
git clone https://github.com/lawndoc/mealie-mcp
cd mealie-mcp
uv venv
uv run mealie_mcp
```

### Client Usage Examples

TODO

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
export MEALIE_URL="https://mealie.yourdomain.com"
export MEALIE_USERNAME="username" 
export MEALIE_PASSWORD="example_password"
export MEALIE_MCP_LOG_LEVEL="DEBUG"
export MEALIE_MCP_LOG_FILE="/var/log/mealie-mcp.log"
```

## Features

### Recipe Management

Resources:

- List all recipes in your Mealie instance
- Search recipes by name or ingredients
- Get detailed information about specific recipes

### Meal Planning

Resources:

- View all meal plans

Tools:

- Add a random recipe to a meal in your plan
- Add specific recipes to a meal in your plan

### Shopping Lists

Resources:

- Retrieve all shopping lists
- Get detailed contents of a specific shopping list

Tools:

- Add a recipe's ingredients to a specific shopping list

## Development

Use black for standardized formatting before contributing changes

```bash
uv run black src/
```

## Technical Details

The project implements a custom HTTPX client wrapper that automatically handles authentication and token refreshing. If a request fails due to an expired token, the client will reauthenticate and retry the request transparently.

## Requirements

- Python 3.10+
- HTTPX 0.28.1+
- MCP 1.6.0+

## License

[Add license information here]