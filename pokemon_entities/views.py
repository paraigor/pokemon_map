import folium
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Pokemon, PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    "https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision"
    "/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832"
    "&fill=transparent"
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def get_pokemon_image_url(image):
    return image.url if image else DEFAULT_IMAGE_URL


def show_all_pokemons(request):
    localtime_now = timezone.localtime()
    pokemon_entities = PokemonEntity.objects.filter(
        appeared_at__lte=localtime_now,
        disappeared_at__gt=localtime_now,
    )

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(
                get_pokemon_image_url(pokemon_entity.pokemon.image)
            ),
        )

    pokemons = Pokemon.objects.all()

    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append(
            {
                "pokemon_id": pokemon.pk,
                "img_url": get_pokemon_image_url(pokemon.image),
                "title_ru": pokemon.title_ru,
            }
        )

    return render(
        request,
        "mainpage.html",
        context={
            "map": folium_map._repr_html_(),
            "pokemons": pokemons_on_page,
        },
    )


def show_pokemon(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, pk=pokemon_id)

    pokemon_next_evolution = pokemon.next_evolutions.filter().first()

    pokemon_previous_evolution_on_page = {
            "title_ru": pokemon.previous_evolution.title_ru,
            "pokemon_id": pokemon.previous_evolution.pk,
            "img_url": get_pokemon_image_url(pokemon.previous_evolution.image),
        } if pokemon.previous_evolution else None

    pokemon_next_evolution_on_page = {
            "title_ru": pokemon_next_evolution.title_ru,
            "pokemon_id": pokemon_next_evolution.pk,
            "img_url": get_pokemon_image_url(pokemon_next_evolution.image),
        } if pokemon_next_evolution else None

    pokemon_on_page = {
        "img_url": get_pokemon_image_url(pokemon.image),
        "title_ru": pokemon.title_ru,
        "title_en": pokemon.title_en,
        "title_jp": pokemon.title_jp,
        "description": pokemon.description,
        "previous_evolution": pokemon_previous_evolution_on_page,
        "next_evolution": pokemon_next_evolution_on_page,
    }

    localtime_now = timezone.localtime()
    pokemon_entities = pokemon.entities.filter(
        appeared_at__lte=localtime_now,
        disappeared_at__gt=localtime_now,
    )

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(
                get_pokemon_image_url(pokemon_entity.pokemon.image),
            ),
        )

    return render(
        request,
        "pokemon.html",
        context={"map": folium_map._repr_html_(), "pokemon": pokemon_on_page},
    )
