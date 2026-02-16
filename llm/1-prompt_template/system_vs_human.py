from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage

# Messages prompt
chat_template = ChatPromptTemplate.from_messages([
    SystemMessage(content="You are a sarcastic and witty assistance. You must roast the user and make fun of them. Always be sarcastic and witty."),
    HumanMessage(content="{user_input}"),
])

system_prompt = SystemMessagePromptTemplate.from_template("You are a helpful assistant.")
human_prompt = HumanMessagePromptTemplate.from_template("{user_input}")

messages = chat_template.format_messages(user_input="What is the weather like in Nairobi?")
print(messages)