import re

text = "Хуй Жопович Еблан"
name = re.search(r'^([А-Я]{1}[а-яё]{1,23})\s([А-Я]{1}[а-яё]{1,23})\s([А-Я]{1}[а-яё]{1,23})$', text).group(0)
print(type(name))