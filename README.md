# Reddit Analyzer

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

### Run the app locally
- `source .env`
- `flask run`

### Run the tests locally
- `python -m pytest`

## CI/CD
- I've setup the CI/CD pipeline using Github Actions. The workflow can be found here: [.github/workflows/main.yml](https://github.com/karansangha/dtsa-5509-twitter-analyzer/blob/main/.github/workflows/main.yml)

### Continuous Integration
- The unit & integration tests are run on every push to the `main` branch.
- If the tests don't pass, I get an email detailing which step of the testing suite failed.
- The workflow doesn't proceed to the next step, i.e. deployment to `Heroku`.

### Continuous Deployment
- If all the tests pass, the build is deployed to `Heroku` at [https://dtsa-5509-reddit.herokuapp.com](https://dtsa-5509-reddit.herokuapp.com)
- This part of the workflow isn't run if any of the tests fail.
