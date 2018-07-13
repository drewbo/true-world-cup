import json
import sys
from os.path import dirname as dir
sys.path.append(dir(sys.path[0]))

from flask import Flask
from flask import make_response
from flask_cors import CORS

from team_generator import team

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def get_scenario_data():
    return make_response(json.dumps(team.get_team(), sort_keys=True, ensure_ascii=False))

if __name__ == '__main__':
    app.run()
