# radaropcoes-mcp

Servidor MCP (stdio) para a [API Tesouro Direto do Radar Opções](https://api.radaropcoes.com/docs).

## Tools

- `listar_titulos` `GET /bonds.json` (público): todos os títulos não vencidos, com `atualizado_em` e `em_negociacao` (false = suspenso ou dado antigo).
- `consultar_titulo(nome)` `GET /bonds/{nome}` (requer token): preços unitários, taxas, vencimento, mínimo.

## Instalação

Requer Python 3.12+. Gere o token em https://app.radaropcoes.com/profile/token.

**Sem clonar, com [uv](https://docs.astral.sh/uv/):** o `uvx` baixa e executa direto do GitHub. Comando do servidor:

```bash
uvx --from git+https://github.com/danperrout/radaropcoes_mcp radaropcoes-mcp
```

Nos exemplos abaixo, isso equivale a `"command": "uvx"` e `"args": ["--from", "git+https://github.com/danperrout/radaropcoes_mcp", "radaropcoes-mcp"]`.

**Clonando o repositório:**

```bash
git clone https://github.com/danperrout/radaropcoes_mcp.git
cd radaropcoes_mcp
```

**Com [uv](https://docs.astral.sh/uv/) (recomendado):** nada mais a fazer — o `uv run` cria o ambiente e instala as dependências na primeira execução. Comando do servidor:

```bash
uv run --directory /caminho/para/radaropcoes_mcp server.py
```

**Sem uv (venv + pip):**

```bash
python3 -m venv .venv
.venv/bin/pip install "httpx>=0.28.1" "mcp[cli]>=2.3.0"   # Windows: .venv\Scripts\pip
```

Comando do servidor: `/caminho/para/radaropcoes_mcp/.venv/bin/python /caminho/para/radaropcoes_mcp/server.py` (Windows: `.venv\Scripts\python.exe`).

Nos exemplos abaixo, troque `command`/`args` por esse comando se não usar uv. Use sempre caminhos absolutos.

Variáveis: `RADAR_TOKEN` (obrigatória para `consultar_titulo`), `RADAR_API_URL` (padrão `https://api.radaropcoes.com`).

## Configuração por cliente

### Claude Code

```bash
claude mcp add radaropcoes -s user -e RADAR_TOKEN=rop_SEU_TOKEN \
  -- uv run --directory /caminho/para/radaropcoes_mcp server.py
```

### Claude Desktop, Cursor, Windsurf, Gemini CLI

Todos usam o mesmo formato `mcpServers`; muda só o arquivo:

| Cliente | Arquivo |
|---|---|
| Claude Desktop | Settings → Developer → Edit Config (`claude_desktop_config.json`) |
| Cursor | `~/.cursor/mcp.json` (global) ou `.cursor/mcp.json` (projeto) |
| Windsurf | `~/.codeium/windsurf/mcp_config.json` |
| Gemini CLI | `~/.gemini/settings.json` |

```json
{
  "mcpServers": {
    "radaropcoes": {
      "command": "uv",
      "args": ["run", "--directory", "/caminho/para/radaropcoes_mcp", "server.py"],
      "env": { "RADAR_TOKEN": "rop_SEU_TOKEN" }
    }
  }
}
```

Reinicie o cliente depois de editar. Se o cliente não achar o `uv`, use o caminho completo (`which uv`).

### VS Code (GitHub Copilot)

`.vscode/mcp.json` no projeto (ou "MCP: Open User Configuration" na paleta de comandos):

```json
{
  "servers": {
    "radaropcoes": {
      "type": "stdio",
      "command": "uv",
      "args": ["run", "--directory", "/caminho/para/radaropcoes_mcp", "server.py"],
      "env": { "RADAR_TOKEN": "rop_SEU_TOKEN" }
    }
  }
}
```

### OpenAI Codex CLI

```bash
codex mcp add radaropcoes --env RADAR_TOKEN=rop_SEU_TOKEN \
  -- uv run --directory /caminho/para/radaropcoes_mcp server.py
```

Ou em `~/.codex/config.toml`:

```toml
[mcp_servers.radaropcoes]
command = "uv"
args = ["run", "--directory", "/caminho/para/radaropcoes_mcp", "server.py"]
env = { RADAR_TOKEN = "rop_SEU_TOKEN" }
```

## Testando

Inspecione as tools sem nenhum cliente de IA:

```bash
RADAR_TOKEN=rop_SEU_TOKEN uv run mcp dev server.py
```
