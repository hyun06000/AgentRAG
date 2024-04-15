import os
from serpapi import GoogleSearch, NaverSearch

from dotenv import load_dotenv
load_dotenv(".env")

def search_google_tool(query: str) -> str:
    """google search tool to get url related to the keywords"""
    params = {
        "q": query,
        "num": 5,
        "api_key": os.environ["SERPAPI_API_KEY"],
        "google_domain": "google.co.kr",
    }

    try:
        search = GoogleSearch(params)
        search_dict = search.get_dict()
        
        if "organic_results" not in search_dict:
            return "There is no result. Please change the search phrase to a more shorter and generic words."
        
        res = list(map(
            lambda x: f"TITLE: {x['title']} | LINK: {x['link']} | DESCRIPTION: {x['snippet']}",
            search.get_dict()["organic_results"]
        ))
    except Exception as e:
        res = str(e)
    
    return res


def search_naver_tool(query: str) -> str:
    """이 도구는 한국어에 특화된 검색엔진인 네이버를 이용하여 정보를 검색합니다."""
    params = {
        "engine": "naver",
        "query": f"{query}",
        "where": "web",
        "device": "mobile",
        "api_key": os.environ["SERPAPI_API_KEY"]
    }

    try:
        search = NaverSearch(params)
        search_dict = search.get_dict()
        if "organic_results" not in search_dict:
            return "검색 결과가 없습니다. 다른 키워드로 다시 검색하세요."
        
        res = str(list(map(
            lambda x: f"TITLE: {x['title']} | LINK: {x['link']}",
            search_dict["organic_results"]
        )))
    
    except Exception as e:
        res = str(e)
    
    return res
