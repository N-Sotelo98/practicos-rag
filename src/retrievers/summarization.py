from tqdm import tqdm
from openai import OpenAI
from dotenv import load_dotenv
import os

OAIclient = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def summarize_single_chunk(query, chunk):
    """
    Summarizes information in a single chunk relevant to the query using OpenAI GPT.
    
    Args:
        query (str): The question or topic of interest.
        chunk (str): The text chunk to analyze.
    
    Returns:
        str: Summary of relevant information if found, else None.
    """
    try:
        # Define the chat messages
        messages = [
            {"role": "system", "content": "You are an expert in food regulations. You will be provided with a query and a chunk of text, both in Spanish. Your task is to extract the relevant information from the chunk that directly addresses the query. It is extremely important that the information is factually correct, if possible, try to quote the original text. If there is no relevant information, respond with the special token '<irrelevant>' and nothing else."},
            {"role": "user", "content": f"Query: {query}\n\nChunk: {chunk}'"}
        ]       
        # Call the OpenAI API
        completion = OAIclient.chat.completions.create(
            model="gpt-4o",  # Use the appropriate model
            messages=messages,
            max_tokens=2000,  # Adjust as needed for summary length
            temperature=0  # Lower temperature for deterministic outputs
        )
        
        # Extract the assistant's reply
        reply = completion.choices[0].message.content.strip()
        
        # Return None if the response indicates no relevant information
        if reply.lower().replace(" ", "")=="<irrelevant>":
            return None
        return reply
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None



def summarize_multiple_chunks(query, chunks):
    """
    Summarizes relevant chunks of text based on the given query.

    Args:
        query (str): The query or topic of interest.
        chunks (list): List of text chunks to analyze.

    Returns:
        list: List of relevant summaries (str) if found, else empty list.
    """
    print(f'Query: {query}')

    # Precompute the total number of chunks
    total_chunks = len(chunks)

    # Initialize the array to store filtered chunks
    filtered_chunks = []

    for chunk in tqdm(chunks, total=total_chunks, desc="Processing chunks"):
        result = summarize_single_chunk(query, chunk)
        if result:
            print("Relevant Summary |", result)
            # Add the relevant summary to the filtered_chunks list
            filtered_chunks.append(result)

    return filtered_chunks