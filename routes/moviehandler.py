import json
from routes.movie import get_movie, get_ott_movie, get_movieApi
import re
def get_combined_movie_info():
    # 영화 정보를 가져오기
    ott_movie_info = json.loads(get_ott_movie())
    movie_info = json.loads(get_movie())

    # 영화 제목을 모으기
    titles_to_search = []
    # 개봉일 모으기
    releaseDate_to_search = []

    for ott_platform, movies in ott_movie_info.items():
        for movie in movies:
            title = movie.get('title', 'Unknown Title')
            releaseDate = movie.get('releaseDate', 'Unknown Release Date')
            titles_to_search.append(title)
            releaseDate_to_search.append(releaseDate)
            print(f"Title: {title}, Release Date: {releaseDate}")

    # movie_info에서 영화 제목과 개봉일 추가
    for movie in movie_info:
        title = movie.get('title', 'Unknown Title')
        releaseDate = movie.get('releaseDate', 'Unknown Release Date')
        titles_to_search.append(title)
        releaseDate_to_search.append(releaseDate)
        print(f"Title: {title}, Release Date: {releaseDate}")

    # 중복된 영화 제목 제거
    unique_titles = list(set(titles_to_search))

    extracted_info_list = []

    # test 파일
    # test = get_movieApi("러브 레터")
    # testData = test.get("Data")

    for i in unique_titles:
        data = get_movieApi(i, releaseDate_to_search)
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

            cleaned_title = re.sub(r'!HS(.*?)!HE', r'\1', title).strip()
            title_final = re.sub(r'\s+', ' ', cleaned_title).strip()

            movie_info_list = {
                "title": title_final,
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
            print(cleaned_title)
            print(movie_info_list)
            extracted_info_list.append(movie_info_list)
    return json.dumps(extracted_info_list, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    result = get_combined_movie_info()
    if result:
        print(result)
