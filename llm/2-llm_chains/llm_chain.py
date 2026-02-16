import os
from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate 
from langchain_openai import AzureChatOpenAI


load_dotenv()

llm = AzureChatOpenAI(
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
)

prompt = PromptTemplate.from_template(
    "What is good name for a company that makes {product}"
)

chain = LLMChain(llm=llm, prompt=prompt)

result = chain.run(product="colorful socks")
print(result)
