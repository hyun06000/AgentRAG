from typing import List
import os
from pinecone import Pinecone


from utils.embedding import get_embedding


from dotenv import load_dotenv
load_dotenv(".env")


pc = Pinecone(
    api_key=os.environ.get("PINECONE_API_KEY")
)

def retrieval_vector_db_tool(query:str)->str:
    """이 도구는 데이터베이스를 검색합니다.
    입력된 쿼리와 의미적 유사도가 가장 높은 문장을 반환합니다."""
    try:
        index = pc.Index("autorag")

        answer = index.query(
            namespace="drink",
            vector=get_embedding(
                text = query,
                model = "text-embedding-ada-002",
            ),
            top_k=1,
            include_values=True,
            include_metadata=True,
        )["matches"][0]["metadata"]
        
        res = f"{answer}"
    except Exception as e:
        res = f"오류가 발생했습니다. 오류 메세지는 다음과 같습니다: {e}"
    
    return res

def upsert_vector_db_tool(list_of_text:str)->str:
    """이 도구는 데이터베이스에 문장들을 저장합니다. 입력되는 문장들의 형태는 반드시 다음과 같아야합니다.
    "[
        (출처_url_1, 문장_1),
        (출처_url_2, 문장_2),
        (출처_url_3, 문장_3),
        ...
    ]"
    """
    try:
        list_of_text = eval(list_of_text)
        assert isinstance(list_of_text, list) and isinstance(list_of_text[0], tuple), "입력의 형식이 맞지 않습니다."
        
        index = pc.Index("autorag")
        vectors = []
        for number, (url, maintext) in enumerate(list_of_text):
            embedding = get_embedding(
                text = maintext,
                model = "text-embedding-ada-002",
            )
            vectors.append(
                {
                    "id": f"{number}", 
                    "values": embedding,
                    "metadata": {
                        "url": url,
                        "text": maintext
                    }
                },
            )
        index.upsert(vectors=vectors, namespace="drink")
    
        res = "업로드를 성공적으로 마쳤습니다."
    
    except Exception as e:
        res = f"오류가 발생했습니다. 오류 메세지는 다음과 같습니다: {e}"
    
    return res