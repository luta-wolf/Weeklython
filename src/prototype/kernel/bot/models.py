from operator import mod
from pyexpat import model
import re
from tabnanny import verbose
from django.db import models
from django.forms import IntegerField

class Campus(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')

    class Meta:
        verbose_name = "Кампус"
        verbose_name_plural = "Кампусы"
    
    def __str__(self) -> str:
        return self.name

class Role(models.Model):
    name = models.CharField(max_length=255, verbose_name='Роль')
    is_admin = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Роль"
        verbose_name_plural = "Роли"
    
    def __str__(self) -> str:
        return self.name

class ObjectType(models.Model):
    name = models.CharField(max_length=255, verbose_name='Тип')

    class Meta:
        verbose_name = "Тип объекта"
        verbose_name_plural = "Типы объектов"
    
    def __str__(self) -> str:
        return self.name

class Status(models.Model):
    name = models.CharField(max_length=255, verbose_name='Статус')

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"
    
    def __str__(self) -> str:
        return self.name

class SchoolObject(models.Model):
    object_type = models.ForeignKey(ObjectType, on_delete=models.CASCADE)
    object_name = models.CharField(max_length=255, verbose_name='Наименование')
    object_desc = models.CharField(max_length=255, verbose_name='Описание', null=True)
    object_image = models.BinaryField(null=True, verbose_name='Изображение')
    object_campus = models.ForeignKey(Campus, on_delete=models.CASCADE)
    object_floor = models.IntegerField(verbose_name='Этаж')
    object_room = models.CharField(max_length=255, verbose_name='Помещение')
    object_role = models.ManyToManyField(Role, related_name="school_objects", verbose_name='Права доступа')

    class Meta:
        verbose_name = "Объект бронирования"
        verbose_name_plural = "Объекты бронирования"
    
    def __str__(self) -> str:
        return self.object_type.name + ' '+ self.object_name + ' ' +str(self.object_floor)+ ' этаж ' + self.object_campus.name


class User(models.Model):

    firstname = models.CharField(max_length=255, verbose_name='Имя', null=True)
    surname = models.CharField(max_length=255, verbose_name='Отчество', null=True, blank=True)
    lastname = models.CharField(max_length=255, verbose_name='Фамилия', null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, verbose_name='Role', null=True)
    login = models.CharField(max_length=25, verbose_name='Логин', null=True)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE, verbose_name='Campus', null=True)
    bot_id = models.CharField(max_length=255, blank=True, null=True, verbose_name='Telegram ID')

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return str(self.firstname) + ' ' + str(self.login) + ' ['+str(self.role.name)+']'


class Booking(models.Model):
    start = models.DateTimeField(null=False, verbose_name='Начало бронирования')
    end = models.DateTimeField(verbose_name='Конец бронирования')
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    school_object = models.ForeignKey(SchoolObject, on_delete=models.CASCADE)
    book_date = models.DateTimeField(auto_now=True, verbose_name='Дата бронирования')

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
    
    def __str__(self) -> str:
        return self.school_object.object_name +' ' + str(self.start)