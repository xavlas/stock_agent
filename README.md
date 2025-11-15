MCP Stock Agent

This project implements a Model Context Protocol (MCP) agent that fetches stock price evolution for a given ticker. It works with VS Code and other MCP-compatible clients.

What it contains

- `mcp_vscode_server.py` - MCP stdio server for VS Code integration.
- `mcp_server.py` - FastAPI app exposing a simple HTTP endpoint (alternative interface).
- `agent/fetcher.py` - Uses `yfinance` to fetch historical price data and compute evolution.
- `tests/test_fetcher.py` - Unit test that mocks yfinance to validate the fetcher.
- `requirements.txt` - Python dependencies.
- `vscode_mcp_settings.json` - VS Code MCP configuration example.

Quick start

1. Create a virtualenv and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Run the server:

```bash
uvicorn mcp_server:app --reload --port 8000
```

3. Example request (get evolution for ticker `AAPL`):

```bash
curl -sS -X POST http://127.0.0.1:8000/mcp -H 'Content-Type: application/json' -d '{"agent":"stock_evolver","action":"get_evolution","params":{"ticker":"AAPL","period":"1mo","interval":"1d"}}' | jq
```

Notes & assumptions

- This is a minimal scaffold. The MCP contract here is simple JSON over HTTP: `{agent, action, params}`.
- We use `yfinance` which does not require an API key. For production-grade usage consider a paid market data provider.

## Use in VS Code chat (MCP)

1) Configure the MCP server in VS Code settings (User or Workspace):

```json
{
	"mcpServers": {
		"stock-evolution": {
			"command": "python",
			"args": [
				"/Users/xavier/Documents/github/mcp_stock_agent/mcp_vscode_server.py"
			],
			"env": {
				"PYTHONPATH": "/Users/xavier/Documents/github/mcp_stock_agent"
			}
		}
	}
}
```

2) In the VS Code Chat, type something like: “Use tool get_stock_evolution with ticker=AAPL period=1mo interval=1d”.

Tip: You can also run the HTTP server (`uvicorn`) and curl it directly, but the MCP stdio server is what VS Code uses.

## Run CI locally with act (optional)

If you want to run GitHub Actions locally:

- Prerequisites: Docker Desktop (or Colima) installed and running.
- Install act:

```bash
brew install act
```

- We included a `.actrc` that maps `ubuntu-latest` to a Docker image compatible with act. From the project root:

```bash
act -l             # List available workflows/jobs
act -j test        # Run the test job
act -j build       # Run the build job
```

Note: You do not need `act` to use GitHub-hosted runners. Simply push to GitHub or open a PR and the workflow in `.github/workflows/ci.yml` will run in the cloud.
