"""Константы."""

NAME_MAX_LENGTH: int = 150
EMAIL_MAX_LENGTH: int = 254
ROLE_MAX_LENGTH: int = 10
ROLE_CHOICES: tuple = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)
