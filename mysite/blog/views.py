from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .models import Post, Comment
from .forms import EmailPostForm, CommentForm
from taggit.models import Tag


class PostListView(ListView):
    """Класс обрабочик"""
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_list(request, tag_slug=None):
    """Обработчик. Запрашивает все данные из БД все статьи"""
    object_list = Post.published.all()

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3)  # По 3 статьи на каждой странице
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # Если страницв не является целым число, возвращаем первую страницу
        posts = paginator.page(1)
    except EmptyPage:
        # Если номер страницы больше, чем общее количество страниц, возвращаем последнюю
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html',
                  {'page': page,
                   'posts': posts,
                   'tag': tag})


def post_detail(request, year, month, day, post):
    """Обработчик страницы статьи"""
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    # Список активных комментариев для статьи
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        # Пользователь отправил комментарий
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Создание комментария, но пока без сохранения в БД
            new_comment = comment_form.save(commit=False)
            # Привязка комментария к текущей статье
            new_comment.post = post
            # Сохранение комментария в БД
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form})


# def post_share(request, post_id):
#     """Получение статьи по id"""
#     post = get_object_or_404(Post, id=post_id, status='published')
#     sent = False
#     if request.method == "POST":
#         form = EmailPostForm(request.Post)
#         if form.is_valid():
#             # Если все поля корректны и прошли валидацию
#             cd = form.cleaned_data
#             # Отправка эл. почты
#             post_url = request.build_absolute_uri(post.get_absolute_url())
#             subject = '{}({}) recommends you reading "{}"'.format(cd['name'], cd['mail'], post.title)
#             message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
#             # name_mail = config_parser.get('main', 'EMAIL_HOST_USER')
#             name_mail = S.EMAIL_HOST_USER
#             send_mail(subject, message, name_mail, [cd['to']])
#             sent = True
#         else:
#             form = EmailPostForm()
#             return render(request, 'blog/post/share.html',
#                           {'post': post, 'form': form, 'sent': sent})
