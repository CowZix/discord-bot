FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

ENV UV_TOOL_BIN_DIR=/usr/local/bin
WORKDIR /app
COPY . /app
RUN uv sync --locked
RUN uv pip install .
CMD ["uv", "run", "discord-bot"]