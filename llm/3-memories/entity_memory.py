import os
from dotenv import load_dotenv
from langchain.memory import ConversationEntityMemory
from langchain.chains import ConversationChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import AzureChatOpenAI

load_dotenv()

llm = AzureChatOpenAI(
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    temperature=0.7,
)

print("---- First Conversation: Entity Memory Demo ----")
print("\nTracks entities (places, people, facts, and events) mentioned in the conversation.")
print("\n"+"="*50+"\n")

entity_memory = ConversationEntityMemory(llm=llm, k=5)

entity_propmt = PromptTemplate.from_template(
    input_variables=["history", "entities", "input"],
    template=
    """
    What are the entities mentioned in the following conversation? 
    
    History: {history}
    
    Entities: {entities}
    
    Human: {input}
    
    AI:
    """
)

conversation_chain = ConversationChain(
    llm=llm,
    memory=entity_memory,
    prompt=entity_propmt
)

print("First Response:\n")
response1 = [conversation_chain.run(input="Hello, my name is Jeremy.")]
print(response1)

print("\nSecond Response:\n")
response2 = conversation_chain.run(input="I am from Seattle, and I have a dog named Max.")
print(response2)

print("\nThird Response:\n")
response3 = conversation_chain.run(input="I work at Microsoft and I graduated from the University of Washington.")
print(response3)

print("\nFourth Response:\n")
response4 = conversation_chain.run(input="What is my name, where am I from and what do I work at?")
print(response4)

print("\n"+"="*50+"\n")
print("Chat History:\n")
print(entity_memory.buffer)
print("\n"+"="*50+"\n")


test_input = "What are the entities mentioned in our conversation so far?"
try:
    memory_variables = entity_memory.load_memory_variables(test_input)
    print("Memory Variables:\n")
    print("History:", memory_variables.get("history", "No history found"))
    print("Entities:", memory_variables.get("entities", "No entities found"))
    print(memory_variables)
except Exception as e:
    print(f"Error loading memory variables: {e}")
    
    
print("\n"+"="*50+"\n")
print("Testing entity extraction with a new question:\n")
response5 = conversation_chain.run(input="Can you list the entities mentioned in our conversation?")
print(response5)


if hasattr(entity_memory, "entities"):
    print("Entity store type:", type(entity_memory.entities))
    
    if hasattr(entity_memory.entity_store, "store"):
        store_dict = entity_memory.entity_store.store
        
        if store_dict:
            print("\nEntities in store:")
            for entity, details in store_dict.items():
                print(f"Entity: {entity}, Details: {details}")
        else: 
            print("No entities found in the store.")
    else:
        print("The entity store does not have a 'store' attribute.")
else:    
    print("The entity memory does not have an 'entities' attribute.")
    

print("\n"+"="*50+"\n")
print("Testing entity memory with a new question about the entities:\n")
if hasattr(entity_memory, "buffer"):
    print("Current entity memory buffer:", entity_memory.buffer)
else:
    print("The entity memory does not have a 'buffer' attribute.")
