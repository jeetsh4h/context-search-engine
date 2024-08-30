from pydoc import doc
import chromadb
import time

# TODO: add a global client that lives throughout the
#       lifetime of the application
# connect in the main loop and then pass it around in functions

MAX_CHUNK_SIZE = 256


# TODO: build a on-disk index that enusres things are not being
#       added to the database multiple times
#       pass documents, metadatas and file_names as a generator,
#       this will avoid storing all the PDF texts in memory if there 
#       are multiple of them.
def add_documents(documents:list[str], metadatas:dict[str,str] = None, file_names=list[str]):
    """
    Creates vector embeddings of a set of documents and adds these to the vector database
    
    Parameters:
    - documents (list[str]): The split list of documents to be vectorized. Each chunk is a string, in the form of a paragraph from a page.
    - max_size (int, optional): The maximum number of words per chunk. 
                                Defaults to MAX_CHUNK_SIZE.
    - file_names
                                
    Yields:
    - None
    
    Example:
    >>> add_document(["This is a sample document", "with more than eight words."])
    """
    
    if (len(documents) != len(list(file_names))):
        print("length of documents and file_names should be same")
        return
    
    client = chromadb.PersistentClient(".")
    
    collection = client.get_or_create_collection("court_documents")
    collection.add(documents=documents, metadatas=metadatas, ids=file_names)

    print("Documents added to collection")


# TODO: Add function to support showing multiple results
def query_documents(query:str, n_results=1):
    """
    Search for the most relevant chunk in the vector datavase based on a query.
    
    Parameters:
    - query (str): The query string for which a matching chunk is to be found.
    - num_matches (int, optional): The number of matches to retrieve. 
                                   Defaults to 1.
                                   
    Returns:
    - str: The matched paragraph.
    
    Example:
    >>> result = query_documents("Introduction to AI")
    >>> print(result['documents'][0])
    ... # Output: Most Relevant chunk from indexed documents.
    """
    
    client = chromadb.PersistentClient(".")
    collection = client.get_or_create_collection("court_documents")
    result = collection.query(query_texts=query, n_results= n_results)
    
    return result