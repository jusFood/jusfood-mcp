# jusfood-mcp

```js
python3 -m venv .venv

source .venv/bin/activate
```

### deploy to local Claude app

```js
mcp install index.py
```

### MCP config

```js
{
  "mcpServers": {
    "jusfood": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "mcp[cli]",
        "mcp",
        "run",
      ]
    }
  }
}
```

python-sdk resource: https://github.com/modelcontextprotocol/python-sdk

youtube tutorial resource: https://www.youtube.com/watch?v=cdBRAVYZKFo
