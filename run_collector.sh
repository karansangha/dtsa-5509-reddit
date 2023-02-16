echo "Setting up virtual environment"
python3 -m venv .venv

echo "Activating virtual environment"
source .venv/bin/activate
pip install -r requirements.txt > /dev/null 2>&1 || echo "Error installing dependencies. Please run pip install -r requirements.txt manually"

echo "Starting Data Collector"
python3 src/data_collector/collector.py
