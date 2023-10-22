setup:
	# pip install pre-commit
	# pre-commit install
	# python -m venv venv
	# source venv/bin/activate
	@make install
	pre-commit autoupdate

activate:
	source $(poetry env info --path)/bin/activate

install:
	# @ pip install --upgrade pip
	# @ pip install -r requirements.txt
	@pip install poetry
	@poetry install --no-root

install-ml-deps:
	poetry add --group ml $(cat requirements-ml.txt)


run:
  # @source venv/bin/activate
	# @python -m streamlit run app.py
	@poetry run streamlit run app.py

install-tests:
	# @python -m pip install -r requirements-test.txt
	@make install

test:
	@pytest -p no:cacheprovider
	@echo "testing complete"

clean:
	@echo "clean all temp folders"
	@find . -type d -name '.pytest_cache' -exec rm -rf {} +
	@find . -type d -name 'testcache' -exec rm -rf {} +
	@find . -type d -name '.benchmarks' -exec rm -rf {} +
	# @find . -type f -name '<_io.BytesIO object at*' -exec rm -f {} +
	@find . -type f -name '*.log' -exec rm -f {} +

docker:
	docker build -t  decenter.streamlit.app .

.PHONY: run install clean setup test activate docker

poetry-export:
	poetry export --with dev --format requirements.txt --output requirements-poetry.txt

export:
	conda env export --name ml > environment.yml export

zip_examples:
	zip -r sample_v2 .
