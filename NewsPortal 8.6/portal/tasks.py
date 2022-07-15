from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from .models import Post, Category, User
from django.template.loader import render_to_string
import time

import logging
logger = logging.getLogger(__name__)


@shared_task
def action_every_monday_8am():
    html_content = render_to_string('mail_weekend.html',
                                    {'title': Post.objects.name(),
                                     'post': Post.objects.text[50:](),
                                     'link': Post.get_absolute_url()
                                     }
                                    )
    msg = EmailMultiAlternatives(
        subject=f'New post in {Category.name}{Post.name}',
        body=f'{Post.text[50:]}',
        from_email='AndreySkillF2@yandex.ru',
        to=['ter_ah@mail.ru', User.objects.all(pk=Category.objects.subscribers.get()).email]
    )
    msg.attach_alternative(html_content, "text/html")  # добавляем html

    msg.send()

