run:
	python3 a_maze_ing.py config/config.conf

debug:
	python3 -m pdb a_maze_ing.py config/config.conf

clean:
	rm -rf *__pycache__ *.mypy_cache */*.txt *.txt */*__pycache__ */*.mypy_cache

lint:
	flake8 maze/mazegen.py
# 	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
# 	mypy  maze/mazegen.py --strict
install:
	python3 -m venv venv
	pip install .
	
