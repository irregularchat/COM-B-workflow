# COM-B-workflow
## Setup
0. Install Package Manager:
    - MacOS: # install [homebrew](https://brew.sh/)
    ```shell
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```
    - Windows: # install [chocolatey](https://chocolatey.org/install)
    ```shell
    Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
    ```
1. Clone the repository or download the script files. 
2. Create a virtual environment.
3. Activate the virtual environment.
4. Install the required dependencies.
5. Create a `.env` file 
6. Set your OpenAI API key in an environment variable `OPENAI_API_KEY`.
    1. Obtain an API key from OpenAI by creating an account and following the instructions.
    1. Go to https://platform.openai.com/account/api-keys and create a new API key.
    1. Save this key in the `.env` file and to a password manager

## How to contribute
1. Fork the repository (click the fork button at the top right of the page)
2. Create a branch (git checkout -b feature/feature-name)
3. Make your changes and commit them (git commit -am 'Add some feature' OR edit directly on the browser press . to launch the editor)
4. Push your changes to your fork 
5. Create a pull request (select the main branch as the base branch and your branch as the compare branch)
6. Wait for the pull request to be reviewed

### Commands
Clone the repository:
```shell
git clone https://github.com/irregularchat/COM-B-workflow.git
cd COM-B-workflow
```

Script to create a virtual environment, installs the dependencies, and creates a `.env` file if it does not exist.

#### Linux and macOS commands:
**Activate the virtual environment**
```shell
python3 -m venv venv
source venv/bin/activate
```
**Create the .env file, set permissions, and install the dependencies**
```shell
if [ ! -f .env ]; then cp .env.template .env; fi
#set permissions for the .env file
chmod 600 .env #set permissions for the .env file to read/write only for the owner
pip3 install -r requirements.txt
```

#### Windows commands:
**Activate the virtual environment**
```shell
python -m venv venv
venv\Scripts\activate
```
**Create the .env file, set permissions, and install the dependencies**
```shell
if not exist .env copy .env.template .env
icacls .env /inheritance:r #remove inherited permissions
pip install -r requirements.txt
```

## Running the Script
### First make sure that you edit .env file and add your OpenAI API key and other requirements
The more you add in here the faster prompting will be. The .env file is not synced with the git repository so you can add your own information in there.
Linux and macOS commands:
```shell
nano .env
```

Windows commands:
```shell
notepad .env
```

### Run the script using Python:
This script is focused more on creating a mission statement and identifying a center of gravity. 

```shell
python3 cog.py
```

This script is focused more on identifying then refining the target audience using the COM-B model and leading to the HPEM. 
```shell
python3 refine_ta.py
```

## Requirements

- Python 3
- Git (To clone the repository OR download the script files directly like an animal)
- OpenAI API key
- Internet connection

## Dependencies

The required dependencies are listed in the `requirements.txt` file:

```text
OpenAI
pyperclip
python-dotenv
argparse
os
colorama
```

## References:
TM 3-53.11 (2024)

The Behavior Change Wheel 
  - https://www.behaviourchangewheel.com/about-wheel
  - https://www.behaviourchangetheories.com/
