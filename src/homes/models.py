from django.db import models


class Home(models.Model):
    HOUSE = 1
    APARTMENT = 2
    TYPE_HOME = ((HOUSE, "Дом"), (APARTMENT, "Квартира"))

    user = models.ForeignKey(
        "authentication.CustomUser", verbose_name="Пользователь", on_delete=models.CASCADE, related_name="homes"
    )
    name = models.CharField(verbose_name="Наименование", max_length=32)
    type_home = models.IntegerField(verbose_name="Тип", choices=TYPE_HOME)
    square = models.DecimalField(verbose_name="Площадь", max_digits=18, decimal_places=2, blank=True, null=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Дом"
        verbose_name_plural = "Дома"
        unique_together = ("name", "user")
        ordering = ("name", "-pk")


class Room(models.Model):
    user = models.ForeignKey(
        "authentication.CustomUser", verbose_name="Пользователь", on_delete=models.CASCADE, related_name="rooms"
    )
    home = models.ForeignKey(Home, verbose_name="Дом", on_delete=models.CASCADE, related_name="home")
    name = models.CharField(verbose_name="Наименование", max_length=32)
    square = models.DecimalField(verbose_name="Площадь", max_digits=18, decimal_places=2, blank=True, null=True)
    date_begin = models.DateField("Дата начала ремонта", blank=True, null=True)
    date_end = models.DateField("Дата окончания ремонта", blank=True, null=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Комната"
        verbose_name_plural = "Комнаты"
        unique_together = ("name", "user", "home")
        ordering = ("name", "-pk")
