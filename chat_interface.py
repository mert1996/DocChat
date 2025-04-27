import openai
from config import OPENAI_API_KEY, GPT_MODEL_NAME
from client.weaviate_client import WeaviateExecuter

openai.api_key = OPENAI_API_KEY


def generate_answer(user_query):
    results = WeaviateExecuter().semantic_search(user_query, top_k=3)

    context_texts = []
    for r in results:
        content = r.get("content", "")
        document_name = r.get("docName", "")
        context_texts.append({
            "content": content,
            "docName": document_name
        })

    prompt = f"""

        Below are up to three (3) reference pieces of information that may be relevant to the user's question.
        These texts are the primary sources you should use to generate your answer.

        Rules:
        1. Base your answer ONLY on the information contained in these reference texts.
        2. If necessary, you can summarize the reference texts, but ensure the accuracy of the information.
        3. Do not add any information or make assumptions beyond what is included in the references.
        4. If the references do not provide sufficient information to answer the question, clearly state that the information is insufficient.
        5. Formulate your answer consistently in the language of the user's question or in a language you deem appropriate.

        References:
        1)
        Document name: {context_texts[0]["docName"]}
        Document content: {context_texts[0]["content"] if len(context_texts) > 0 else "—"}

        2)
        Document name: {context_texts[1]["docName"]}
        Document content: {context_texts[1]["content"] if len(context_texts) > 1 else "—"}

        3)
        Document name: {context_texts[2]["docName"]}
        Document content: {context_texts[2]["content"] if len(context_texts) > 2 else "—"}

        User's Question: {user_query}

        Now, please generate your final answer strictly based on the above rules and references. 
        Use a friendly and polite tone in your response. Always aim to answer the user's question as accurately and clearly as possible.
        """

    # print(prompt)
    response = openai.ChatCompletion.create(
        model=GPT_MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are an AI assistant. You must answer user questions as accurately and clearly as possible."},

            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=500
    )

    answer = response["choices"][0]["message"]["content"].strip()
    return answer

