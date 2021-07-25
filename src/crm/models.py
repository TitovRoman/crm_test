from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=128)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f"Категория: {self.title}"


class Status(models.Model):
    title = models.CharField(max_length=128)

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'

    def __str__(self):
        return f"Статус: {self.title}"


class Client(models.Model):
    first_name = models.CharField(
        'Имя',
        max_length=128,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=128,
        blank=True,
    )
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format:"
                " '+999999999'. Up to 15 digits allowed.",
    )
    phone_number = models.CharField(
        'Номер телефона',
        validators=[phone_regex],
        max_length=17,
        blank=True
    )
    email = models.EmailField('Электронная почта')
    tg_username = models.CharField('Ник в telegram', max_length=128, blank=True)
    registration_data = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f"Клиент {self.first_name} {self.last_name}"


class ApplicationWithSelectRelated(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related(
            'client',
            'status',
            'category',
            'employee',
        )


class ApplicationQuerySet(models.QuerySet):
    def all_select_related(self):
        return self.select_related(
            'client',
            'status',
            'category',
            'employee',
        )

class Application(models.Model):
    title = models.CharField('Заголовок', max_length=128)
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        null=True,
        on_delete=models.SET_NULL,
    )
    client = models.ForeignKey(
        Client,
        verbose_name='Клиент',
        null=True,
        on_delete=models.SET_NULL,
    )
    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Сотрудник',
        null=True,
        on_delete=models.SET_NULL,
    )
    description = models.TextField(
        'Описание'
    )
    status = models.ForeignKey(
        Status,
        verbose_name='Статус',
        on_delete=models.PROTECT,
    )
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def __str__(self):
        return f"Заявка №{self.pk} ({self.title})"

    objects = ApplicationQuerySet.as_manager()
