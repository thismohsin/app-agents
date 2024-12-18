#python -m pip install pyautogen

import autogen

config_list = [{
        "model": "llama3.2:1b",
        "api_key": "fake-key",
        "base_url": "http://localhost:11434/v1",
        "temperature": 0.4
    }]

def get_weather_forecast(city: str) -> str:
    """
    Retrieves the weather forecast for a given city using a weather API.
    
    Args:
        city (str): Name of the city to get weather for
    
    Returns:
        str: Formatted weather forecast information
    """
    temp = '10'
    description = 'cold'
    humidity = 'windy'
    forecast = (f"Weather in {city}: {description}. "
                f"Temperature: {temp}°C, "
                f"Humidity: {humidity}%")
    return forecast

# Create the AutoGen agents
weather_agent = autogen.AssistantAgent(
    name="WeatherAgent",
    description="A helpful weather assistant that provides detailed and accurate weather forecasts.",
    llm_config={
        "config_list": config_list,
        "temperature": 0.4,
    }
)

user_proxy = autogen.UserProxyAgent(
    name="UserProxy",
    human_input_mode="ALWAYS",  # Changed to ALWAYS for more control
    max_consecutive_auto_reply=1,
    code_execution_config={"use_docker": False},
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE")
)

# Register the weather forecast function
user_proxy.register_function(
    function_map={
        "get_weather_forecast": get_weather_forecast
    }
)

# Initiate the conversation
def main():
    try:
        # Start the conversation
        result = user_proxy.initiate_chat(
            weather_agent, 
            message="Can you help me get the weather forecast for Paris?"
        )
        
        # Print the final summary
        print("\nChat Summary:")
        print(result.summary)
    
    except Exception as e:
        print(f"An error occurred during the chat: {e}")

# Run the main function
if __name__ == "__main__":
    main()



# from autogen import AssistantAgent, UserProxyAgent

# config_list = [{
#         "model": "llama3.2:1b",
#         "api_key": "fake-key",
#         "base_url": "http://localhost:11434/v1",
#         "temperature": 0.4
#     }]


# weather_agent = AssistantAgent(
#     name="WeatherAgent",
#     description="""A weather assistant that summarizes and provides helpful
#     details, customized for the user's query.""",
#     llm_config={
#         "config_list": config_list,
#     }
# )


# user_proxy = UserProxyAgent(
#     name="UserProxy",
#     human_input_mode="NEVER",
#     code_execution_config={"use_docker": False},
#     is_termination_msg=lambda x: x.get("content", "")
#     and x.get("content", "").rstrip().endswith("TERMINATE"),
# )

# @user_proxy.register_for_execution()
# @weather_agent.register_for_llm(
#     description="Retrieves the weather forecast for a given city."
# )
# def get_weather_forecast(city: str) -> str:
#     """Retrieves the weather forecast for a given city."""
#     print(f"Retrieving weather forecast for {city}...")
#     return "foggy and cold weather fprcast for {city}"

# result = user_proxy.initiate_chat(
#         weather_agent, message="What's the weather like in Paris?"
#     )

# print(result.summary)
