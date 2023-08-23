import openai
import pinecone
import os

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

def connect_pinecone(index_name):
    # Set up OpenAI
    openai.api_key = os.getenv("OPENAI_API_KEY")
    
    # Set up Pinecone
    pinecone_api_key = os.getenv("PINECONE_API_KEY")
    pinecone_env = 'us-east4-gcp'
    pinecone.init(api_key=pinecone_api_key, environment=pinecone_env)

    # Connect to the Pinecone index
    return pinecone.Index(index_name)

def pinecone_search(index, query, namespace, top_k=3):
    # Create the query embedding
    xq = openai.Embedding.create(input=query, engine='text-embedding-ada-002')['data'][0]['embedding']
    
    # Query the index
    res = index.query([xq], top_k=top_k, namespace=namespace, include_metadata=True)
    query_matches = res['matches']

    # Store the metadata text in a list and print matches
    CYAN_CODE = '\033[96m'
    END_CODE = '\033[0m'
    print("query: " + CYAN_CODE + query + END_CODE)
    
    metadata_text_list = []
    for match in query_matches:
        print(f"{match['score']:.2f}: {match['metadata']['text']}")
        metadata_text_list.append(match['metadata']['text'])
    
    return metadata_text_list
