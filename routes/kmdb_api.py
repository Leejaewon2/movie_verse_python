import requests
import json
from routes.basis_data import get_box_office, get_ott_movie
import re

def combine_movie_info():
    ls = []
    box_office = get_box_office()
    ls.append({"box_office":box_office})
    for i in range(3):
        ott = get_ott_movie(i)
        ls.append(ott)
    print(ls)
    return ls

combine_movie_info()

def api_search_ls():
    movie_ls = combine_movie_info()
    unique_titles = set()
    result = []

    for movie in movie_ls:
        for data in movie.values():
            for e in data:
                title = e['title']
                release_date = e['release_date']
                director = e['director']

                if title not in unique_titles:
                    unique_titles.add(title)
                    result.append({'title':title, 'release_date':release_date, 'director':director})
    print(result)
    return result

# api_search_ls()

def kmdb_api(title=None, release_date=None, director=None):
    API_KEY = 'F851HE5P50Z8OBX419D3'
    print(f"title : {title} / rlsdate : {release_date} / director : {director}")

    # 올바른 API 엔드포인트 및 매개변수
    url = f'http://api.koreafilm.or.kr/openapi-data2/wisenut/search_api/search_json2.jsp?collection=kmdb_new2'

    req_parameters = {
        'ServiceKey': API_KEY,
        'title': title,
        'director': director,
        'releaseDts': release_date
    }

    # 최대 재시도 횟수 설정
    max_retries = 3
    current_retry = 0

    # 요청 및 응답
    while current_retry < max_retries:
        try:
            r = requests.get(url, params=req_parameters)
            r.raise_for_status()  # 4xx 또는 5xx 응답에 대한 HTTPError 발생
            dict_data = r.json()
            if 'Data' in dict_data and dict_data['Data'][0].get('Result', []):
                return dict_data  # 정상적인 JSON 데이터 반환

            print("결과가 없습니다.")

            req_parameters = {
                'ServiceKey': API_KEY,
                'title': title,
                'director': None,  # Reduce to fewer parameters
                'releaseDts': None  # You can adjust as needed
            }

            current_retry += 1
            print(f"Retry #{current_retry}...")


        except requests.exceptions.RequestException as e:
            print(f"요청 중 오류가 발생했습니다: {e}")
            current_retry += 1
            print(f"재시도 중... (재시도 횟수: {current_retry})")

    print(f"{max_retries}번의 재시도 후에도 성공하지 못했습니다.")
    return {"error": "Maximum retries reached."}

def get_kmdb_info():
    search_ls = api_search_ls()
    # print(search_ls)
    result = []
    for search in search_ls:
        data = kmdb_api(search.get("title"), search.get("release_date"), search.get("director"))

        if 'Data' in data:
            result_data = data['Data'][0]['Result'][0]
            directors = result_data.get('directors', {}).get('director', [])
            director = directors[0] if directors else {}
            plots = result_data.get('plots', {}).get('plot', [])
            plot = plots[0] if plots else {}
            actors = result_data.get('actors', {}).get('actor', [])

            actor_names = [actor.get('actorNm', '').strip() for actor in actors[:5]]
            actor_names_string = ', '.join(actor_names)

            title = result_data.get('title', '').strip()
            posters = result_data.get('posters', '').strip()
            first_poster = posters.split('|')[0]
            titleEng = result_data.get('titleEng', '').strip()
            repRlsDate = result_data.get('repRlsDate', '').strip()
            genre = result_data.get('genre', '').strip()
            nation = result_data.get('nation', '').strip()
            rating = result_data.get('rating', '').strip()
            runtime = result_data.get('runtime', '').strip()
            audiAcc = result_data.get('audiAcc', '').strip()
            directorNm = director.get('directorNm', '').strip()
            actorNm = actor_names_string



            plotText = plot.get('plotText', '').strip()
            stlls = result_data.get('stlls', '').strip()

            cleaned_title = re.sub(r'!HS(.*?)!HE', r'\1', title).strip()
            title_final = re.sub(r'\s+', ' ', cleaned_title).strip()

            cleaned_dir_name = re.sub(r'!HS(.*?)!HE', r'\1', directorNm).strip()
            director = re.sub(r'\s+', ' ', cleaned_dir_name).strip()

            movie_info_list = {
                "title": title_final,
                "posters": first_poster,
                "titleEng": titleEng,
                "reprlsDate": repRlsDate,
                "genre": genre,
                "nation": nation,
                "rating": rating,
                "runtime": runtime,
                "audiAcc": audiAcc,
                "directorNm": director,
                "actorNm": actorNm,
                "plotText": plotText,
                "stlls": stlls,
            }

            result.append(movie_info_list)
            # print(result)
    return json.dumps(result, ensure_ascii=False, indent=4)

# get_kmdb_info()

if __name__ == '__main__':
    result = get_kmdb_info()
    if result:
        print(result)