import os
import textwrap
from main.models import Event
import random
from django.utils import timezone


path = '.'

addresses = [
    'Moscow, Arbat',
    'Moscow, Teatralnaya',
    'Moscow, Red Square',
    'Moscow, VDNH',
    'Moscow, Gorkov Park',
    'Vladivostok, Naberezhnaya',
    'China, Pekin',
    'Vladivostok, China Town',
    'Moscow, China Town',
    'St. Petersburg, China Town',
    'St. Petersburg, Bridge',
    'St. Petersburg, Ermitazh',
    'St. Petersburg, Naberezhnaya',
]

countries = [
    "Russia",
    "USA",
    "Italia",
    "Spain",
    "Germany",
    "Australia"
]

sportTypes = [
    "Football",
    "PokemonBall",
    "Golf",
    "Sleeping"
]


def generate():
    with open(os.path.join(path, 'names.txt'), "r", encoding='utf-8') as file:
        names = file.read().split('\n')

    # print(names)

    with open(os.path.join(path, 'descs.txt'), "r") as file:
        descs = textwrap.wrap(file.read(), 200)

    images = list(filter(lambda x: "jpg" in x, next(os.walk(path))[2]))

    print(images)

    for i in range(1000):
        Event.objects.create(
            name=random.choice(names),
            address=random.choice(addresses),
            time=timezone.datetime(
                year=random.randrange(2000, 2020),
                month=random.randrange(1, 12),
                day=random.randrange(1, 28),
                hour=random.randrange(0, 23),
                minute=random.randrange(0, 60),
                tzinfo=timezone.utc
            ),
            desc=random.choice(descs),
            imageUrl="images/pokemons/" + random.choice(images)
        )
