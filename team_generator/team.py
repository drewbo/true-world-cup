import os
from os import path as op
import json

from faker import Faker
import numpy as np
import scipy.stats
import requests

by_country = json.load(open(op.join(op.dirname(__file__), 'bycountry.json'), 'r'))
country_pop = list(map(lambda x: int(x['pop']), by_country))
countries = list(map(lambda x: x['country'], by_country))

by_age_and_gender = json.load(open(op.join(op.dirname(__file__),'byageandgender.json'), 'r'))
age_gender_pop = list(map(lambda x: float(x['v']), by_age_and_gender))
age_gender = list(map(lambda x: (x['k'], x['g']), by_age_and_gender))

WORDNIK_API_KEY = os.environ.get('WORDNIK_API_KEY')

def get_latent_soccer_skill():
    return scipy.stats.norm(0, 1).cdf(np.random.randn())

def get_locale(country):
    if country == 'China':
        return 'zh_CN'
    elif country == 'India':
        return 'hi_IN'
    elif country == 'Brazil':
        return 'pt_BR'
    elif country == 'Russia':
        return 'ru_RU'
    elif country == 'Nepal':
        return 'ne_NP'
    else:
        return None

def get_age_and_gender():
    index = np.random.choice(len(age_gender), 1, p=list(np.array(age_gender_pop) / sum(age_gender_pop)))[0]
    age_range, gender = age_gender[index]
    range_list = list(map(lambda x: int(x), age_range.split('-')))
    return int(np.random.random_integers(*range_list)), gender

def get_country():
    return np.random.choice(countries, 1, p=list(np.array(country_pop) / sum(country_pop)))[0]

def get_name(country, gender):
    locale = get_locale(country)
    fake = Faker(locale)
    if gender == 'male':
        return fake.name_male()
    else:
        return fake.name_female()

def get_team_name(country):
    locale = get_locale(country)
    fake = Faker(locale)
    plural_noun_request = requests.get('https://api.wordnik.com/v4/words.json/randomWord?hasDictionaryDef=true&includePartOfSpeech=noun-plural&maxCorpusCount=-1&minDictionaryCount=1&maxDictionaryCount=-1&minLength=5&maxLength=-1&api_key=' + WORDNIK_API_KEY)
    plural_noun = plural_noun_request.json()['word']
    return '%s %s' % (fake.city(), plural_noun.capitalize())

def get_players():
    players = []
    for player in range(11):
        country = get_country()
        age, gender = get_age_and_gender()
        name = get_name(country, gender)
        skill = get_latent_soccer_skill()
        player = dict(country=country, age=age, gender=gender, name=name, skill=skill)
        players.append(player)
    return players

def get_team():
    players = get_players()
    random_player_country = np.random.choice(players, 1)[0]['country']
    team_name = get_team_name(random_player_country)
    return dict(players=players, name=team_name)

if __name__ == '__main__':
    team = get_team()
    print(json.dumps(team, indent=4, sort_keys=True, ensure_ascii=False))
