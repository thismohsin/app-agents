import json
from swarm import Agent, Swarm
import openai

## pip install git+https://github.com/openai/swarm.git

def getllama():
    client = openai.OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama"
    )
    return client

ollm = getllama()


def get_weather(location, time="now"):
    """Get the current weather in a given location. Location MUST be a city."""
    return json.dumps({"location": location, "temperature": "65", "time": time})


istream = False
weather_agent = Agent(
    name="Weather Agent",
    instructions="You are a helpful agent.",
    functions=[get_weather],
    llm=ollm,
    model='llama3.2:1b',
    stream=istream,
    temperature=0.2,
    max_tokens=25,
)

sclient = Swarm(client=ollm)
response = sclient.run(agent=weather_agent, messages=[{"role": "user", "content": "What is the weather in New York?"}])  
print(response.messages[-1].get("content"))
