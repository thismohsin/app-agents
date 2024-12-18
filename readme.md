# Navigate to your project directory
cd /path/to/your/project

# Create the virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install
pip install git+https://github.com/openai/swarm.git
pip install crewai crewai-tools langchain-ollama 
pip install --upgrade crewai
pip install langchain langchain-ollama ollama

# Run
```
./venv/bin/python ./ex.py
```