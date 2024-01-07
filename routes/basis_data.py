import requests
import json
from bs4 import BeautifulSoup
from flask import jsonify
import time
import random

DEBUG_MODE = False

# 포스터 url 가져오기
def get_image_url(url,title, max_retries = 3) :
    retries = 0
    while retries < max_retries:
        if DEBUG_MODE:
            print(f'{title}의 포스터 가져오는 중 / 시도 : {retries + 1}')
        try :
            # 지연
            sleep_interval = random.uniform(0.5, 1.5)
            time.sleep(sleep_interval)

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raises HTTPError for bad responses

            soup = BeautifulSoup(response.text, 'html.parser')
            main_el = soup.find('body', class_='wrap-new api_animation').find('div', class_='sec_movie_photo')

            poster_outer = main_el.find('div', class_='_image_base_poster').find('div', class_='movie_photo_list')
            poster_el = poster_outer.find('li', class_='item').find('img')
            poster = poster_el['data-img-src']

            stlls_outer = main_el.find('div', class_='_image_base_stillcut')

            stlls_urls_ls = []

            try:
                if stlls_outer:
                    stlls_list = stlls_outer.find('div', class_='movie_photo_list')
                    stlls_els = stlls_list.find_all('li', class_='item')

                    for index, li in enumerate(stlls_els):
                        stlls_el = li.find('img')

                        if stlls_el:
                            stlls_url = stlls_el.get('data-img-src')
                            stlls_urls_ls.append(stlls_url)

                        if index == 7:
                            break

            except Exception as e :
                if DEBUG_MODE:
                    print(f"스틸가져오는 중 에러 : {e}")
                stlls_urls_ls = []

            stlls_urls = "|".join(stlls_urls_ls)

            if DEBUG_MODE:
                print(f"{title} poster : {poster}")
                print(f"{title} stlls : {stlls_urls}")

            result = {"poster": poster, "stlls":stlls_urls}
            return result

        except requests.exceptions.RequestException as e:
            if DEBUG_MODE:
                print(f'Error: {str(e)} - Retry {retries + 1}/{max_retries}')
        retries += 1

    return {'error': '3번 시도 후에도 실패'}

# 영화 전체 개봉일 + 감독 정보 가져오기
def get_more_data(href,title, max_retries = 3):
    retries = 0
    while retries < max_retries:
        if DEBUG_MODE:
            print(f'{title}의 추가 정보 가져오는 중 / 시도 : {retries + 1}')
        try:

            url = 'https://search.naver.com/search.naver' + href

            #지연
            sleep_interval = random.uniform(0.5, 1.5)
            time.sleep(sleep_interval)

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
            try:
                director = director_outer.find('strong', class_='name').find('a', class_='_text').text.strip()
            except AttributeError:
                try:
                    director = director_outer.find('strong', class_='name').find('span', class_='_text').text.strip()
                except AttributeError:
                    director = ""

            image_urls = get_image_url(url+"포토",title)

            result = {"open_date": open_date, "director": director, "poster": image_urls.get("poster"), "stlls": image_urls.get("stlls")}
            return result

        except requests.exceptions.RequestException as e:
            if DEBUG_MODE:
                print(f'Error: {str(e)} - Retry {retries + 1}/{max_retries}')
            retries += 1

    return {'error': '3번 시도 후에도 실패'}

# 현재 상영작
def get_box_office() :
    max_retries = 3
    retries = 0
    while retries < max_retries:
        if DEBUG_MODE:
            print(f'현재상영영화 정보 가져오는 중 / 시도 : {retries + 1}')
        try :

            url = 'https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&qvt=0&query=현재상영영화'

            # 지연
            sleep_interval = random.uniform(0.5, 1.5)
            time.sleep(sleep_interval)

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
                data = get_more_data(href, title)

                # 평점 정보 찾기
                score_el = movie.find('dl', class_='info_group type_visible').find('span', class_='num')
                score = score_el.text.strip() if score_el else "-"

                # 포스터 정보 찾기
                # poster_el = movie.find('a', class_="img_box").find('img')
                # poster = poster_el['src']

                box_office.append({
                    'title': title,
                    'release_date': data.get('open_date'),
                    'director': data.get('director'),
                    'score': score,
                    'poster': data.get('poster'),
                    'stlls': data.get('stlls')
                })

            # print(f"box_office : {box_office}")
            return box_office


        except requests.exceptions.RequestException as e:
            if DEBUG_MODE:
                print(f'Error: {str(e)} - Retry {retries + 1}/{max_retries}')
            retries += 1
    return {'error': '3번 시도 후에도 실패'}


def get_ott_movie(num):
    max_retries = 3
    retries = 0
    while retries < max_retries:
        if DEBUG_MODE:
            print(f'ott별 정보 가져오는 중 / 시도 : {retries + 1}')
        try:
            movie_queries = [
                'query=넷플릭스+영화',
                'query=왓챠+영화',
                'query=티빙+영화',
            ]

            base_url = 'https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&{movie_query}'

            # 지연
            sleep_interval = random.uniform(0.5, 1.5)
            time.sleep(sleep_interval)

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
                data = get_more_data(href,title)

                # 별점 정보 찾기
                score_el = main_el.find('span', class_='num')
                score = score_el.text.strip() if score_el else "-"

                # 포스터 정보 찾기
                # poster_el = main_el.find('div', class_="thumb_area").find('img')
                # poster = poster_el['src']


                # 영화 데이터를 딕셔너리로 만들어 플랫폼에 해당하는 리스트에 추가
                ott_movies.append({
                    'title': title,
                    'release_date': data.get("open_date"),
                    'score': score,
                    'director': data.get("director"),
                    'poster': data.get("poster"),
                    'stlls': data.get("stlls")
                })

            ott_data = {ott_names[num]: ott_movies}
            # print(ott_data)
            return ott_data


        except requests.exceptions.RequestException as e:
            if DEBUG_MODE:
                print(f'Error: {str(e)} - Retry {retries + 1}/{max_retries}')
            retries += 1
    return {'error': '3번 시도 후에도 실패'}

# get_ott_movie(1)
# get_box_office()

# get_more_data("?where=nexearch&sm=tab_etc&mra=bkEw&pkid=68&os=14406752&qvt=0&query=영화%20콘크리트%20유토피아","콘크리트 유토피아")



