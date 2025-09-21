.venv/bin/activate: requirements.txt
	python3 -m venv .venv
	.venv/bin/pip3 install --upgrade pip
	.venv/bin/pip3 install -r requirements.txt

.venv/bin/hatch: .venv/bin/activate
	.venv/bin/pip3 install hatch hatch-requirements-txt

.venv/bin/ruff: .venv/bin/activate
	.venv/bin/pip3 install ruff

install: .venv/bin/hatch
	.venv/bin/pip3 install .

check: .venv/bin/ruff 
	.venv/bin/ruff check
	.venv/bin/ruff format --check

fix: .venv/bin/ruff
	.venv/bin/ruff check --fix
	.venv/bin/ruff format

image: 
	docker build . -t clwb-sandbox

clean:
	find . -name .venv -prune -o -name __pycache__ | xargs rm -rf

.PHONY: install clean image


