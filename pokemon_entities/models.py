from django.db import models


class Pokemon(models.Model):
    title = models.CharField('название', max_length=200)
    title_en = models.CharField('английское название', null=True, blank=True, max_length=200)
    title_jp = models.CharField('японское название', null=True, blank=True, max_length=200)
    description = models.TextField('описание', null=True, blank=True, max_length=2000)
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
    level = models.IntegerField('уровень', null=True, blank=True)
    health = models.IntegerField('здоровье', null=True, blank=True)
    strength = models.IntegerField('прочность', null=True, blank=True)
    defence = models.IntegerField('защита', null=True, blank=True)
    stamina = models.IntegerField('выносливость', null=True, blank=True)
