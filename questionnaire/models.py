from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    name = models.CharField('Название', max_length=30, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    avatar = models.ImageField("Аватар", upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return f"Профиль {self.user.username}"

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

class Question(models.Model):
    title = models.CharField("Заголовок", max_length=255)
    text = models.TextField("Текст вопроса")
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    tags = models.ManyToManyField(Tag, related_name='questions', verbose_name="Теги")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/questions/{self.id}/"

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE, verbose_name="Вопрос")
    text = models.TextField("Текст ответа")
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")

    def __str__(self):
        return f"Ответ к вопросу: {self.question.title}"

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

class QuestionLike(models.Model):
    question = models.ForeignKey(Question, related_name='likes', on_delete=models.CASCADE, verbose_name="Вопрос")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        unique_together = ('question', 'user')
        verbose_name = "Лайк вопроса"
        verbose_name_plural = "Лайки вопросов"

class AnswerLike(models.Model):
    answer = models.ForeignKey(Answer, related_name='likes', on_delete=models.CASCADE, verbose_name="Ответ")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        unique_together = ('answer', 'user')
        verbose_name = "Лайк ответа"
        verbose_name_plural = "Лайки ответов"
