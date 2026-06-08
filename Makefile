test:
	uv run python -m pytest --html=report.html

install:
    playwright install && \
    camoufox fetch