from langchain_community.document_loaders import PyPDFLoader

file_path = "/home/jeremy/Documents/Work/Learning/fastapi/llm/4-document_loader/sample_data/document.pdf"

loader = PyPDFLoader(file_path=file_path)

documents = loader.load()

print(documents)
print(f"Length of entire document: {len(documents)}")
print(f"Type of doc: {type(document for document in documents)}")
print(type(documents[0]))
print(documents[0])

print("\n"+"="*50+"\n")

first_doc = documents[0]
print(f"Page/Doc content length: {len(first_doc.page_content)}")
print(f"Document Keys: {list(first_doc.metadata.keys())}")

print("\n"+"="*50+"\n")

for idx, doc in enumerate(documents[:3]):
    print(f"Page {idx+1}")
    print(f"Content: {len(doc.page_content)} characters")
    print(f"Page number in metadata: {doc.metadata.get("page", "N/A")}")
    print(f"Source: {doc.metadata.get("source", "N/A")}")
    print("\n"+"="*50)
    