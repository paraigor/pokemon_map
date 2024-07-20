from django.db import models  # noqa F401


class Pokemon(models.Model):
    title_ru = models.CharField("название", max_length=200)
    title_en = models.CharField(
        "название на английском", max_length=200, blank=True
    )
    title_jp = models.CharField(
        "название на японском", max_length=200, blank=True
    )
    image = models.ImageField("изображение", null=True, blank=True)
    description = models.TextField("описание", blank=True)
    previous_evolution = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="next_evolution",
        verbose_name="из кого эволюционирует",
    )

    def __str__(self):
        return self.title_ru


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon, on_delete=models.CASCADE, verbose_name="покемон"
    )
    lat = models.FloatField("широта", default=0, blank=True)
    lon = models.FloatField("долгота", default=0, blank=True)
    appeared_at = models.DateTimeField(
        "время появления", null=True, blank=True
    )
    disappeared_at = models.DateTimeField(
        "время исчезновения", null=True, blank=True
    )
    level = models.IntegerField("уровень", default=0)
    health = models.IntegerField("здоровье", default=0)
    strength = models.IntegerField("сила", default=0)
    defence = models.IntegerField("защита", default=0)
    stamina = models.IntegerField("выносливость", default=0)

    def __str__(self):
        return f"Сущность {self.pokemon.title_ru}"
