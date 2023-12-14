from movie_api import get_movie_api
import json
import schedule
import time

def get_api_extract_info():
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
        extracted_info_list.append(movie_info_list)
        # print("데이터 값 TEST : ", result_data)
        # print("타이틀 값 TEST : ", title)
        # print(movie_info_list)
    return json.dumps(extracted_info_list, ensure_ascii=False, indent=4)


# 스케쥴링
def movie_api_send():
    result = get_api_extract_info()
    print("movie_api 정보를 전송합니다.\n" + result)


# 매일 정해진 시간에 동작 하도록 구현
schedule.every().day.at("15:30").do(movie_api_send)

while True:
    schedule.run_pending()
    time.sleep(1)





