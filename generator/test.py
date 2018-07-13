import json

from faker import Faker
import numpy as np
import scipy.stats

by_country = json.load(open('bycountry.json', 'r'))
country_pop = list(map(lambda x: int(x['pop']), by_country))
countries = list(map(lambda x: x['country'], by_country))

by_age_and_gender = json.load(open('byageandgender.json', 'r'))
age_gender_pop = list(map(lambda x: float(x['v']), by_age_and_gender))
age_gender = list(map(lambda x: (x['k'], x['g']), by_age_and_gender))

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

def get_team():
    team = []
    for player in range(11):
        country = get_country()
        age, gender = get_age_and_gender()
        name = get_name(country, gender)
        skill = get_latent_soccer_skill()
        player = dict(country=country, age=age, gender=gender, name=name, skill=skill)
        team.append(player)
    return team

if __name__ == '__main__':
    team = get_team()
    print(json.dumps(team, indent=4, sort_keys=True, ensure_ascii=False))
