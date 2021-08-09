# Welcome to the PyClinic

A library to test services in Python

## Setup and Contribute

💡 Use `Poetry` as the package manager to take advantage of the `pyproject.toml` at the Workspace Root

> ⚠️ Python version 3.9 or higher is required

1. Clone/Fork this repo and open it in your favorite editor (VS Code, Pycharm, etc)

2. Open the Integrated Terminal and use Poetry to install all dependencies

   ```bash
   # this also creates the virtual environment automatically
   poetry install
   ```

3. Configure your IDE

   - Select Interpreter - Gives you autocomplete, intellisense, etc
   - Configure Tests - We use `pytest` instead of the default `unittest` library
   - Any other settings. This project uses a Formatter (`black`) and Linter (`flake8`)

4. That's it! Run the tests to see it all work

   ```bash
   poetry run poe test
   ```

5. Make your changes, then submit a Pull Request (PR) for review. This automatically triggers a pipeline that lints and runs tests. Once the pipeline is green, a **Maintainer** will review your PR! 😄

> Shoutout to @sudomaze from Twitch 💪🏽🐍
