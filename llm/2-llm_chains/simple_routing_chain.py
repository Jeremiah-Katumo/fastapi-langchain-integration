import os
from dotenv import load_dotenv
from langchain.chains import LLMChain, RouterChain
from langchain_core.chains.router import LLMRouterChain, RouterOutputParser, MultiRouteChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import AzureChatOpenAI

load_dotenv()


llm = AzureChatOpenAI(
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
)

# Destination chains
math_prompt = PromptTemplate.from_template("Solve this math problem: {input}")
science_prompt = PromptTemplate.from_template("Answer this science question: {input}")

math_chain = LLMChain(llm=llm, prompt=math_prompt)
science_chain = LLMChain(llm=llm, prompt=science_prompt)

destination_chains = {
    "math": math_chain,
    "science": science_chain,
}

# Router prompt
router_template = """
Route the user input to either 'math' or 'science'.

Input: {input}

Return JSON with destination and next_inputs.
"""

router_prompt = PromptTemplate.from_template(router_template)
router_chain = LLMRouterChain.from_llm(llm, router_prompt)

# Multi route chain
chain = MultiRouteChain(
    router_chain=router_chain,
    destination_chains=destination_chains,
    default_chain=science_chain,
)

print(chain.run("What is 12 * 8?"))


destinations = [
    {"destination": "math", "next_inputs": {"input": "What is 12 * 8?"}},
    {"destination": "science", "next_inputs": {"input": "What is the chemical symbol for water?"}},
]

for dest in destinations:
    result = chain.run(dest["next_inputs"]["input"])
    print(f"Destination: {dest['destination']}, Result: {result}")
    
    
destinations2 = [
    ("physics", "for questions about physics"),
    ("chemistry", "for questions about chemistry"),
    ("maths", "for questions about mathematics"),
    ("biology", "for questions about biology"),
]

router_template2 = """You are an expert at routing questions to the correct subject area.
Select the correct subject area for the following question:

{% for dest, desc in destinations %}
- {{ dest }} : {{ desc }}
{% endfor %}

Question: {{ input }}

Return the subject area as a string.
"""

router_prompt2 = PromptTemplate.from_template(router_template2, template_format="jinja2")
router_prompt2 = router_prompt2.partial(destinations=destinations2)
router_chain2 = LLMRouterChain.from_llm(llm, router_prompt2)

result2 = router_chain2.run("What is the chemical symbol for water?")
print(f"Routed to: {result2}")