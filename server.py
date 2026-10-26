"""Servidor MCP para a API Tesouro Direto do Radar Opções (https://api.radaropcoes.com/docs)."""

import os
from urllib.parse import quote

import httpx
from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

BASE_URL = os.environ.get("RADAR_API_URL", "https://api.radaropcoes.com")
RADAR_TOKEN = os.environ.get("RADAR_TOKEN", "")

mcp = MCPServer(
    "radaropcoes",
    instructions=(
        "Consulta preços e taxas do Tesouro Direto em tempo real via API do Radar Opções. "
        "Use listar_titulos para descobrir o nome exato e consultar_titulo para os detalhes."
    ),
)


async def _get(path: str, auth: bool = False) -> dict:
    headers = {"Authorization": f"Bearer {RADAR_TOKEN}"} if auth else {}
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=15) as client:
        response = await client.get(path, headers=headers)
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def listar_titulos() -> list[dict]:
    """Lista todos os títulos do Tesouro Direto não vencidos, com a data do último preço de cada um.
    `em_negociacao` é true quando o título apareceu na leitura mais recente; false indica negociação
    suspensa ou dado antigo (confira `atualizado_em`). Use o `nome` exato em consultar_titulo."""
    data = await _get("/bonds.json")
    # Os suspensos ficam com o updated_at da última leitura em que apareceram
    ultima_leitura = data["updated_at"]
    return [
        {
            "nome": item["TrsrBd"]["nm"],
            "atualizado_em": item["TrsrBd"]["updated_at"],
            "em_negociacao": item["TrsrBd"]["updated_at"] == ultima_leitura,
        }
        for item in data["response"]["TrsrBdTradgList"]
    ]


@mcp.tool()
async def consultar_titulo(nome: str) -> dict:
    """Detalhes de um título do Tesouro Direto: preço unitário de investimento e de resgate, taxas,
    vencimento e investimento mínimo. `nome` é o nome exato, ex.: "Tesouro IPCA+ 2035"."""
    if not RADAR_TOKEN:
        raise ToolError("RADAR_TOKEN não configurado. Gere um token em https://radaropcoes.com/profile/token.")
    try:
        bond = await _get(f"/bonds/{quote(nome, safe='')}", auth=True)
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise ToolError(f"Título não encontrado: {nome}") from e
        raise
    # A API responde 200 com treasuryBondCode nulo e o motivo em `indication` quando falha
    if bond.get("treasuryBondCode") is None:
        raise ToolError(bond.get("indication") or f"Título não encontrado: {nome}")
    return bond


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
