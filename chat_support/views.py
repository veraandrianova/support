from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordContextMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views import View
from django.views.generic import CreateView, FormView, ListView, TemplateView, DetailView
from django.views.generic.edit import FormMixin
from rest_framework import generics

from chat_support.forms import RegisterUserForm, Auntification, RatingForm
from chat_support.models import ChatMessage, ChatDialog, User
from chat_support.serializers import ChatMessageSerializer


def login_out(reguest):
    logout(reguest)
    return redirect('title')

# титульная страница авторизации

class LoginViewList(LoginView):
    form_class = Auntification
    template_name = 'chat/number.html'

    def get_success_url(self):
        user = self.request.POST.get('username')
        print(user)
        return reverse('index', kwargs={'room_name': user})


# регистрация
class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'chat/register.html'
    success_url = reverse_lazy('title')

# забыли свой пароль

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'chat/password_reset.html'
    success_url = 'password_reset_confirm'


class PasswordResetConfirmView(PasswordContextMixin, FormView):
    template_name = 'chat/password_reset_confirm.html'
    success_url = 'title'

# класс личного кабинета
class PersonalArea(FormMixin, ListView):
    model = ChatMessage
    template_name = 'chat/index.html'
    context_object_name = "messages"
    form_class = RatingForm
# забираем контекст
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         print(f'{context} ok')
#         context['user'] = self.kwargs['room_name']
#         return context
# формируем сообщения для оценки
    def get_queryset(self):
        return ChatMessage.objects.filter(author=self.request.user).order_by("-create_at")

    def get_success_url(self):
        pk = self.kwargs['room_name']
        return reverse('index', kwargs={'room_name': pk})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        return self.form_valid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        print(self.object)
        print(form.cleaned_data)
        self.object.star_1 = form.cleaned_data['star_1']
        self.object.star_2 = form.cleaned_data['star_2']
        self.object.comment = form.cleaned_data['comment']
        print(self.object.star_1)
        print(self.object.message)
        self.object.rated_by = self.request.user
        print(self.object.rated_by)
        # self.object.save()
        return super().form_valid(form)

# класс комнаты
class PersonalRoom(DetailView):
    model = ChatDialog
    template_name = 'chat/room.html'
    pk_url_kwarg = 'room_name'
# получаем контекст
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['last_message'] = ChatMessage.objects.filter(dialog=self.get_object()).last()
        return context



class ChatDialogCreateApiView(generics.CreateAPIView):
    queryset = ChatDialog.objects.all()
    serializer_class = ChatMessageSerializer

    def perform_create(self, serializer):
        chat_dialog = ChatDialog.objects.create()
        serializer.save(author=self.request.user, dialog=chat_dialog)
        # body = serializer.data['body']
        # ChatMessage.objects.create(body=body, author=self.request.user, dialog=chat_dialog)
        # send_telegram(serializer.data['message'], serializer.data['number'])


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            mail = password_reset_form.cleaned_data['email']
            user = User.objects.get(email=mail)  # email в форме регистрации проверен на уникальность
            subject = 'Запрошен сброс пароля'
            email_template_name = "chat/email_password_reset.html"
            cont = {
                "email": user.email,
                'domain': '127.0.0.1:8000',  # доменное имя сайта
                'site_name': 'Website',  # название своего сайта
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),  # шифруем идентификатор
                "user": user,  # чтобы обратиться в письме по логину пользователя
                'token': default_token_generator.make_token(user),  # генерируем токен
                'protocol': 'http',
            }
            msg_html = render_to_string(email_template_name, cont)

            return redirect("/password_reset/done/")
    else:
        password_reset_form = PasswordResetForm()
    return render(request=request, template_name="chat/password_reset.html",
                  context={"password_reset_form": password_reset_form})
