from movie_api import get_movie_api
from flask import jsonify
import json

def api_extract_info():
    result_data = get_movie_api()

    # 필요한 정보 추출
    extracted_info_list = []
    for result in result_data['Data'][0]['Result']:
        directors = result.get('directors', {}).get('director', [])
        director = directors[0] if directors else {}
        plots = result.get('plots', {}).get('plot', [])
        plot = plots[0] if plots else {}
        actors = result.get('actors', {}).get('actor', [])
        actor = actors[0] if actors else {}

        title = result.get('title', '').strip()
        posters = result.get('posters', '').strip()
        titleEng = result.get('titleEng', '').strip()
        repRlsDate = result.get('repRlsDate', '').strip()
        genre = result.get('genre', '').strip()
        nation = result.get('nation', '').strip()
        rating = result.get('rating', '').strip()
        runtime = result.get('runtime', '').strip()
        audiAcc = result.get('audiAcc', '').strip()
        directorNm = director.get('directorNm', '').strip()
        actorNm = actor.get('actorNm', '').strip()
        plotText = plot.get('plotText', '').strip()
        stlls = result.get('stlls', '').strip()

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
        # print("데이터 값 TEST : ", data)
        print("타이틀 값 TEST : ", title)
        # cleaned_title = re.sub(r'!HS[^!]*!HE', '', title).strip()
        # print(cleaned_title)
        print(movie_info_list)
        extracted_info_list.append(movie_info_list)
    return json.dumps(extracted_info_list, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    result = api_extract_info()
    if result:
        print(result)
