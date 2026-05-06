FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

ENV UV_TOOL_BIN_DIR=/usr/local/bin
WORKDIR /app
COPY . /app
RUN uv sync --locked
ENV PYTHONPATH="${PYTHONPATH}:/app"
CMD ["uv", "run", "discord_bot"]