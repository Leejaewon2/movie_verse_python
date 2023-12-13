#app.py
from flask import Flask, Response ,jsonify
from flask_cors import CORS
from routes.movie import get_movie
from routes.movie import get_ott_movie
from routes.moviehandler import get_combined_movie_info
from routes.kmdb_api import get_kmdb_info

app = Flask(__name__)
CORS(app, origins=['http://localhost:3000'])

app.add_url_rule('/api/ottMovie', 'get_ott_movie', get_ott_movie, methods=['GET'])
app.add_url_rule('/api/movie', 'get_movie', get_movie, methods=['GET'])

#get_movieApi 함수가 JSON 응답을 반환
@app.route('/api/movieApi', methods=['GET'])
def route_get_movieApi():
    result = get_combined_movie_info()

    # jsonify 함수를 사용하여 JSON 응답으로 전송하는 코드
    # 그러나 여전히 JSON 응답이 HTML 이스케이프되지 않았다는 문제가 있을 수 있음
    # 때문에 jsonify 함수를 사용하지 않고 직접 문자열로 응답하는 방법을 시도해서 Reponse 사용한것
    # return jsonify(result)

    # 이렇게 변경하면 직접적으로 Response 객체를 생성하여 content_type을 명시함으로써 JSON 문자열이
    # HTML 이스케이프되지 않도록 할 수 있음
    return Response(result, content_type='application/json; charset=utf-8')

@app.route('/api/kmdblist', methods=['GET'])
def route_get_kmdb_info():
    result = get_kmdb_info()

    return Response(result, content_type='application/json; charset=utf-8')

if __name__ == '__main__':
    app.run(debug=True)


