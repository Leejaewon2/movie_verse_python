import requests
import json
from flask import Flask
from datetime import date, timedelta
from env import settings

app2 = Flask(__name__)


def get_movie_api():
    API_KEY = settings.KMDB_API['key']
    # 오늘 기준 -30일 전 개봉
    recall_release_date = date.today() - timedelta(60)
    release_date = recall_release_date.strftime('%Y%m%d')
    releaseDte = date.today().strftime('%Y%m%d')


    # 올바른 API 엔드포인트 및 매개변수
    url = 'http://api.koreafilm.or.kr/openapi-data2/wisenut/search_api/search_json2.jsp?'

    req_parameters = {
        'ServiceKey': API_KEY,
        'collection': 'kmdb_new2',
        'releaseDts': release_date,
        'releaseDte': releaseDte,
        'listCount':'80',
    }

    # 요청 및 응답
    try:
        response = requests.get(url, params=req_parameters)
        response.raise_for_status()
        dict_data = response.json()
        return dict_data
    except requests.exceptions.RequestException as e:
        return {"error": f"요청 중 오류가 발생했습니다: {e}"}


if __name__ == '__main__':
    result = get_movie_api()
    print(json.dumps(result, indent=2, ensure_ascii=False))



