import os
from dotenv import load_dotenv
from langchain.memory import ConversationSummaryMemory
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

memory = ConversationSummaryMemory(
    llm=llm,
    input_key="input",
    output_key="output",
    memory_variables=["history", "summary"],
    prompt=PromptTemplate.from_template(
        """
        Write a concise summary of the following conversation between a human and an AI. The summary should capture the key points 
        and important details of the conversation, but should be concise and to the point. If the conversation is short, 
        the summary should be the same as the conversation. 
        
        Conversation: {history} 
        
        Summary:
        """
    )
)

conversation_chain = ConversationChain(
    llm=llm,
    memory=memory,
    prompt=PromptTemplate.from_template(
        """
        The following is a friendly conversation between a human and an AI. The AI is helpful and provides lots of specific details from its context. 
        If the AI does not know the answer to a question, it truthfully says it does not know. 
        
        The conversation history is as follows: {history}. The summary of the conversation so far is: {summary}.
        Human: {input}
        AI:
        """
    )
)


conversation_chain.predict(input="I love Data Science and Software Engineering. I am currently learning about LLMs and LangChain.")
conversation_chain.predict(input="I am interested in Generative AI")
conversation_chain.predict(input="I am eager to learn LangGraph after completing my learning of LangChain.")
conversation_chain.predict(input="I want to combine my knowledge of Data Science, Software Engineering, LLMs, LangChain, and LangGraph to build amazing applications that can help people solve real world problems.")
conversation_chain.predict(input="What is the summary of our conversation so far?")

print("\n"+"="*40+"\n")
print("Chat History:\n")
print(memory.buffer)
print("\n"+"="*40+"\n")
print(memory.load_memory_variables({}))  # dictionary format of memory variables, in this case the chat history and the conversation summary
