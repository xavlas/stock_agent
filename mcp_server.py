from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent.fetcher import get_evolution

app = FastAPI(title="MCP Stock Agent")

class MCPRequest(BaseModel):
    agent: str
    action: str
    params: dict = {}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/mcp")
async def mcp(req: MCPRequest):
    if req.agent != "stock_evolver":
        raise HTTPException(status_code=404, detail="Unknown agent")

    if req.action == "get_evolution":
        ticker = req.params.get("ticker")
        if not ticker:
            raise HTTPException(status_code=400, detail="Missing 'ticker' in params")
        period = req.params.get("period", "1mo")
        interval = req.params.get("interval", "1d")
        try:
            result = get_evolution(ticker, period=period, interval=interval)
            return {"success": True, "payload": result}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    raise HTTPException(status_code=400, detail="Unknown action")
