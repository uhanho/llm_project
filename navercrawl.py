import os
import sys
import urllib.request
import dotenv
from dotenv import load_dotenv
import requests
from urllib.parse import urlparse  # 한글 엔코딩
import urllib.parse
import pandas as pd
import json
from datetime import datetime

class naver:
    def __init__(self, searchingkey = None):
        load_dotenv()
        self.client_id = os.environ["NAVER_CLIENT_ID"]
        self.client_secret = os.environ["NAVER_CLIENT_SECRET"]
        self.display = 100
        self.start = 1
        self.sort = "sim"
        self.searchingkey = searchingkey
        self.blogdatalist = []
    
    def _request_api(self,start = 1, area = 'blog'):
        """ naver api를 통해 검색 결과를 가져옵니다.

        Args:
            start (int, optional): 검색 시작 위치를 설정합니다. Defaults to 1.
            area (str, optional): 어떤 종류의 api를 사용할 것인지 설정합니다. Defaults to 'blog'.

        Returns:
            JSON : 검색 결과를 json 형태로 반환합니다.
        """
        self.start = start
        if area not in ['blog','news','cafearticle','webkr']:
            return 600
        encText = urllib.parse.quote(self.searchingkey)
        url = f"https://openapi.naver.com/v1/search/{area}.json?query={encText}&display={self.display}&start={self.start}&sort={self.sort}"
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id",self.client_id)
        request.add_header("X-Naver-Client-Secret",self.client_secret)
        response = urllib.request.urlopen(request)
        response.getcode()
        readresponse = response.read()
        result = json.loads(readresponse)
        return result
    
    def _get_result_blog(self, page = 1):
        """ 블로그 검색 결과를 가져옵니다.

        Args:
            page (int, optional): 검색 시작 위치를 지정합니다. Defaults to 1.

        Returns:
            String[] : 100개씩 검색해가며 주어진 시간까지의 결과를 검색합니다. 모두 검색한 경우 결과를 반환합니다.
        """
        selected_keys = ['link', 'title', 'postdate','description'] # 결과에서 들고 올 항목입니다.
        while page <= 1000:                                         # page는 최대 값이 1000입니다.
            result = self._request_api(page, 'blog')                # 현재 페이지 기준 blog 검색 결과를 들고 옵니다.
            for item in result['items']:                            # 모든 아이템을 들고옵니다.                   
                selected_data = {key: item[key] for key in selected_keys} # 들고올 항목들만 아이템에서 들고옵니다.
                self.blogdatalist.append(selected_data)             # datalist에 추가합니다.
            page += self.display                                    # 한번에 self.display만큼 찾아오므로, 그다음 페이지를 업데이트 합니다
            if result['total'] < page:                              # 검색 결과가 부족한 경우, 지금까지 찾은 내용을 return 합니다.
                return self.blogdatalist
        return self.blogdatalist                                    # 검색 결과가 담긴 list를 반환합니다.
    
    def set_searchingkey(self, key):
        self.searchingkey = key
        return self.searchingkey
    
    def get_searchingkey(self):
        return self.searchingkey
