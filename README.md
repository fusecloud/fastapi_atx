# fastapi_atx
Repo for the apps built in the Austin FastAPI Developers Meetup group

## Poetry package management

1. Install poetry package and dependecy manager
   
   a. On Mac.
        
       $ brew install poetry

   b. On Linux (REL).
   
       $ dnf search poetry
       ================= Name Exactly Matched: poetry ========================
       poetry.noarch : Python dependency management and packaging made easy

       $ sudo dnf install poetry 

2. Check if poetry has been installed.

       $ poetry --version
       Poetry version 1.1.5

3. Create a basic `pyproject.toml`.

       $ poetry init

```toml
[tool.poetry]
name = "fastapi_atx"
version = "0.1.0"
description = "apps built in the Austin FastAPI Developers Meetup group"
authors = ["Your Name <you@example.com>"]

[tool.poetry.dependencies]
python = "^3.9"

[tool.poetry.dev-dependencies]

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"

```

4. Virtual environments.
After many years I have found that the easiest tool to manage python environments is [`pyenv`](https://github.com/pyenv/pyenv). 
   
       $ brew install pyenv
       
       $ pyenv --version
       pyenv 1.2.18
       
       $ pyenv install 3.9.0a6 
       Downloading Python-3.9.0a6.tar.xz...
       -> https://www.python.org/ftp/python/3.9.0/Python-3.9.0a6.tar.xz
       Installing Python-3.9.0a6...
       Installed Python-3.9.0a6 to /home/adrian/.pyenv/versions/3.9.0a6

Now we have two options, use `pyenv local <version>` or `poetry env use <path/to/env>`:

- Virtual environment management with `pyenv`.

This configuration is prefered when the project has a CI test suite that runs inside a docker container.

    # Check current python environment.
    $ python --version
    Python 3.7.7
      
    # Define local environment.
    $ pyenv virtualenv 3.9.0a6 fastapi_atx-3.9.0
    $ pyenv local fastapi_atx-3.9.0
    $ python --version
    Python 3.9.0a6

    # Poetry avoid virtual environment creation and use local environment.
    $ poetry config virtualenvs.create false --local
    # Check poetry configuration
    $ poetry config --list
    cache-dir = "$USER/.cache/pypoetry"
    experimental.new-installer = true
    installer.parallel = true
    virtualenvs.create = false <- Previous configuration changed this line
    virtualenvs.in-project = null <- Set to true to create virtual environments in /<projec>/.venv
    virtualenvs.path = "{cache-dir}/virtualenvs"  # /home/adrian/.cache/pypoetry/virtualenvs


- Virtual environment management with `poetry`.

It is possible to configure poetry to automatically create a virtual environment within the project folder.

    $ poetry config virtualenvs.create true --local
    $ poetry config virtualenvs.in-project true --local
    # Check poetry configuration
    $ poetry config --list
    cache-dir = "$USER/.cache/pypoetry"
    experimental.new-installer = true
    installer.parallel = true
    virtualenvs.create = true <- Previous configuration changed this line
    virtualenvs.in-project = true <- Set to true to create virtual environments in /<projec>/.venv
    virtualenvs.path = "{cache-dir}/virtualenvs"  # /home/adrian/.cache/pypoetry/virtualenvs


5. Installing packages.

- Production packages. `$ poetry add <package-name>`
- Development packages. `$ poetry add -D <package-name>`
