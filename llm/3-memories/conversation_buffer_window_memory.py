import os
from dotenv import load_dotenv
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import AzureChatOpenAI

load_dotenv()

llm = AzureChatOpenAI(
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
)

memory = ConversationBufferWindowMemory(k=2, return_messages=True)  # only keep the last 2 interactions in memory, and return them as messages (instead of a formatted string)

conversation = ConversationChain(
    llm=llm,
    memory=memory,
    prompt=PromptTemplate.from_template(
        """
        The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific 
        details from its context. If the AI does not know the answer to a question, it truthfully says it does not know. 
        
        The conversation history is as follows: {history}. 
        
        Human: {input} 
        
        AI:
        """
    )
)


print("First Response:\n")
response1 = conversation.predict(input="What year did the first man land on the moon?")
print(response1)

print("\nSecond Response:\n")
response2 = conversation.predict(input="Hello, I am John.")
print(response2)

print("\nThird Response:\n")
response3 = conversation.predict(input="What is my name?")
print(response3)

print("\n"+"="*40+"\n")
print("Chat History:\n")
print(memory.buffer)
print("\n"+"="*40+"\n")
print(memory.load_memory_variables({}))  # dictionary format of memory variables, in this case just the chat history