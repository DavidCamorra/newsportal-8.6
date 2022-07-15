from django.forms import ModelForm, BooleanField
from .models import Post, Author
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


# Создаём модельную форму
class PostForm(ModelForm):
    # check_box = BooleanField(label='Алло, Галочка!')
    class Meta:
        model = Post
        fields = ['name', 'type', 'category', 'text', 'post_auth']


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        Author.objects.create(user=user)
        return user
