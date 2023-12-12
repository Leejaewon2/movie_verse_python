import json
from routes.movie import get_movie, get_ott_movie, get_movieApi
import re

def get_combined_movie_info():
    # 영화 정보를 가져오기
    ott_movie_info = json.loads(get_ott_movie())
    movie_info = json.loads(get_movie())

    # 영화 제목을 모으기
    titles_to_search = []

    # ott_movie_info에서 영화 제목 추가
    for ott_platform, movies in ott_movie_info.items():
        for movie in movies:
            titles_to_search.append(movie['title'])

    # movie_info에서 영화 제목 추가
    for movie in movie_info:
        titles_to_search.append(movie['title'])

    # 중복된 영화 제목 제거
    unique_titles = list(set(titles_to_search))

    extracted_info_list = []
    # test = get_movieApi("러브 레터")
    # testData = test.get("Data")
    for i in unique_titles:
        data = get_movieApi(i)
        if 'Data' in data:
            result_data = data['Data'][0]['Result'][0]
            directors = result_data.get('directors', {}).get('director', [])
            director = directors[0] if directors else {}
            plots = result_data.get('plots', {}).get('plot', [])
            plot = plots[0] if plots else {}
            actors = result_data.get('actors', {}).get('actor', [])
            actor = actors[0] if actors else {}

            title = result_data.get('title', '').strip()
            posters = result_data.get('posters', '').strip()
            titleEng = result_data.get('titleEng', '').strip()
            repRlsDate = result_data.get('repRlsDate', '').strip()
            genre = result_data.get('genre', '').strip()
            nation = result_data.get('nation', '').strip()
            rating = result_data.get('rating', '').strip()
            runtime = result_data.get('runtime', '').strip()
            audiAcc = result_data.get('audiAcc', '').strip()
            directorNm = director.get('directorNm', '').strip()
            actorNm = actor.get('actorNm', '').strip()
            plotText = plot.get('plotText', '').strip()
            stlls = result_data.get('stlls', '').strip()

            movie_info_list = {
                "title": title,
                "posters": posters,
                "titleEng": titleEng,
                "reprlsDate": repRlsDate,
                "genre": genre,
                "nation": nation,
                "rating": rating,
                "runtime": runtime,
                "audiAcc": audiAcc,
                "directorNm": directorNm,
                "actorNm": actorNm,
                "plotText": plotText,
                "stlls": stlls,
            }
            print("데이터 값 TEST : ", data)
            print("타이틀 값 TEST : ", title)
            # cleaned_title = re.sub(r'!HS[^!]*!HE', '', title).strip()
            # print(cleaned_title)
            print(movie_info_list)
            extracted_info_list.append(movie_info_list)
    return json.dumps(extracted_info_list, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    result = get_combined_movie_info()
    if result:
        print(result)
