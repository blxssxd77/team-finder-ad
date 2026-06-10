from django.core.management.base import BaseCommand

from projects.models import Project
from users.models import User


class Command(BaseCommand):
    help = 'Загружает тестовых пользователей и проекты'

    def handle(self, *args, **options):
        if User.objects.filter(email='admin@teamfinder.ru').exists():
            self.stdout.write('Данные уже загружены.')
            return

        User.objects.create_superuser(
            email='admin@teamfinder.ru',
            password='admin12345',
            name='Админ',
            surname='Системный',
            phone='+79000000000',
        )

        users_data = [
            {
                'email': 'maria@example.com',
                'password': 'testpass123',
                'name': 'Мария',
                'surname': 'Байбородина',
                'about': 'Frontend-разработчик с опытом в React и Vue.js.',
                'phone': '+79001112233',
                'github_url': 'https://github.com/maria-dev',
            },
            {
                'email': 'nikita@example.com',
                'password': 'testpass123',
                'name': 'Никита',
                'surname': 'Воронин',
                'about': 'Python Backend Developer. Специализируюсь на Django.',
                'phone': '+79002223344',
                'github_url': 'https://github.com/nikita-dev',
            },
            {
                'email': 'alex@example.com',
                'password': 'testpass123',
                'name': 'Алексей',
                'surname': 'Иванов',
                'about': 'Full-stack разработчик и DevOps-инженер.',
                'phone': '+79003334455',
                'github_url': 'https://github.com/alex-dev',
            },
        ]

        users = []
        for data in users_data:
            password = data.pop('password')
            user = User.objects.create_user(**data)
            user.set_password(password)
            user.save()
            users.append(user)

        projects_data = [
            {
                'name': 'Платформа для mental health поддержки MindSpace',
                'description': (
                    'Разрабатываем приложение для поддержки ментального здоровья. '
                    'Функционал: дневник эмоций с AI-анализом, медитации и практики.'
                ),
                'owner': users[0],
            },
            {
                'name': 'Fitness трекер с геймификацией FitQuest',
                'description': (
                    'Мобильное приложение для отслеживания физической активности '
                    'с элементами игры и квестов.'
                ),
                'owner': users[1],
            },
            {
                'name': 'Децентрализованная платформа для фрилансеров Web3Lance',
                'description': (
                    'Блокчейн-платформа для фрилансеров без посредников '
                    'с умными контрактами.'
                ),
                'owner': users[2],
            },
            {
                'name': 'AI-ассистент для изучения языков LinguaBot',
                'description': (
                    'Чат-бот на базе ИИ для практики иностранных языков '
                    'с исправлением ошибок.'
                ),
                'owner': users[1],
            },
            {
                'name': 'Экологический маркетплейс GreenChoice',
                'description': (
                    'Маркетплейс для продажи экологичных товаров '
                    'от локальных производителей.'
                ),
                'owner': users[0],
            },
        ]

        projects = []
        for data in projects_data:
            owner = data['owner']
            project = Project.objects.create(**data)
            project.participants.add(owner)
            projects.append(project)

        projects[1].participants.add(users[0], users[2])
        projects[2].participants.add(users[1])
        projects[4].participants.add(users[1], users[2])

        users[1].favorites.add(projects[0])
        users[0].favorites.add(projects[1])
        users[2].favorites.add(projects[1], projects[4])
        users[1].favorites.add(projects[4])

        self.stdout.write(self.style.SUCCESS('Тестовые данные загружены.'))
        self.stdout.write('Админ: admin@teamfinder.ru / admin12345')
        self.stdout.write(
            'Пользователи: maria@example.com, nikita@example.com, '
            'alex@example.com / testpass123',
        )
