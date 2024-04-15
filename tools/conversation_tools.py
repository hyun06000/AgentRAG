import requests

def conversation_tool_with_search_master(prompt: str) -> str:
    """이 도구를 통해서 당신은 데이터베이스 관리자에게 문의할 수 있습니다.
    데이터베이스 관리자는 당신의 요구에 맞는 정보를 업데이트하여 데이터베이스에 채워줍니다."""
    try:
        response = requests.post(
            "http://localhost:8001/prompt",
            json={"text":f"{prompt}"}
        )
        return response.text
    except Exception as e:
        return f"오류가 발생하였습니다.\n오류 메세지: {e}"


def conversation_tool_with_article_researcher(prompt: str) -> str:
    """이 도구를 통해서 당신은 조사 전문가에게 질문할 수 있습니다.
    이 도구는 조사 전문가의 조사 내용을 반환합니다."""
    try:
        response = requests.post(
            "http://localhost:8002/prompt",
            json={"text":f"{prompt}"}
        )
        return response.text
    except Exception as e:
        return f"오류가 발생하였습니다.\n오류 메세지: {e}"


def conversation_tool_with_article_parser(prompt: str) -> str:
    """이 도구를 통해서 당신은 요약 전문가에게 질문할 수 있습니다.
    이 도구는 요약 전문가가 추출한 몇 가지 요약문을 알려줍니다."""
    try:
        response = requests.post(
            "http://localhost:8003/prompt",
            json={"text":f"{prompt}"}
        )
        return response.text
    except Exception as e:
        return f"오류가 발생하였습니다.\n오류 메세지: {e}"

