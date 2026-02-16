import os 
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize the chat model (llm)
llm = ChatOpenAI(
    model="gpt-3.5-turbo", 
    temperature=0.9, 
    api_key=API_KEY
)

# prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that translates {input_language} to {output_language}."),
    ("human", "Translate the following English text to French: {text}")
])

# Create the chain by combining the prompt and the llm
chain = prompt | llm

# Run the chain with input variables
response = chain.invoke({
    "input_language": "English",
    "output_language": "French",
    "text": "Hello, how are you?"
})

print("Full response:", response)
print("Translated text:", response.text)