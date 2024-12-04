from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'image', 'image_preview', 'preview', 'status', 'tags']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_title(self):
        title = self.cleaned_data['title']
        if Post.objects.filter(
            title=title,
            author=self.user
        ).exists():
            raise forms.ValidationError('У вас уже есть пост с таким заголовком')
        return title