from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    UnstructuredWordDocumentLoader,
    CSVLoader
)

def multiple_loaders():
    loaders_info = [
        {
            'name': 'pdf loader',
            'loader': PyPDFLoader,
            'file': '/home/jeremy/Documents/Work/Learning/fastapi/llm/4-document_loader/sample_data/document.pdf',
            'description': 'Research papers, reports or any pdf',
        },
        {
            'name': 'text loader',
            'loader': TextLoader,
            'file': '/home/jeremy/Documents/Work/Learning/fastapi/llm/4-document_loader/sample_data/shopping_behavior_updated.txt',
            'description': 'Text files (.txt)',
        },
        {
            'name': 'csv loader',
            'loader': CSVLoader,
            'file': '/home/jeremy/Documents/Work/Learning/fastapi/llm/4-document_loader/sample_data/shopping_behavior_updated.csv',
            'description': 'Csv files (.csv)',
        }
    ]
    
    all_documents = []
    
    for loader_info in loaders_info:
        print(f"\nProcessing with: {loader_info['name']}")
        print(f"\nFile: {loader_info['file']}")
        print(f"\nUse case: {loader_info['description']}")
        
        try:
            loader = loader_info['loader'](loader_info['file'])
            docs = loader.load()
            print(f"Loaded {len(docs)} documents")
            
            if docs:
                sample_content = docs[0].page_content[:150]+"..." if len(docs[0].page_content) > 150 else docs[0].page_content
                print(f"Sample: {sample_content}")
                
            all_documents.extend(docs)
            
        except FileNotFoundError as e:
            print(f"Error: File not found - {e}")
        except ValueError as e:
            print(f"Error: Invalid value - {e}")
            
    print(f"\n Total: {len(all_documents)} documents load from multiple file types")
    return all_documents


documents = multiple_loaders()