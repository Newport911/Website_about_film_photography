# Django core
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.text import slugify

# Django views
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView
)
from django.contrib.auth.mixins import LoginRequiredMixin

# Third party
from taggit.models import Tag

# Local
from .forms import PostForm
from .models import Post


class PostListView(ListView):
    """
    Представление для отображения списка постов с фильтрацией по тегам и пагинацией

    Атрибуты:
        model (Post): Модель для получения данных
        template_name (str): Путь к шаблону index.html
        context_object_name (str): Имя переменной списка постов в шаблоне
        paginate_by (int): Количество постов на странице
    """
    model = Post
    template_name = 'filmblog/index.html'
    context_object_name = 'page_obj'
    paginate_by = 8

    def get_queryset(self):
        """
        Возвращает отфильтрованный QuerySet постов

        Returns:
            QuerySet: Опубликованные посты, отфильтрованные по тегу (если указан),
                     с предзагруженными данными автора и тегов
        """
        queryset = Post.published.all()
        tag_slug = self.kwargs.get('tag_slug')

        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            queryset = queryset.filter(tags__in=[tag])

        return queryset.select_related('author').prefetch_related('tags')

    def get_context_data(self, **kwargs):
        """
        Расширяет контекст шаблона дополнительными данными

        Args:
            **kwargs: Дополнительные именованные аргументы

        Returns:
            dict: Контекст с дополнительными данными:
                - page_obj: Пагинированный список постов
                - tag: Текущий тег (если указан)
                - articles: Посты с указанным тегом
        """
        context = super().get_context_data(**kwargs)
        tag_slug = self.kwargs.get('tag_slug')

        if tag_slug:
            context['tag'] = get_object_or_404(Tag, slug=tag_slug)

        context['articles'] = Post.objects.filter(
            tags__name=context.get('tag')
        ).distinct() if context.get('tag') else None

        return context


class PostDetailView(DetailView):
    """
    Представление для отображения детальной информации о посте

    Атрибуты:
        model (Post): Модель поста
        template_name (str): Путь к шаблону детального просмотра
        context_object_name (str): Имя переменной поста в шаблоне
    """
    model = Post
    template_name = 'filmblog/single-standard.html'
    context_object_name = 'post'

    def get_object(self):
        """
        Получает конкретный пост по параметрам URL

        Returns:
            Post: Опубликованный пост с указанными параметрами или 404

        Raises:
            Http404: Если пост не найден
        """
        return get_object_or_404(
            Post,
            slug=self.kwargs['post'],
            status='published',
            publish__year=self.kwargs['year'],
            publish__month=self.kwargs['month'],
            publish__day=self.kwargs['day']
        )

    def get_context_data(self, **kwargs):
        """
        Расширяет контекст шаблона навигационными данными

        Args:
            **kwargs: Дополнительные именованные аргументы

        Returns:
            dict: Контекст с дополнительными данными:
                - post: Текущий пост
                - prev_post: Предыдущий пост
                - next_post: Следующий пост
        """
        context = super().get_context_data(**kwargs)
        post = self.get_object()

        context.update({
            'prev_post': self._get_adjacent_post(post, is_next=False),
            'next_post': self._get_adjacent_post(post, is_next=True)
        })

        return context

    def _get_adjacent_post(self, post, is_next=True):
        """
        Получает следующий или предыдущий пост относительно текущего

        Args:
            post (Post): Текущий пост
            is_next (bool): True для следующего, False для предыдущего

        Returns:
            Post|None: Соседний опубликованный пост или None если не существует
        """
        try:
            if is_next:
                return post.get_next_by_publish(status='published')
            return post.get_previous_by_publish(status='published')
        except Post.DoesNotExist:
            return None

class SearchResultsView(ListView):
    """
    Представление для поиска постов по заголовку

    Атрибуты:
        model (Post): Модель для поиска
        template_name (str): Путь к шаблону результатов
        context_object_name (str): Имя переменной с результатами в контексте
        paginate_by (int): Количество результатов на странице
    """
    model = Post
    template_name = 'filmblog/search_results.html'
    context_object_name = 'results'
    paginate_by = 8

    def get_queryset(self):
        """
        Возвращает отфильтрованный QuerySet на основе поискового запроса

        Returns:
            QuerySet: Отфильтрованные посты или пустой QuerySet
        """
        query = self.request.GET.get('query', '')
        if query:
            return Post.objects.filter(
                Q(title__icontains=query) |
                Q(body__icontains=query) |
                Q(preview__icontains=query)
            ).select_related('author').prefetch_related('tags')
        return Post.objects.none()

    def get_context_data(self, **kwargs):
        """
        Добавляет поисковый запрос в контекст шаблона
        """
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('query', '')
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """
    Представление для создания новых постов

    Атрибуты:
        model (Post): Модель поста
        template_name (str): Путь к шаблону создания
        form_class (PostForm): Форма для создания поста
        success_url (str): URL для перенаправления после успешного создания
    """
    model = Post
    template_name = 'filmblog/post_create.html'
    form_class = PostForm
    success_url = reverse_lazy('filmblog:index')

    def get_form_kwargs(self):
        """Передает дополнительные аргументы в форму"""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        """
        Обработка валидной формы

        Args:
            form: Валидированная форма

        Returns:
            HttpResponse: Ответ с перенаправлением
        """
        form.instance.author = self.request.user
        form.instance.original_author = self.request.user.username
        form.instance.slug = slugify(form.cleaned_data['title'])

        return super().form_valid(form)


    def get_success_url(self):
        """Получает URL для перенаправления после создания поста"""
        return self.object.get_absolute_url()


