FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir \
    fastmcp==3.3.1 \
    httpx==0.28.1

# Built from this repo (kinghrothgar/netbox-mcp). Bump the tag when bumping
# the source.
COPY netbox_mcp /app/netbox_mcp

USER 65534

EXPOSE 8000

CMD ["python", "-m", "netbox_mcp"]
