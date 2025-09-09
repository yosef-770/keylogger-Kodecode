```
▗▖ ▗▖▗▄▄▄▖▗▖  ▗▖▗▖    ▗▄▖  ▗▄▄▖ ▗▄▄▖▗▄▄▄▖▗▄▄▖ 
▐▌▗▞▘▐▌    ▝▚▞▘ ▐▌   ▐▌ ▐▌▐▌   ▐▌   ▐▌   ▐▌ ▐▌
▐▛▚▖ ▐▛▀▀▘  ▐▌  ▐▌   ▐▌ ▐▌▐▌▝▜▌▐▌▝▜▌▐▛▀▀▘▐▛▀▚▖
▐▌ ▐▌▐▙▄▄▖  ▐▌  ▐▙▄▄▖▝▚▄▞▘▝▚▄▞▘▝▚▄▞▘▐▙▄▄▖▐▌ ▐▌
```

# Keylogger — פרויקט גמר

[![Postman](https://img.shields.io/badge/Postman-API_Tests-FF6C37?logo=postman&logoColor=white)](https://www.postman.com/telecoms-engineer-78795300/keylogger)


## Instruction:
### install the project
Requirements:
- `python` installed on your machine

run in your terminal:
```bash
git clone https://github.com/yosef-770/keylogger-Kodecode/
cd keylogger-Kodecode

# Create a venv environment
python3 -m venv venv
# For windows cmd:
venv\Scripts\activate
# For windows PowerShell:
.\venv\Scripts\Activate.ps1
# For Unix based (MacOs / Linux):
source venv/bin/activate

# Install the Requirements
pip install -r requirements.txt
```

### Run the Agent:
```bash
python main.py
```

If you want to run the agent in dev mode (depend on the server to run in the same machine):
```bash
python main.py debug
```

**That's it!**

Now we know all of your secrets 🤫

### Run the server:
First, you need to create a `.evn` file, contains the variables listed in `.env.example`.

TODO()
```bash
export PYTHONPATH=$(pwd)
python backend/app.py
```