class PostManageView(LoginRequiredMixin, ListView):
    """
    Представление для управления постами

    Атрибуты:
        model (Post): Модель поста
        template_name (str): Путь к шаблону управления постами
        context_object_name (str): Имя переменной списка постов в контексте
        paginate_by (int): Количество постов на странице
    """
    model = Post
    template_name = 'filmblog/post_manage.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        """
        Получает отсортированный и оптимизированный QuerySet постов

        Returns:
            QuerySet: Посты с предзагруженными связанными данными
        """
        return Post.objects.select_related('author') \
            .prefetch_related('tags') \
            .order_by('-created')

    def get_context_data(self, **kwargs):
        """Добавляет дополнительный контекст"""
        context = super().get_context_data(**kwargs)
        context.update({
            'total_posts': Post.objects.count(),
            'published_posts': Post.published.count(),
            'draft_posts': Post.objects.filter(status='draft').count()
        })
        return context

    def get_queryset_by_status(self, status):
        """
        Фильтрует посты по статусу

        Args:
            status (str): Статус постов ('published' или 'draft')
        """
        queryset = self.get_queryset()
        return queryset.filter(status=status)


class PostEditView(LoginRequiredMixin, UpdateView):
    """
    Представление для редактирования постов

    Атрибуты:
        model (Post): Модель поста
        template_name (str): Путь к шаблону редактирования
        form_class (PostForm): Форма для редактирования поста
    """
    model = Post
    template_name = 'filmblog/post_edit.html'
    form_class = PostForm

    def get_form_kwargs(self):
        """Передает дополнительные аргументы в форму"""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        """
        Обработка валидной формы

        Args:
            form: Валидированная форма

        Returns:
            HttpResponse: Ответ с перенаправлением
        """
        if form.has_changed():
            form.instance.updated = timezone.now()
            form.instance.slug = slugify(form.cleaned_data['title'])
        return super().form_valid(form)

    def get_queryset(self):
        """Оптимизация запросов к БД"""
        return Post.objects.select_related('author').prefetch_related('tags')

    def get_success_url(self):
        """URL для перенаправления после успешного редактирования"""
        messages.success(self.request, 'Пост успешно обновлен')
        return reverse_lazy('filmblog:post_manage')

    def dispatch(self, request, *args, **kwargs):
        """Проверка прав доступа к редактированию"""
        obj = self.get_object()
        if obj.author != request.user:
            messages.error(request, 'У вас нет прав для редактирования этого поста')
            return redirect('filmblog:post_manage')
        return super().dispatch(request, *args, **kwargs)

from django.views.generic.edit import DeleteView


class PostDeleteView(LoginRequiredMixin, DeleteView):
    """
    Представление для удаления постов

    Атрибуты:
        model (Post): Модель поста
        template_name (str): Путь к шаблону подтверждения удаления
    """
    model = Post
    template_name = 'filmblog/post_confirm_delete.html'

    def get_queryset(self):
        """Оптимизация запросов к БД"""
        return Post.objects.select_related('author')

    def get_success_url(self):
        """URL для перенаправления после успешного удаления"""
        messages.success(self.request, 'Пост успешно удален')
        return reverse_lazy('filmblog:post_manage')

    def dispatch(self, request, *args, **kwargs):
        """Проверка прав доступа к удалению"""
        obj = self.get_object()
        if obj.author != request.user:
            messages.error(request, 'У вас нет прав для удаления этого поста')
            return redirect('filmblog:post_manage')
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        Переопределение метода удаления для сохранения файлов
        """
        obj = self.get_object()

        # Удаление связанных изображений
        if obj.image:
            obj.image.delete(save=False)
        if obj.image_preview:
            obj.image_preview.delete(save=False)

        return super().delete(request, *args, **kwargs)