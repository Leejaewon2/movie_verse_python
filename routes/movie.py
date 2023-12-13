import requests
import json
from bs4 import BeautifulSoup
from flask import jsonify

def get_movie():

    url = 'https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&qvt=0&query=%ED%98%84%EC%9E%AC%EC%83%81%EC%98%81%EC%98%81%ED%99%94'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    movieInfoList = soup.find('body', class_='wrap-new api_animation').find_all('div', class_='card_item') if soup.find('body', class_='wrap-new api_animation') else []

    movie_data = []

    for movieInfo in movieInfoList:
        # 영화 제목 정보 찾기
        movieTitleElement = movieInfo.find('a', class_='this_text _text')
        movieTitle = movieTitleElement.text.strip() if movieTitleElement else "-"

        # 개봉일 정보 찾기
        releaseDateElement = movieInfo.find('dl', class_='info_group type_visible').find('dt', text='개봉')
        movieReleaseDate = releaseDateElement.find_next('dd').text.strip() if releaseDateElement else "-"

        # 평점 정보 찾기
        ratingElement = movieInfo.find('dl', class_='info_group type_visible').find('span', class_='num')
        movieRating = ratingElement.text.strip() if ratingElement else "-"

        movie_data.append({
            'title': movieTitle,
            'releaseDate': movieReleaseDate,
            'score': movieRating,
        })
        print("제발 잘나와라 : ", movieReleaseDate)
        print("movieRating : ", movieRating)

    # Convert the movie data to JSON
    json_data = json.dumps(movie_data, ensure_ascii=False, indent=4)
    return json_data

def get_ott_movie():
    try:
        movie_queries = [
            'query=%EC%99%93%EC%B1%A0+%EC%98%81%ED%99%94',
            'query=%EB%84%B7%ED%94%8C%EB%A6%AD%EC%8A%A4+%EC%98%81%ED%99%94',
            'query=%ED%8B%B0%EB%B9%99+%EC%98%81%ED%99%94',
        ]

        base_url = 'https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&{movie_query}'

        # 각 플랫폼에 대한 리스트 초기화
        movie_data = []

        for movie_query in movie_queries:
            url = base_url.format(movie_query=movie_query)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
            }
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')

            main_elements = soup.find('ul', class_='list_info _panel').find_all('li', class_='info_box')

            # 각 플랫폼에 대한 리스트 초기화
            platform_movies = []

            for main_element in main_elements:
                # 영화 제목 정보 찾기
                movieTitle = main_element.find('a', class_='_text').get_text(strip=True)

                # "개봉" 정보 찾기
                movieReleaseDate = main_element.find_all('span', class_='info_txt')

                # 별점 정보 찾기
                movieRating = main_element.find('span', class_='num').get_text(strip=True)

                # 개봉일 초기화
                movieOpenDate = "-"
                if len(movieReleaseDate) >= 2:
                    movieOpenDateElement = movieReleaseDate[1].get_text(strip=True)
                    movieOpenDate = movieOpenDateElement

                # 영화 데이터를 딕셔너리로 만들어 플랫폼에 해당하는 리스트에 추가
                platform_movies.append({
                    'title': movieTitle,
                    'release_date': movieOpenDate,
                    'rating': movieRating,
                })

            # 전체 데이터에 추가
            movie_data.extend(platform_movies)

        # 순서대로 8개씩 추출하여 리스트 생성
        netflix_movies = movie_data[:8]
        watcha_movies = movie_data[8:16]
        tving_movies = movie_data[16:24]

        # 각 플랫폼의 JSON 데이터 반환
        return json.dumps({
            'netflix': netflix_movies,
            'watcha': watcha_movies,
            'tving': tving_movies,
        }, ensure_ascii=False, indent=4)

    except requests.exceptions.RequestException as e:
        return {'error': str(e)}

def get_movieApi(title_to_search, releaseDate_to_search):
    API_KEY = 'F851HE5P50Z8OBX419D3'

    # 올바른 API 엔드포인트 및 매개변수
    url = 'http://api.koreafilm.or.kr/openapi-data2/wisenut/search_api/search_json2.jsp?collection=kmdb_new2'

    req_parameters = {
        'ServiceKey': API_KEY,
        'collection': 'kmdb_new2',
        'title': title_to_search,
        'releaseDate': releaseDate_to_search,
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