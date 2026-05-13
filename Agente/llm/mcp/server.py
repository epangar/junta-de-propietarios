from fastmcp import FastMCP

mcp = FastMCP("Excel MCP Server")

@mcp.tool()
def analyze_errors(errors: list) -> dict:
    return {
        "summary": f"{len(errors)} errores detectados",
        "errors": errors
    }

@mcp.tool()
def get_template() -> dict:
    return {
        "columns": [
            "fecha",
            "tipo",
            "categoria",
            "concepto",
            "ingresos",
            "gastos"
        ]
    }

if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="127.0.0.1",
        port=8001
    )