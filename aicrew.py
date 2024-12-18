## pip install crewai crewai-tools langchain-ollama 
## pip install --upgrade crewai

from crewai import Crew, Agent, Task
from crewai import LLM

ollm = LLM(
    model="ollama/llama3.2:1b",
    base_url="http://localhost:11434"
)

# Define agents
def weather_report_agent():
    return Agent(
        role="Expert Weather Report Agent",
        goal="Create a detailed weather report for the the particular date of the given city.",
        backstory=( "Create a detailed weather report for the the particular date of the given city.  Check for any weather alerts. Give weather alerts if any and the precautions to be taken if any alert exists."),
        llm='ollama/llama3.2:1b', 
        #llm=ollm
    )

# Define a task 
def identify_weather(agent, city):
    return Task(
        description="Get me the WEATHER REPORT OF TODAY {city} .",
        expected_output="Get me the WEATHER REPORT OF TODAY for {city}. You MUST give a detailed Weather Report of the city for the current day precautions that has to be taken if there's a bad weather. For example carry an umberella when its rainy.",
        agent=agent
    )

weather_report_agent = weather_report_agent()
weather_report_task = identify_weather(agent=weather_report_agent,city="New York")

# Create a crew with agents and tasks
crew = Crew(agents=[weather_report_agent], tasks=[weather_report_task])

result = crew.kickoff()
print(result)
