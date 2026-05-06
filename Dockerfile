FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# Copy only dependency files first (better caching)
COPY pyproject.toml uv.lock* /app/

RUN uv sync --locked

# Now copy source code
COPY . /app

# Reinstall your package to ensure it's fresh
RUN uv pip install .

CMD ["uv", "run", "discord-bot"]