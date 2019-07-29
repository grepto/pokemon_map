from django.db import models


class Pokemon(models.Model):
    title = models.CharField('название', max_length=200)
    title_en = models.CharField('английское название', max_length=200)
    title_jp = models.CharField('японское название', max_length=200)
    description = models.TextField('описание', max_length=2000)
    image = models.ImageField(upload_to='pokemons', null=True, blank=True, verbose_name='изображение')
    next_evolution = models.OneToOneField('self', on_delete=models.CASCADE, null=True, blank=True,
                                          related_name='previous_evolution', verbose_name='в кого эволюционирует')

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, verbose_name='покемон')
    lat = models.FloatField('широта')
    lon = models.FloatField('долгота')
    appeared_at = models.DateTimeField('появится')
    disappeared_at = models.DateTimeField('исчезнет')
    level = models.IntegerField('уровень')
    health = models.IntegerField('здоровье')
    strength = models.IntegerField('прочность')
    defence = models.IntegerField('защита')
    stamina = models.IntegerField('выносливость')
