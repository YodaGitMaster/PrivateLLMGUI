# PrivateLLMGUI

![](https://raw.githubusercontent.com/YodaGitMaster/PrivateLLMGUI/main/images/logo.jpg)

## Requirements:
- python-3
- Graphic Card
- Ollama installed
- Windows

## Step 1: Ollama
- Download ollama from https://ollama.com/download/windows
- choose a model https://ollama.com/library (phi3)
- open a terminal
  - type  ```ollama run phi3```
  - wait it download
  - close that terminal

## Step 2: PrivateGPT
- open another terminal
- type ```git clone https://github.com/YodaGitMaster/PrivateLLMGUI.git```
- type ```cd PrivateLLMGUI```
- type ```pip install -r reuirements.txt```
- type ```python -m venv .env ```
- type ```.\.env\Scripts\activate ```
- type ```streamlit run .\index.py  ```
- navigate to your local browser http://localhost:5000
  
