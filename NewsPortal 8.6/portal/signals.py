from django.db.models.signals import post_save
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import EmailMultiAlternatives
from .models import Post, Category, User
from django.template.loader import render_to_string


# в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция,
# и в отправители надо передать также модель
@receiver(post_save, sender=Post)
def notify_new_post(sender, instance, created, **kwargs):
    html_content = render_to_string('mail_created.html',
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
