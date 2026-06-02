IMAGE      ?= kinghrothgar/netbox-mcp
TAG        ?= dev
TEST_IMAGE ?= netbox-mcp-test:dev
ENV_FILE   ?= .env

# Pull MCP_PORT (and any other vars) from $(ENV_FILE) into make's namespace
# if the file exists. Lines must be simple KEY=value (no quotes, no spaces).
-include $(ENV_FILE)

MCP_PORT ?= 8000

.PHONY: build-dev run-dev build-test test-demo

build-dev:
	docker buildx build --tag $(IMAGE):$(TAG) --pull .

run-dev:
	docker run --rm -it \
		--env-file $(ENV_FILE) \
		--network host \
		$(IMAGE):$(TAG)

build-test:
	docker buildx build --tag $(TEST_IMAGE) --pull -f tests/Dockerfile tests/

# Integration tests against demo.netbox.dev. Mounts the repo so the
# auto-bootstrapped .netbox-demo-creds.json persists on the host, and
# uses --network host so both the spawned netbox-mcp container and the
# test pytest process can reach the demo (egress) and each other
# (127.0.0.1:<random port>). Mounts the docker socket so the test
# process can spawn/stop the netbox-mcp container under test.
test-demo: build-dev build-test
	docker run --rm \
		--network host \
		-v $(PWD):/work -w /work \
		-v /var/run/docker.sock:/var/run/docker.sock \
		-e NETBOX_MCP_IMAGE=$(IMAGE):$(TAG) \
		$(TEST_IMAGE)
