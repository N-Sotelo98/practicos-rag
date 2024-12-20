from openai import OpenAI
from dotenv import load_dotenv
import os

OAIclient = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def answer_query_with_context(query, chunks):

    try:
        # Define the chat messages
        messages = [
            {"role": "system", "content": "You are an expert in food regulations. You will be provided with a query and some context, both in Spanish. Your task is faithfully answer the query -also in spanish- both with your knowledge and leveraging the provided context."},
            {"role": "user", "content": f"Query: {query}\n\nContext: {chunks}'"}
        ]       
        # Call the OpenAI API
        completion = OAIclient.chat.completions.create(
            model="gpt-3.5-turbo",  # Use the appropriate model
            messages=messages,
            max_tokens=2000,  # Adjust as needed for summary length
            temperature=0  # Lower temperature for deterministic outputs
        )
        
        # Extract the assistant's reply
        reply = completion.choices[0].message.content.strip()

        return reply
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None