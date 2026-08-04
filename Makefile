.PHONY: install dev test run stack clean

install:
	pip install -r requirements.txt

dev:
	pip install -r requirements.txt -r requirements-dev.txt

test:
	pytest tests/ -v

run:
	uvicorn src.main:app --reload

stack:
	docker-compose -f docker-compose.yml -f docker-compose.observability.yml up

examples:
	python examples/01_first_structured_log.py
	python examples/04_end_to_end_llm_trace.py

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
