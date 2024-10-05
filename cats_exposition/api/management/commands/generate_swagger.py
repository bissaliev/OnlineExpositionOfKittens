from django.core.management.base import BaseCommand
from drf_yasg.management.commands import generate_swagger


class Command(BaseCommand):
    help = "Генерация статической документации Swagger"

    def handle(self, *args, **kwargs):
        # Укажите формат документации: openapi (json) или swagger (yaml)
        format = "yaml"  # или 'yaml'

        # Путь к файлу, куда будет сохранена документация
        output_file = f"../docs/swagger.{format}"

        # Выполняем команду генерации документации
        generate_swagger.Command().handle(
            output_file=output_file,
            format=format,
            api_url="http://localhost:8000",  # Укажите базовый URL вашего API
            overwrite=True,  # Перезаписать файл, если он уже существует
            mock=False,  # Не использовать mock данные
            api_version="1.0",  # Версия API
            user=None,  # Пользователь не задан
            private=False,  # Сделать документацию публичной
            generator_class_name=None,  # Использовать стандартный генератор
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Документация сгенерирована и сохранена в {output_file}"
            )
        )
