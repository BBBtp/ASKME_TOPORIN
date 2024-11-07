import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from questionnaire.models import Profile, Question, Answer, Tag, QuestionLike, AnswerLike


class Command(BaseCommand):
    help = "Заполнить базу тестовыми данными."

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help="Коэффициент для заполнения базы")

    def handle(self, *args, **options):
        ratio = options['ratio']

        # Создание пользователей и профилей
        users = [
            User(
                username=f'user_{i}',
                email=f'user_{i}@example.com',
                password='password',
                last_login=timezone.now()  # Устанавливаем last_login
            ) for i in range(ratio)
        ]
        User.objects.bulk_create(users)
        profiles = [Profile(user=user) for user in User.objects.all()]
        Profile.objects.bulk_create(profiles)
        self.stdout.write(self.style.SUCCESS(f'Создано {len(users)} пользователей и профилей.'))

        # Создание тегов
        tags = [Tag(name=f'Tag_{i}') for i in range(ratio)]
        Tag.objects.bulk_create(tags)
        tags = list(Tag.objects.all())  # Сохраняем для ссылок на теги
        self.stdout.write(self.style.SUCCESS(f'Создано {len(tags)} тегов.'))

        # Создание вопросов с тегами
        questions = [
            Question(
                title=f'Вопрос номер {i}',
                text=f'Это текст вопроса {i}.',
                author=random.choice(User.objects.all())
            ) for i in range(ratio * 10)
        ]
        Question.objects.bulk_create(questions)
        self.stdout.write(self.style.SUCCESS(f'Создано {len(questions)} вопросов.'))

        # Создание связей между вопросами и тегами
        question_tag_links = []
        for question in Question.objects.all():
            selected_tags = random.sample(list(tags), min(5, len(tags)))  # Преобразуем QuerySet в список
            for tag in selected_tags:
                question_tag_links.append(Question.tags.through(question_id=question.id, tag_id=tag.id))

        Question.tags.through.objects.bulk_create(question_tag_links)
        self.stdout.write(self.style.SUCCESS(f'Создано {len(question_tag_links)} связей между вопросами и тегами.'))

        # Создание ответов
        answers = [
            Answer(
                question=random.choice(questions),
                text=f'Это текст ответа {i}.',
                author=random.choice(User.objects.all())
            ) for i in range(ratio * 100)
        ]
        Answer.objects.bulk_create(answers)
        self.stdout.write(self.style.SUCCESS(f'Создано {len(answers)} ответов.'))

        # Создание лайков к вопросам
        question_likes = [
            QuestionLike(question=random.choice(questions), user=random.choice(User.objects.all()))
            for _ in range(ratio * 200)
        ]
        QuestionLike.objects.bulk_create(question_likes, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS(f'Создано {len(question_likes)} лайков к вопросам.'))

        # Создание лайков к ответам
        answer_likes = [
            AnswerLike(answer=random.choice(answers), user=random.choice(User.objects.all()))
            for _ in range(ratio * 200)
        ]
        AnswerLike.objects.bulk_create(answer_likes, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS(f'Создано {len(answer_likes)} лайков к ответам.'))

        self.stdout.write(self.style.SUCCESS("База данных успешно заполнена."))
