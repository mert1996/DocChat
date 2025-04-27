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

    # Yeni prompt metni:
    prompt = f"""
    Aşağıda, kullanıcı sorusuyla ilgili olabileceğini düşündüğümüz en fazla üç (3) adet referans bilgi bulunmaktadır. 
    Bu metinler, kullanıcının sorusuna yanıt vermek için kullanabileceğin başlıca kaynaklardır.

    Kurallar:
    1. Cevabında YALNIZCA bu referans metinlerde yer alan bilgilere dayan.
    2. Referans metinlerdeki bilgileri özetlemen gerekiyorsa özetleyebilirsin, ancak doğruluk payından emin ol.
    3. Referans metinlerde olmayan hiçbir bilgiyi ekleme veya varsayımda bulunma.
    4. Referans metinlerde soruyu karşılayacak yeterli bilgi yoksa, bu bilgilerin yetersiz olduğunu belirt.
    5. Cevabı, kullanıcının sorduğu dilde veya uygun gördüğün dilde tutarlı şekilde oluştur.
    
    Referans Alınacaklar:
    1)
    Döküman adı: {context_texts[0]["docName"]}
    Döküman içeriği: {context_texts[0]["content"] if len(context_texts) > 0 else "—"}
    
    2)
    Döküman adı: {context_texts[1]["docName"]}
    Döküman içeriği:  {context_texts[1]["content"] if len(context_texts) > 1 else "—"}
    
    3)
    Döküman adı: {context_texts[2]["docName"]}
    Döküman içeriği: {context_texts[2]["content"] if len(context_texts) > 2 else "—"}

    Kullanıcının Sorduğu Soru: {user_query}

    Şimdi lütfen, yukarıdaki kurallara ve referans metinlere sadık kalarak nihai cevabını ver. Verdiğin cevaplarda 
    samimi bir dil kullan. Her zaman kibar ol ve kullanıcının sorusunu mümkün olduğunca doğru ve net bir şekilde 
    yanıtla.
    """

    # print(prompt)
    response = openai.ChatCompletion.create(
        model=GPT_MODEL_NAME,
        messages=[
            {"role": "system", "content": "Sen bir yapay zeka asistanısın. Kullanıcı sorularını mümkün olduğunca doğru ve net cevaplamalısın."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=500
    )

    answer = response["choices"][0]["message"]["content"].strip()
    return answer

