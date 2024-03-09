import os
from openai import OpenAI # for generating embeddings
import tiktoken  # for counting tokens
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(
  api_key="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",  # this is also the default, it can be omitted
)
# Set GPT model
GPT_MODEL = os.environ.get("GPT_MODEL", "gpt-4-1106-preview")

def num_tokens(text: str, model: str = GPT_MODEL) -> int:
    """Return the number of tokens in a string."""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))


async def query_message(
    query: str,
    model: str,
    token_budget: int
) -> str:
    try:
        """Return a message for GPT, with relevant source texts pulled from a dataframe."""
        introduction = 'Below are the sections to a document provided by the user. Use the below sections to answer the subsequent question or respond to prompt. If the answer cannot be found in the articles, write "I could not find an answer."'
        question = f"\n\nQuestion or Prompt: Based on the text provided, {query}"
        message = introduction
        for string in strings["related_strings"]:
            next_article = f'\n\nSection:\n"""\n{string}\n"""'
            if (
                num_tokens(message + next_article + question, model=model)
                > token_budget
            ):
                break
            else:
                message += next_article
        return message + question
    except Exception as e:
        print(e)
        return "Error"
    
    


async def ask(
    query: str,
    model: str = GPT_MODEL,
    token_budget: int = 100000,
    print_message: bool = False,
) -> str:
    try:
        """Answers a query using GPT and a dataframe of relevant texts and embeddings."""
        messages = [
            {"role": "system", "content": "You answer the questions or respond to prompts in context of sections below."},
            {"role": "user", "content": query},
        ]
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0
        )
        response_message = response.choices[0].message.content
        return response_message
    except Exception as e:
        print(e)
        return "Error"
    