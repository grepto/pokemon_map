import folium

from django.http import HttpResponseNotFound
from django.shortcuts import render
from pokemon_entities.models import Pokemon, PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = "https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832&fill=transparent"


def get_pokemon_image_url(pokemon, request):
    return f'{request.scheme}://{request.META["HTTP_HOST"]}{pokemon.image.url}' if pokemon.image else None


def add_pokemon(folium_map, lat, lon, name, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        tooltip=name,
        icon=icon,
    ).add_to(folium_map)


def get_pokemons_entity_map(pokemons_entity, request, location=MOSCOW_CENTER, zoom_start=12):
    map = folium.Map(location=location, zoom_start=zoom_start)
    for pokemon_entity in pokemons_entity:
        pokemon = pokemon_entity.pokemon
        add_pokemon(
            map, pokemon_entity.lat, pokemon_entity.lon,
            pokemon.title, get_pokemon_image_url(pokemon, request))

    return map


def show_all_pokemons(request):
    pokemons = Pokemon.objects.all()
    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': get_pokemon_image_url(pokemon, request),
            'title_ru': pokemon.title,
        })

    pokemons_entity = PokemonEntity.objects.all()
    folium_map = get_pokemons_entity_map(pokemons_entity, request)

    return render(request, "mainpage.html", context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        requested_pokemon = Pokemon.objects.filter(id=pokemon_id)[0]
    except IndexError:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    pokemon = {
        'pokemon_id': requested_pokemon.id,
        'title_ru': requested_pokemon.title,
        'title_en': requested_pokemon.title_en,
        'title_jp': requested_pokemon.title_jp,
        'description': requested_pokemon.description,
        'img_url': get_pokemon_image_url(requested_pokemon, request),
    }

    next_evolution = requested_pokemon.next_evolution
    if next_evolution:
        pokemon.update({'next_evolution': {
            'pokemon_id': next_evolution.id,
            'title_ru': next_evolution.title,
            'img_url': get_pokemon_image_url(next_evolution, request),
        }})

    previous_evolution = requested_pokemon.previous_evolution.all()
    if previous_evolution:
        pokemon.update({'previous_evolution': {
            'pokemon_id': previous_evolution[0].id,
            'title_ru': previous_evolution[0].title,
            'img_url': get_pokemon_image_url(previous_evolution[0], request),
        }})

    pokemons_entity = PokemonEntity.objects.filter(pokemon=requested_pokemon)
    folium_map = get_pokemons_entity_map(pokemons_entity, request)

    return render(request, "pokemon.html", context={'map': folium_map._repr_html_(),
                                                    'pokemon': pokemon})
