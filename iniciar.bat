@echo off

IF NOT EXIST "env" (
	python -m venv env
)

call env\Scripts\activate

pip install -r requirements.txt

python app.py