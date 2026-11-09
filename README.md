# SiliconCrew Demo

SiliconCrew is a small web demo of an LLM-assisted RTL workflow: describe a digital design, generate Verilog, and lint/simulate it with local EDA tools. It includes a Next.js workbench, a FastAPI backend, an example gallery, and an optional MCP server.

## Quick start

### Requirements

- Python 3.10+
- Node.js 18+ and npm
- Icarus Verilog (`iverilog` and `vvp`) for linting and simulation
- An API key from Google, OpenAI, or Anthropic

The demo path uses local tools; Docker and deployment setup are not needed.

### Install

```bash
git clone https://github.com/mfzhang/LLM-RTL-siliconcrew.git
cd LLM-RTL-siliconcrew

python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt

cp .env.example .env
# Add your provider API key to .env

cd frontend
npm ci
cd ..
```

Install Icarus Verilog with your system package manager if it is not already available (for example, `sudo apt install iverilog` on Debian/Ubuntu or `brew install icarus-verilog` on macOS).

### Run

Start the backend:

```bash
source .venv/bin/activate
uvicorn api:app --reload --port 8000
```

In a second terminal, start the web app:

```bash
cd frontend
npm run dev
```

Open <http://localhost:3000>, choose an example or start a session, and ask for a small design such as a 4-bit counter. The workbench shows the generated specification, RTL, tool activity, and simulation artifacts.

## What is included

- LLM-driven spec and Verilog generation
- Local lint/simulation through Icarus Verilog
- Example designs and precomputed demo artifacts
- Session history and artifact viewers
- Optional MCP server for local MCP clients

To run the MCP server locally, use `python mcp_server.py` from the activated virtual environment. See [docs/MCP_SETUP.md](docs/MCP_SETUP.md) for client configuration.

## Demo scope

This checkout intentionally omits CI/deployment workflows, cloud deployment files, and Docker images. The lightweight demo covers RTL generation and local verification. Advanced physical-design, formal, XLS, and container-backed flows are not part of the quick-start setup and may require extra tools.

## Tests

```bash
# Backend tests that do not require external EDA tools or services
pytest -m 'not requires_eda and not slow and not requires_services' -q

# Frontend unit tests
cd frontend && npm test
```

See [docs/TESTING.md](docs/TESTING.md) for the optional tool-dependent test set.

## License

MIT. See [LICENSE](LICENSE).
