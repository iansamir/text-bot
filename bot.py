import openai
import os
from dotenv import load_dotenv

from embeddings.vector_search import connect_pinecone, pinecone_search

class Bot: 
    def __init__(self):
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def get_completion(self, conversation):
        
        print("Conversation:", conversation)
        
        # Get the newest message
        prompt = conversation[-1]["content"]

        # Get context from vector searching Arlin's videos
        index = connect_pinecone("workout-names")
        namespace = "tribe-transcripts"
        query = prompt
        matches = pinecone_search(index, query, namespace) 
        
        context_string = "\n".join(matches)

        context = [{"role":"assistant", "content": "CONTEXT FOUND: " + context_string}]
        
        # Create a combined message to include only recent context, and feed it to GPT-4
        arlin_seed = [{"role": "user", "content": "You are Arlin Moore, a successful YouTuber and entrepreneur mainly focused on improving people's social lives and creating high value social circles. Answer the questions with reference to the context provided from a search of your Online course (Tribe Accelerator) transcripts. Please respond very briefly, under 50 words."}]
        combined = arlin_seed + conversation + context 

        response = openai.ChatCompletion.create(
            model="gpt-4",
            max_tokens = 512,
            messages=combined
        )
        
        return response['choices'][0]['message']['content']

