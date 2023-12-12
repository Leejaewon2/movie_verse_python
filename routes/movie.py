import requests
import json
from bs4 import BeautifulSoup
from flask import jsonify
import re
def get_movie():
    url = 'https://search.daum.net/search?nil_suggest=btn&w=tot&DA=SBC&q=%EC%98%81%ED%99%94%EC%88%9C%EC%9C%84'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }

    response = requests.get(url, headers=headers)  # headers were missing in your GET request
    soup = BeautifulSoup(response.text, 'html.parser')
    movieInfoList = soup.find('ol', attrs={'class': 'movie_list'}).find_all('li') if soup.find('ol', attrs={
        'class': 'movie_list'}) else []

    movie_data = []
    release_date = "-"

    for movieInfo in movieInfoList:

        movieRank = movieInfo.find('span', attrs={'class': 'img_number'})
        movieTitle = movieInfo.find('a', attrs={'class': 'tit_main'})
        movieScore = movieInfo.find('em', attrs={'class': 'rate'})
        movieOpenDate = movieInfo.find('dd', class_='cont')

        movie_data.append({
            'rank': movieRank.get_text() if movieRank else "-",
            'title': movieTitle.get_text().strip() if movieTitle else "-",
            'score': movieScore.get_text() if movieScore else "-",
            'releaseDate': movieOpenDate
        })

        top_10_movies = movie_data[:10]
        print("제발 잘나와라 : ", release_date)

    # Convert the movie data to JSON
    json_data = json.dumps(top_10_movies, ensure_ascii=False, indent=4)
    return json_data

def get_ott_movie():
    try:
        url = 'https://movie.daum.net/ranking/ott'

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
        }

        response = requests.get(url, headers=headers)  # headers were missing in your GET request
        soup = BeautifulSoup(response.text, 'html.parser')
        # 특정 클래스를 가진 모든 ol 태그를 찾음
        ol_elements = soup.find_all('ol', class_='list_movieranking aniposter_ott') if soup.find('ol', attrs={
            'list_movieranking aniposter_ott'}) else []

        # 모든 영화 정보를 담을 리스트 초기화
        movie_data = []

        for ol_element in ol_elements:
            movieInfoList = ol_element.find_all('li')

            for movieInfo in movieInfoList:
                movieTitle = movieInfo.find('a', class_='link_txt')
                movieRank = movieInfo.find('span', class_='rank_num')
                movieScore = movieInfo.find('span', class_='info_grade')

                # 영화 정보를 딕셔너리에 추가
                movie_data.append({
                    'rank': movieRank.get_text() if movieRank else "-",
                    'title': movieTitle.get_text().strip() if movieTitle else "-",
                    'score': movieScore.get_text() if movieScore else "-",
                })

                # 전체 영화 리스트에 추가

        # 순서대로 10개씩 추출하여 리스트 생성
        tving_movies = movie_data[:10]
        watcha_movies = movie_data[10:20]
        wavve_movies = movie_data[20:30]

        # 각 플랫폼의 JSON 데이터 반환
        return json.dumps({
            'tving': tving_movies,
            'watcha': watcha_movies,
            'wavve': wavve_movies
        }, ensure_ascii=False)
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}

print(get_ott_movie())


def get_movieApi(title_to_search):
    API_KEY = 'F851HE5P50Z8OBX419D3'

    # 올바른 API 엔드포인트 및 매개변수
    url = 'http://api.koreafilm.or.kr/openapi-data2/wisenut/search_api/search_json2.jsp?collection=kmdb_new2'

    req_parameters = {
        'ServiceKey': API_KEY,
        'collection': 'kmdb_new2',
        'title': title_to_search,
    }

    # 요청 및 응답
    try:
        r = requests.get(url, params=req_parameters)
        r.raise_for_status()  # 4xx 또는 5xx 응답에 대한 HTTPError 발생
        dict_data = r.json()
        return dict_data  # 정상적인 JSON 데이터 반환
    except requests.exceptions.RequestException as e:
        print(f"요청 중 오류가 발생했습니다: {e}")
        return {"error": str(e)}

if __name__ == '__main__':
    result = get_movieApi("영화 제목")
    print(jsonify(result))