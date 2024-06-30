# COM-B-workflow
## Setup

1. Clone the repository or download the script files.
2. Create a virtual environment.
3. Activate the virtual environment.
4. Install the required dependencies.
5. Create a `.env` file 
6. Set your OpenAI API key in an environment variable `OPENAI_API_KEY`.
    1. Obtain an API key from OpenAI by creating an account and following the instructions.
    1. Go to https://platform.openai.com/account/api-keys and create a new API key.
    1. Save this key in the `.env` file and to a password manager

### Commands
Script to create a virtual environment, installs the dependencies, and creates a `.env` file if it does not exist.

Linux and macOS commands:
```shell
python3 -m venv venv
source venv/bin/activate
if [ ! -f .env ]; then cp .env.template .env; fi
pip3 install -r requirements.txt
```

Windows commands:
```shell
python -m venv venv
venv\Scripts\activate
if not exist .env copy .env.template .env
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

Run the script using Python:
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
- OpenAI API key
- Internet connection

## Dependencies

The required dependencies are listed in the `requirements.txt` file:

```text
OpenAI
pyperclip
python-dotenv
os
argparse
```

## References:
TM 3-53.11 (2024)

The Behavior Change Wheel 
  - https://www.behaviourchangewheel.com/about-wheel
  - https://www.behaviourchangetheories.com/
