# Reddit Analyzer
![main.yml](https://github.com/karansangha/dtsa-5509-reddit/actions/workflows/main.yml/badge.svg)

- Currently the repo only hosts a rudimentary `flask` app with a few unit & integration tests.
- Over the next few weeks I will be adding a fully developed frontend with a data collector and a data analyzer.

## Run Individual Modules
### Data Collector
- `./run_collector.sh`
- If the above doesn't run, please try `chmod +x run_collector.sh` and try `./run_collector.sh` again.

### Data Analyzer
- `./run_analyzer.sh`
- If the above doesn't run, please try `chmod +x run_analyzer.sh` and try `./run_analyzer.sh` again.

## Development Environment
- Open a new terminal window in the root directory of this project
- `python3 -m venv .venv`
- `source .venv/bin/activate`
- `pip install -r requirements.txt`
- Please ensure you have `Docker Desktop` installed and running on your machine.

### Run the app locally
- `source .env`
- `docker-compose up -d`
- `flask run`
- Or run `./run_app.sh`
    - If the above doesn't run, please try `chmod +x run_app.sh` and try `./run_app.sh` again.

### Run the tests locally
- Activate the virtual env and run `python -m pytest`
- Or run `./run_tests.sh`
    - If the above doesn't run, please try `chmod +x run_tests.sh` and try `./run_tests.sh` again.

## CI/CD
- I've setup the CI/CD pipeline using Github Actions. The workflow can be found here: [.github/workflows/main.yml](https://github.com/karansangha/dtsa-5509-reddit/blob/main/.github/workflows/main.yml)

### Continuous Integration
- The unit & integration tests are run on every push to the `main` branch.
- If the tests don't pass, I get an email detailing which step of the testing suite failed.
- The workflow doesn't proceed to the next step, i.e. deployment to `Heroku`.

### Continuous Deployment
- If all the tests pass, the build is deployed to `Heroku` at [https://dtsa-5509-reddit.herokuapp.com](https://dtsa-5509-reddit.herokuapp.com)
- This part of the workflow isn't run if any of the tests fail.
