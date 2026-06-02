IMAGE    ?= kinghrothgar/netbox-mcp
TAG      ?= dev
ENV_FILE ?= .env

# Pull MCP_PORT (and any other vars) from $(ENV_FILE) into make's namespace
# if the file exists. Lines must be simple KEY=value (no quotes, no spaces).
-include $(ENV_FILE)

MCP_PORT ?= 8000

.PHONY: build-dev run-dev

build-dev:
	docker buildx build --tag $(IMAGE):$(TAG) --pull .

run-dev:
	docker run --rm -it \
		--env-file $(ENV_FILE) \
		-p 127.0.0.1:$(MCP_PORT):$(MCP_PORT) \
		$(IMAGE):$(TAG)
