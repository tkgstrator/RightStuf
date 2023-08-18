.PHONY: build
build:
	act --secret-file .secrets -P ubuntu-20.04=node:16-buster-slim -j build --container-architecture linux/amd64
