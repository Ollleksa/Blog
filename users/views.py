from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site

from .forms import BlogUserCreationForm
from .models import BlogUser
from .cts import account_activation_token

def signup(request):
    if request.method == 'POST':
        form = BlogUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Activate your account'
            context = {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            }
            message = render_to_string('registration/activation_email.html', context)

            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return HttpResponse('Check your email for confirmation letter.')
    else:
        form = BlogUserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = BlogUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, BlogUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_verified = True
        user.save()
        login(request, user)
        # return redirect('home')
        return render(request, 'registration/success_activation.html')
    else:
        return HttpResponse('Activation link is invalid!')


def activation_needed(request):
    return render(request, 'registration/activation_needed.html')