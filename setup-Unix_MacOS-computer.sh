python -m venv .venv
source .venv/bin/activate
echo 'current python path: '
echo $(.venv/bin/python)
python -m pip install -r dependencies.txt