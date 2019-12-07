

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .models import Post
from .forms import EmailPostForm


class PostListView(ListView):
    """Класс обрабочик"""
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_list(request):
    """Обработчик. Запрашивает все данные из БД все статьи"""
    object_list = Post.published.all()
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
                   'posts': posts})


def post_detail(request, year, month, day, post):
    """Обработчик страницы статьи"""
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request,
                  'blog/post/detail.html',
                  {'post': post})


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
#             send_mail(subject, message, name_mail, [cd['to']])
#             sent = True
#         else:
#             form = EmailPostForm()
#             return render(request, 'blog/post/share.html',
#                           {'post': post, 'form': form, 'sent': sent})
