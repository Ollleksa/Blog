from django.shortcuts import render
from django.template import loader
from django.http import Http404, HttpResponse, HttpResponseRedirect

from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string

from .models import Blog, Message, Comment
from .forms import NewComment, NewMessage, NewBlog


def check_auth(func):
    """
    Decorator for checking if user are authenticated, and verify it account by email
    :param func: view function
    :return: Normal page, or page with error message.
    """
    def wrapper(request, **kwargs):
        user = request.user
        if not user.is_authenticated:
            template = loader.get_template('registration/auth_problems.html')
            return HttpResponse(template.render({'is_login': True, }, request))
        elif not user.is_verified:
            template = loader.get_template('registration/auth_problems.html')
            return HttpResponse(template.render({'is_login': False, 'email': user.email, }, request))
        else:
            return func(request, **kwargs)
    return wrapper


@check_auth
def home(request):

    message_list = Message.objects.all().order_by('-timestamp')

    context = {
        'message_list': message_list,
    }

    template = loader.get_template('home.html')

    return HttpResponse(template.render(context, request))


@check_auth
def blog(request, blog_id):

    try:
        blog = Blog.objects.get(pk=blog_id)
    except Blog.DoesNotExist:
        raise Http404("Blog does not exist.")

    message_list = Message.objects.filter(blog=blog).order_by('-timestamp')

    context = {
        'blog': blog,
        'message_list': message_list,
    }

    template = loader.get_template('blog.html')

    return HttpResponse(template.render(context, request))


@check_auth
def message(request, message_id):

    try:
        mess = Message.objects.get(pk=message_id)
    except Message.DoesNotExist:
        raise Http404("Entry does not exist.")

    comment_list = Comment.objects.filter(message=mess).order_by('timestamp')

    if request.method == 'POST':
        form = NewComment(request.POST)
        if form.is_valid():
            new_com = Comment(message=mess, content=form.cleaned_data['content'], user=request.user)
            new_com.save()
            sent_email_comment(request, mess, new_com)
            return HttpResponseRedirect(request.path_info)
    else:
        form = NewComment()

    context = {
        'form': form,
        'message': mess,
        'comment_list': comment_list,
    }

    template = loader.get_template('message.html')

    return HttpResponse(template.render(context, request))


@check_auth
def create(request):

    current_user = request.user

    try:
        user_blog = Blog.objects.get(user=current_user)
    except Blog.DoesNotExist:
        return HttpResponseRedirect('../create_blog')

    if request.method == 'POST':
        form = NewMessage(request.POST)
        if form.is_valid():
            mess = Message(name=form.cleaned_data['name'], content=form.cleaned_data['content'], blog=user_blog)
            mess.save()
            return HttpResponseRedirect('../message/{}'.format(mess.pk))
    else:
        form = NewMessage()

    template = loader.get_template('create_message.html')
    context = {
        'form': form,
        'blog': user_blog,
    }
    return HttpResponse(template.render(context, request))


@check_auth
def create_blog(request):

    if request.method == 'POST':
        form = NewBlog(request.POST)
        if form.is_valid():
            new_blog = Blog(name=form.cleaned_data['name'], user=request.user)
            new_blog.save()
            return HttpResponseRedirect('blog/create_message')
    else:
        form = NewBlog()

    template = loader.get_template('create_blog.html')
    context = {
        'form': form,
        'user': request.user,
    }
    return HttpResponse(template.render(context, request))


def sent_email_comment(request, mess, comment):
    """
    Send email about comment to user
    :param request: request on creation of commment
    :param mess: message which is commented
    :param comment: comment
    :return if user comment its own message - sent nothing
    """
    if mess.blog.user == request.user:
        return None

    current_site = get_current_site(request)
    mail_subject = 'New Comment on {}'.format(mess.name)
    context = {
        'user': mess.blog.user,
        'domain': current_site.domain,
        'comment': comment
    }
    message = render_to_string('comment_email.html', context)

    to_email = mess.blog.user.email
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()
