echo "Setting up virtual environment"
python3 -m venv .venv

echo "Activating virtual environment"
source .venv/bin/activate
pip install -r requirements.txt > /dev/null 2>&1 || echo "Error installing dependencies. Please run pip install -r requirements.txt manually"

echo "Loading environment variables"
source .env

echo "Running the tests"
python -m pytest -v
