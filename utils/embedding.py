import os


from openai import OpenAI


from dotenv import load_dotenv
load_dotenv(".env")


client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def get_embedding(text, model="text-embedding-ada-002"):
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding