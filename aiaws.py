from langchain.agents import tool, AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_aws import ChatBedrockConverse

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

tools = [multiply]

llm_with_tools = ChatBedrockConverse(
    model="us.amazon.nova-lite-v1:0",
    temperature=1,
    top_p=1,
    additional_model_request_fields={
        "inferenceConfig": {
            "topK": 1
        }
    },
).bind_tools(tools)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant",
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

agent = create_tool_calling_agent(llm, tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

agent_executor.invoke({"input": "What is 2*2?"})
