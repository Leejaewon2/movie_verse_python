import requests
import json
from bs4 import BeautifulSoup
from flask import jsonify

# 영화 전체 개봉일 + 감독 정보 가져오기
def get_release_date(href,title, max_retries = 3):
    retries = 0
    while retries < max_retries:
        try:
            url = 'https://search.naver.com/search.naver' + href
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raises HTTPError for bad responses

            soup = BeautifulSoup(response.text, 'html.parser')
            main_el = soup.find('body', class_='wrap-new api_animation').find('dl', class_='info')
            outer_els = main_el.find_all('div', class_='info_group')

            open_date = ''
            if len(outer_els) >= 2:
                release_date_el = outer_els[1].find('dt')
                release_date = release_date_el.find_next('dd').text.strip() if release_date_el else "-"
                open_date = release_date.replace('.', '')

            director_outer = soup.find('div', class_='middle_title').find_next('div').find('div', class_='area_card')
            director = director_outer.find('strong', class_='name').find('a',
                                                                         class_='_text').text.strip() if director_outer else ""

            result = {"open_date": open_date, "director": director}
            return result

        except requests.exceptions.RequestException as e:
            print(f'Error: {str(e)} - Retry {retries + 1}/{max_retries}')
            retries += 1

    return {'error': 'Max retries reached'}

# 현재 상영작
def get_box_office() :
    try :
        url = 'https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&qvt=0&query=현재상영영화'

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
        }

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        movie_ls = soup.find('body', class_='wrap-new api_animation').find_all('div', class_='card_item') if soup.find('body', class_='wrap-new api_animation') else []

        box_office = []

        for movie in movie_ls:
            # 영화 제목 정보 찾기
            title_el = movie.find('a', class_='this_text _text')
            title = title_el.text.strip() if title_el else "-"

            # 개봉일 정보 찾기 (text="개봉" => string="개봉") text 더이상 지원하지 않음
            # release_date_el = movie.find('dl', class_='info_group type_visible').find('dt', string='개봉')
            # release_date = release_date_el.find_next('dd').text.strip() if release_date_el else "-"
            # open_date = release_date.replace('.','')

            # 영화 상세 정보 url
            href = title_el['href']
            # 영화 개봉일 + 감독
            data = get_release_date(href, title)

            # 평점 정보 찾기
            rating_el = movie.find('dl', class_='info_group type_visible').find('span', class_='num')
            rating = rating_el.text.strip() if rating_el else "-"

            # 포스터 정보 찾기
            poster_el = movie.find('a', class_="img_box").find('img')
            poster = poster_el['src']

            box_office.append({
                'title': title,
                'release_date': data.get('open_date'),
                'director': data.get('director'),
                'rating': rating,
                'poster': poster
            })

        # print(f"box_office : {box_office}")
        return box_office

    except requests.exceptions.RequestException as e:
        return {'error': str(e)}


def get_ott_movie(num):
    try:
        movie_queries = [
            'query=넷플릭스+영화',
            'query=왓챠+영화',
            'query=티빙+영화',
        ]

        base_url = 'https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&{movie_query}'

        ott_names = ['netflix', 'watcha', 'tving']
        # cnt = 0
        # 각 플랫폼에 대한 리스트 초기화
        ott_list = []

        url = base_url.format(movie_query=movie_queries[num])

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        main_els = soup.find('ul', class_='list_info _panel').find_all('li', class_='info_box')

        ott_movies = []

        for main_el in main_els:
            # 영화 제목 정보 찾기
            title_el = main_el.find('a', class_='_text')
            title = title_el.get_text(strip=True)

            # 영화 상세 정보 url
            href = title_el['href']
            # 영화 개봉일 + 감독
            data = get_release_date(href,title)

            # 별점 정보 찾기
            rating = main_el.find('span', class_='num').get_text(strip=True)

            # 포스터 정보 찾기
            poster_el = main_el.find('div', class_="thumb_area").find('img')
            poster = poster_el['src']


            # 영화 데이터를 딕셔너리로 만들어 플랫폼에 해당하는 리스트에 추가
            ott_movies.append({
                'title': title,
                'release_date': data.get("open_date"),
                'rating': rating,
                'director': data.get("director"),
                'poster':poster
            })

        ott_data = {ott_names[num]: ott_movies}
        # print(ott_data)
        return ott_data

    except requests.exceptions.RequestException as e:
        return {'error': str(e)}

# get_ott_movie(1)
# get_box_office()

get_release_date("?where=nexearch&sm=tab_etc&mra=bkEw&pkid=68&os=14406752&qvt=0&query=영화%20콘크리트%20유토피아","콘크리트 유토피아")



