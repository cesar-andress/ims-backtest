.PHONY: install test lint data build analysis validate smaa ml matrix outputs legacy all

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

validate:
	$(UV) run imsfe validate

smaa:
	$(UV) run imsfe smaa

ml:
	$(UV) run imsfe ml

matrix:
	$(UV) run imsfe matrix

legacy:
	$(UV) run imsfe legacy

# Regenerate manuscript tables/figures from data/processed + existing analysis CSVs.
outputs:
	$(UV) run imsfe report

# Full pipeline assuming data/raw is present (download is idempotent).
all: data build analysis validate smaa ml matrix legacy outputs
