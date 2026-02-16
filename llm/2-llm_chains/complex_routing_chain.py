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
    
    
destinations = [
    ("physics", "for questions about physics"),
    ("chemistry", "for questions about chemistry"),
    ("maths", "for questions about mathematics"),
    ("biology", "for questions about biology"),
]

router_template = """
You are an expert at routing questions to the correct subject area.

Available subject areas are:
- physics: {physics_desc}
- chemistry: {chemistry_desc}
- maths: {maths_desc}
- biology: {biology_desc}

Analyze the following question and determine which subject area it belongs to.
Return the subject area as a single word (physics, chemistry, maths, or biology) - no other text.

Question: {input}

Subject area: 
"""

router_prompt = PromptTemplate(
    template=router_template,
    input_variables=["input"],
    partial_variables={
        "physics_desc": destinations[0][1],
        "chemistry_desc": destinations[1][1],
        "maths_desc": destinations[2][1],
        "biology_desc": destinations[3][1],
    }
)

physics_template = """
You are physics expert. Answer the following physics question with clear, accurate and concise physics knowledge.

Question: {input}

Physics answer:
"""
physics_prompt = PromptTemplate.from_template(physics_template)
physics_chain = LLMChain(llm=llm, prompt=physics_prompt)

chemistry_template = """
You are chemistry expert. Answer the following chemistry question with clear, accurate and concise chemistry knowledge.

Question: {input}

Chemistry answer:
"""
chemistry_prompt = PromptTemplate.from_template(chemistry_template)
chemistry_chain = LLMChain(llm=llm, prompt=chemistry_prompt)

maths_template = """
You are mathematics expert. Answer the following mathematics question with clear, accurate and concise mathematics knowledge.

Question: {input}

Mathematics answer:
"""
maths_prompt = PromptTemplate.from_template(maths_template)
maths_chain = LLMChain(llm=llm, prompt=maths_prompt)

biology_template = """
You are biology expert. Answer the following biology question with clear, accurate and concise biology knowledge.

Question: {input}

Biology answer:
"""
biology_prompt = PromptTemplate.from_template(biology_template)
biology_chain = LLMChain(llm=llm, prompt=biology_prompt)

destination_chains = {
    "physics": physics_chain,
    "chemistry": chemistry_chain,
    "maths": maths_chain,
    "biology": biology_chain,
}

router_chain = LLMRouterChain.from_llm(llm, router_prompt, destination_chains=destination_chains)


def custom_router_output_parser(output: str) -> RouterOutputParser:
    output = output.strip().lower()
    if output in destination_chains:
        return RouterOutputParser(destination=output, next_inputs={"input": input})
    else:
        return RouterOutputParser(destination="physics", next_inputs={"input": input})
    
def custom_router_chain(input: str) -> RouterOutputParser:
    router_output = router_chain.run(input)
    return custom_router_output_parser(router_output)

def smart_router(question: str):
    router_chain = LLMChain(llm=llm, prompt=router_prompt)
    
    response = router_chain.invoke({"input": question})
    destination = response.strip().lower()
    
    print(f"Routed to: {destination}")
    
    # if destination in destination_chains:
    #     return destination_chains[destination].run(question)
    if "physics" in destination:
        return "physics", physics_chain.invoke({"input": question})
    elif "chemistry" in destination:
        return "chemistry", chemistry_chain.invoke({"input": question})
    elif "maths" in destination:
        return "maths", maths_chain.invoke({"input": question})
    elif "biology" in destination:
        return "biology", biology_chain.invoke({"input": question})
    else:
        fallback_response = """
        Sorry, I couldn't determine the subject area. Questions can be about physics, chemistry, mathematics, or biology.
        
        Question: {question}
        SUbject: 
        Here's a general answer: """
        fallback_chain = LLMChain(llm=llm, prompt=PromptTemplate.from_template(fallback_response))
        fallback_result = fallback_chain.invoke({"question": question})
        final_destination = fallback_result["text"].strip().lower()
        
        if "physics" in final_destination:
            return "physics", physics_chain.invoke({"input": question})
        elif "chemistry" in final_destination:
            return "chemistry", chemistry_chain.invoke({"input": question})
        elif "maths" in final_destination:
            return "maths", maths_chain.invoke({"input": question})
        elif "biology" in final_destination:
            return "biology", biology_chain.invoke({"input": question})
        else:
            return "Sorry, I couldn't determine the subject area for your question.", physics_chain.invoke({"input": question})
        
def test_router():
    questions = [
        "What is the chemical symbol for water?",
        "What is the formula for calculating the area of a circle?",
        "What is the process of photosynthesis?",
        "What is Newton's second law of motion?"
    ]
    
    for i, question in enumerate(questions):
        destination, answer = smart_router(question)
        print(f"Router decides: {destination}")
        
        if destination in destination_chains:
            result = destination_chains[destination].invoke({"input": question})
            print(f"Answer: {result['text'][:200]}...\n") # Print only the first 200 characters of the answer for brevity
        else:
            print("No valid destination found for the question.\n")
            result = physics_chain.invoke({"input": question})
            print(f"Fallback answer: {result['text'][:200]}...\n") # Print only the first 200 characters of the fallback answer for brevity
            
        print("-" * 50)
        
def test_connection():
    """Test Azure OpenAI connection and router chain."""
    try:
        test_prompt = PromptTemplate.from_template("Say, Connection successful!")
        text_chain = LLMChain(llm=llm, prompt=test_prompt)

        result = text_chain.invoke({"input": "test connection"})
        print(f"Connection test result: {result['text']}")
    except Exception as e:
        print(f"Error testing connection: {e}")
        return False
    
if __name__ == "__main__":
    if test_connection():
        test_router()
        
        print("Testing individual questions:")
        
        questions = [
            "What is mitochondria?",
            "What is the formula for calculating the area of a circle?",
            "What is the process of photosynthesis?",
            "What is Newton's second law of motion?"
        ]
        
        for question in questions:
            destination, answer = smart_router(question)
            print(f"Question: {question}")
            print(f"Routed to: {destination}")
            print(f"Answer: {answer['text'][:200]}...\n") # Print only the first 200 characters of the answer for brevity
            print("-" * 50)

result = router_chain.run("What is the chemical symbol for water?")
print(f"Routed to: {result}")