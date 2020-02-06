from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


# Create your models here.


class Diary(models.Model):

    class WeatherChoice(models.TextChoices):
        FOG = 'FG', _('안개')
        SNOW = 'SW', _('눈')
        SUNNY = 'SY', _('맑음')
        RAIN = 'RN', _('비')
        MICRO_DUST = 'MD', _('미세먼지')
        CLOUD = 'CD', _('구름')
        NOT_INTERESTED = 'NI', _('관심없음')

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                               related_name='Diaries')
    date = models.DateField('날짜')
    weather = models.CharField('날씨', max_length=2, choices=WeatherChoice.choices,
                               default=WeatherChoice.NOT_INTERESTED)
    Title = models.CharField('제목', max_length=20)
    Contents = models.TextField('내용')
    realized = models.CharField('느낀점', max_length=20)

    created = models.DateTimeField('작성날짜', auto_now_add=True)
    updated = models.DateTimeField('수정날짜', auto_now=True)

    def __str__(self):
        return str(self.date) + self.author.username

    class Meta:
        ordering = ['-author']
