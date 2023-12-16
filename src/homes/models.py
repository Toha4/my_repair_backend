from django.db import models


class RepairObject(models.Model):
    LAND = 1
    APARTMENT = 2
    TYPE_OBJECT = ((LAND, "Земельный участок"), (APARTMENT, "Квартира"))

    user = models.ForeignKey(
        "authentication.CustomUser", verbose_name="Пользователь", on_delete=models.CASCADE, related_name="repair_objects"
    )
    name = models.CharField(verbose_name="Наименование", max_length=32)
    type_object = models.IntegerField(verbose_name="Тип", choices=TYPE_OBJECT)
    square = models.DecimalField(verbose_name="Площадь", max_digits=18, decimal_places=2, blank=True, null=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Объект ремонта"
        verbose_name_plural = "Объекты ремонта"
        unique_together = ("name", "user")
        ordering = ("name", "-pk")

    @property
    def type_object_name(self):
        if self.type_object:
            return dict((x, y) for x, y in self.TYPE_OBJECT).get(self.type_object)
        return ""


class Building(models.Model):
    user = models.ForeignKey(
        "authentication.CustomUser", verbose_name="Пользователь", on_delete=models.CASCADE, related_name="buildings"
    )
    repair_object = models.ForeignKey(RepairObject, verbose_name="Объект ремонта", on_delete=models.CASCADE, related_name="buildings")
    name = models.CharField(verbose_name="Наименование", max_length=32)
    square = models.DecimalField(verbose_name="Площадь", max_digits=18, decimal_places=2, blank=True, null=True)
    date_begin = models.DateField("Дата начала ремонта", blank=True, null=True)
    date_end = models.DateField("Дата окончания ремонта", blank=True, null=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Строение"
        verbose_name_plural = "Строения"
        unique_together = ("name", "repair_object", "user")
        ordering = ("name", "-pk")

    def save(self, *args, **kwargs):
        self.repair_object = self.user.settings.current_repair_object
        super(Building, self).save(*args, **kwargs)


class Room(models.Model):
    user = models.ForeignKey(
        "authentication.CustomUser", verbose_name="Пользователь", on_delete=models.CASCADE, related_name="rooms"
    )
    repair_object = models.ForeignKey(RepairObject, verbose_name="Объект ремонта", on_delete=models.CASCADE, related_name="rooms")
    building = models.ForeignKey(
        Building, verbose_name="Строение", on_delete=models.CASCADE, related_name="rooms", blank=True, null=True
    )
    name = models.CharField(verbose_name="Наименование", max_length=32)
    square = models.DecimalField(verbose_name="Площадь", max_digits=18, decimal_places=2, blank=True, null=True)
    date_begin = models.DateField("Дата начала ремонта", blank=True, null=True)
    date_end = models.DateField("Дата окончания ремонта", blank=True, null=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Комната"
        verbose_name_plural = "Комнаты"
        unique_together = ("name", "user", "repair_object", 'building')
        ordering = ("name", "-pk")

    def save(self, *args, **kwargs):
        self.repair_object = self.user.settings.current_repair_object
        super(Room, self).save(*args, **kwargs)
