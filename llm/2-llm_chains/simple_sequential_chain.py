import os
from dotenv import load_dotenv
from langchain.chains import SimpleSequentialChain, LLMChain
from langchain_core.prompts import PromptTemplate 
from langchain_openai import AzureChatOpenAI

load_dotenv()

llm = AzureChatOpenAI(
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
)

name_chain = LLMChain(llm=llm, prompt=PromptTemplate.from_template(
    "What is good name for a company that makes {product}?"
))

catchphrase_chain = LLMChain(llm=llm, prompt=PromptTemplate.from_template(
    "Write a short, catchy slogan or catchphrase for a company named {company_name}?"
))

overall_chain = SimpleSequentialChain(
    chains=[name_chain, catchphrase_chain], 
    input_variables=["product"],
    output_variables=["company_name", "catchphrase"],
    verbose=True
)

final_result = overall_chain.run(product="user friendly housing software for real estate agents, landlords, and tenants")
print(final_result)