from django.db import models

# Create your models here.
#
#
# models bu malumotlar bazasini pythondagi korinishi
# malumotlar bazasi bu data base
# FloatField bu ,li sonlar maydoni
# PositiveIntegerField bu + butun sonlar maydoni
# CharField bu cheklangan matn maydoni(belgilar)
# TextField bu chekalanmagan matn maydoni
# DataTimeField bu sana va vaqt maydoni
# DataField bu sana maydoni
# BooleanField : True/False
# EmailField email manzil uchun
# ForeignKey boshqa modellarga bog'lash
# field maydon
# ImageField rasm joylash uchun maydon




# test_1

class ish(models.Model):
    nomi = models.CharField(max_length=50)
    narxi = models.PositiveIntegerField()
    rasmi = models.ImageField()
    info = models.TextField()


def __str__(self):
    return self.nomi



