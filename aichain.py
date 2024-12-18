

from langchain_ollama.chat_models import ChatOllama
from langchain_core.tools import tool

@tool
def get_weather(city: str):
    """Give me name of city, I return current weather"""
    return "19 degree and foggy"

llm = ChatOllama(model="llama3.2:1b").bind_tools(tools=[get_weather])

res = llm.invoke("what is the weather in London?")
print(res)
print("-----")
print(res.tool_calls[0])
exit(1)


#########################

# https://github.com/langchain-ai/langchain/discussions/21907


from langchain_core.output_parsers import PydanticToolsParser
from langchain_ollama.chat_models import ChatOllama
from langchain.tools import Tool
from langchain.prompts import PromptTemplate
from langchain.tools import tool
from langchain.agents import AgentExecutor, create_react_agent
from langchain.memory import ConversationBufferWindowMemory
prompt = PromptTemplate(template="""
                            Answer the following question as best you can. You have access to the following tools: {tools}. 
                            You are allowed to take at one two actions. After one actions, you must provide a final answer.
                            Use the following format:
                            Question: the input question you must answer
                            Thought: you should always think about what to do next
                            Action: the action to take, should be one of [{tool_names}]
                            Action Input: the input to the action
                            Observation: the result of the action
                            ... (this Thought/Action/Action Input/Observation can repeat N times)
                            Thought: I now know the final answer
                            Final Answer: the final answer to the original input question
                            Begin! 
                            Question: {input}
                            Thought: {agent_scratchpad}""",
                            input_variables=['agent_scratchpad', 'input', 'tool_names', 'tools'])
@tool
def weather(city: str) -> str:
    """Get the current weather in a given city."""
    print(f"Getting weather for {city}")
    return f"The weather in {city} is 65 degrees Fahrenheit"

llm = ChatOllama(model="llama3.2:1b")
tools=[weather]
llm_with_tools = llm.bind_tools(tools)

agent = create_react_agent(llm,tools,prompt)
memory = ConversationBufferWindowMemory(return_messages=True, memory_key='chat_history', input_key='input', k=5)
agent_executor = AgentExecutor(agent=agent,tools=tools,verbose=True,memory=memory,handle_parsing_errors=True)

query = "What's the weather like today in San Francisco? Ensure you use the 'get_current_weather' tool."
response = agent_executor.invoke({'input':query})
print(response)

######################

# #pip install langchain langchain-ollama ollama


# from langchain_ollama.chat_models import ChatOllama
# from langchain_openai.chat_models import ChatOpenAI
# from pydantic import BaseModel
# from langchain_core.output_parsers import PydanticToolsParser

# class AdditionTool(BaseModel):
#     int_1:int
#     int_2:int

# llm = ChatOllama(model="llama3.2:1b")
# llm_with_tools = llm.bind_tools(tools = [AdditionTool])

# query = "What is 3 * 12?"


# chain = llm_with_tools | PydanticToolsParser(tools=[AdditionTool])
# result = chain.invoke(query)
# print(result)

##############

# from langchain_core.tools import StructuredTool


# def multiply(a: int, b: int) -> int:
#     """Multiply two numbers."""
#     return a * b

# calculator = StructuredTool.from_function(func=multiply)

# print(calculator.invoke({"a": 2, "b": 3}))

##############

# from langchain_core.output_parsers import PydanticToolsParser

# def weather_agent(city: str)  -> str:
#     print(f"Getting weather for {city}")
#     return f'''The weather in {city} is 65 degrees Fahrenheit'''

# from langchain_ollama.chat_models import ChatOllama
# llm = ChatOllama(model="llama3.2:1b")
# llm_with_tools = llm.bind_tools(tools = [weather_agent])
# query ="What's the weather like today in San Francisco? Ensure you use the 'get_current_weather' tool."
# # result = llm_with_tools.invoke(query);
# # print(result)

# chain = llm_with_tools | PydanticToolsParser(tools=[llm_with_tools])
# result = chain.invoke(query)
# print(result)
