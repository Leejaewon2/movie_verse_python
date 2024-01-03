from routes.movie_api import get_movie_api
import json
import schedule
import time
import re

DEBUG_MODE = False

def get_api_extract_info():
    result_data_ls = get_movie_api()

    # 필요한 정보 추출
    extracted_info_list = []
    for result_data in result_data_ls['Data'][0]['Result']:
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
        score = ' '
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
            "score": score,
            "directorNm": director,
            "actorNm": actorNm,
            "plotText": plotText,
            "stlls": stlls,
        }

        if DEBUG_MODE:
            print(title)
        extracted_info_list.append(movie_info_list)
    if DEBUG_MODE:
        print(extracted_info_list)
        # print("데이터 값 TEST : ", result_data)
        # print("타이틀 값 TEST : ", title)
        # print(movie_info_list)
    return json.dumps(extracted_info_list, ensure_ascii=False, indent=4)

# get_api_extract_info()

# 스크립트 실행 시 KMDB 정보를 가져와 출력하는 부분
if __name__ == '__main__':
    result = get_api_extract_info()
    if result:
        print(result)


