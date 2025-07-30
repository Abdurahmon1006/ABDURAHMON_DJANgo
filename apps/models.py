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


# Yutuqlar uchun model
class yutuq(models.Model):
    nomi = models.CharField(max_length=100, verbose_name="Yutuq nomi")
    tavsif = models.TextField(verbose_name="Yutuq haqida")
    sana = models.DateField(verbose_name="Olingan sana")
    rasmi = models.ImageField(upload_to='yutuqlar/', verbose_name="Yutuq rasmi")
    darajasi = models.CharField(max_length=50, choices=[
        ('bronza', 'Bronza'),
        ('kumush', 'Kumush'),
        ('oltin', 'Oltin'),
        ('maxsus', 'Maxsus'),
    ], default='bronza', verbose_name="Yutuq darajasi")
    link = models.URLField(max_length=250, blank=True, null=True, verbose_name="Yutuq havolasi")
    
    class Meta:
        verbose_name = "Yutuq"
        verbose_name_plural = "Yutuqlar"
        ordering = ['-sana']  # Eng yangi yutuqlar avval
    
    def __str__(self):
        return self.nomi



