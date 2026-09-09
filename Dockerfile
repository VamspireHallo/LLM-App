FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY app.py .

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 7860

CMD ["python", "app.py"]