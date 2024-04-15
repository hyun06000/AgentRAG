import io
import re
import requests


from bs4 import BeautifulSoup
from PyPDF2 import PdfReader


def request_tool(url: str) -> str:
    """이 도구는 입력된 url의 응답을 돌려줍니다. 입력은 반드시 http로 시작하는 하나의 구문이어야합니다."""

    try:
        response = requests.get(url, verify=False)
        if url.endswith(".pdf"):
            text = ""
            with io.BytesIO(response.content) as f:
                pdf = PdfReader(f)
                for page_num in range(len(pdf.pages)):
                    text += pdf.pages[page_num].extract_text() + '\n'
        else:
            soup = BeautifulSoup(response.text, "html.parser")
            text = soup.body.get_text().strip().encode('utf8','replace').decode()
        text = re.sub(r"\n", " ", text)
        text = re.sub(r"\s+", " ", text)
    except Exception as e:
        text = f"오류가 발생했습니다: {e}"

    return text