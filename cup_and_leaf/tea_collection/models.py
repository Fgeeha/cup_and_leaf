from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

User = get_user_model()

TITLE_MAX_LENGTH = 256
STR_MAX_LENGTH = 50


class PublishedModel(models.Model):
    is_published = models.BooleanField(
        "Опубликовано",
        default=True,
        help_text="Снимите галочку, чтобы скрыть публикацию.",
    )
    created_at = models.DateTimeField("Добавлено", auto_now_add=True)

    class Meta:
        abstract = True
        default_related_name = "%(app_label)s_%(class)s_related"


class TeaType(PublishedModel):
    title = models.CharField(
        "Название типа чая",
        max_length=TITLE_MAX_LENGTH,
        help_text="Максимальная длина 256 символов",
    )
    description = models.TextField("Описание")
    slug = models.SlugField(
        "Идентификатор",
        unique=True,
        help_text=(
            "Идентификатор страницы для URL; разрешены символы латиницы, "
            "цифры, дефис и подчёркивание."
        ),
    )

    class Meta(PublishedModel.Meta):
        verbose_name = "тип чая"
        verbose_name_plural = "Типы чая"
        ordering = ("title",)

    def __str__(self):
        return self.title[:STR_MAX_LENGTH]


class TeaOrigin(PublishedModel):
    name = models.CharField(
        "Страна происхождения",
        max_length=TITLE_MAX_LENGTH,
        help_text="Максимальная длина 256 символов",
    )
    description = models.TextField("Описание региона", blank=True)

    class Meta(PublishedModel.Meta):
        verbose_name = "страна происхождения"
        verbose_name_plural = "Страны происхождения"
        ordering = ("name",)

    def __str__(self):
        return self.name[:STR_MAX_LENGTH]


class TeaPost(models.Model):
    TYPE_CHOICES = [
        ("green", "Зеленый"),
        ("black", "Черный"),
        ("white", "Белый"),
        ("oolong", "Улун"),
        ("pu_erh", "Пуэр"),
        ("yellow", "Желтый"),
    ]

    ORIGIN_CHOICES = [
        ("china", "Китай"),
        ("japan", "Япония"),
        ("india", "Индия"),
        ("sri_lanka", "Шри-Ланка"),
        ("taiwan", "Тайвань"),
        ("vietnam", "Вьетнам"),
        ("other", "Другое"),
    ]

    TEA_GRADE_CHOICES = [
        ("special", "Особый"),
        ("first", "Первый"),
        ("second", "Второй"),
        ("third", "Третий"),
    ]

    title = models.CharField(max_length=200, verbose_name="Название")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="Тип чая")
    origin = models.CharField(
        max_length=20, choices=ORIGIN_CHOICES, verbose_name="Страна происхождения"
    )
    production_year = models.PositiveIntegerField(verbose_name="Год производства")
    tea_grade = models.CharField(
        max_length=20, choices=TEA_GRADE_CHOICES, verbose_name="Сорт чая"
    )
    appearance = models.TextField(verbose_name="Внешний вид")
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(
        upload_to="tea_images/", null=True, blank=True, verbose_name="Изображение"
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Чай"
        verbose_name_plural = "Чаи"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("tea_collection:tea_post_detail", kwargs={"pk": self.pk})


class TeaComment(models.Model):
    text = models.TextField("Текст комментария")
    tea_post = models.ForeignKey(
        TeaPost,
        on_delete=models.CASCADE,
        verbose_name="Чай",
        related_name="comments",
    )
    created_at = models.DateTimeField("Добавлено", auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор комментария",
        related_name="tea_comments",
    )
    rating = models.IntegerField(
        "Оценка",
        choices=[(i, i) for i in range(1, 6)],
        null=True,
        blank=True,
        help_text="Оценка от 1 до 5",
    )

    class Meta:
        verbose_name = "комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ("created_at",)

    def __str__(self):
        return self.text[:STR_MAX_LENGTH]
