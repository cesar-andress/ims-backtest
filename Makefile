.PHONY: install test lint data build analysis outputs legacy all

UV ?= uv

install:
	$(UV) sync

lint:
	$(UV) run ruff check src tests

test:
	$(UV) run pytest -q

data:
	$(UV) run imsfe download

build:
	$(UV) run imsfe build

analysis:
	$(UV) run imsfe run

outputs:
	$(UV) run imsfe report

legacy:
	$(UV) run imsfe legacy

all: data build analysis outputs
