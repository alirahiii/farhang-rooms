from django import forms

from .models import Comment, WorkRequest


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author_name', 'body']
        labels = {
            'author_name': 'نام',
            'body': 'متن نظر',
        }
        widgets = {
            'author_name': forms.TextInput(attrs={
                'class': 'w-full border rounded-lg px-3 py-2',
                'placeholder': 'نام شما (اختیاری)',
            }),
            'body': forms.Textarea(attrs={
                'class': 'w-full border rounded-lg px-3 py-2',
                'rows': 4,
                'placeholder': 'نظر خود را بنویسید',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author_name'].required = False

    def clean_author_name(self):
        return self.cleaned_data.get('author_name', '').strip() or 'ناشناس'


class WorkRequestForm(forms.ModelForm):
    class Meta:
        model = WorkRequest
        fields = ['title', 'creator', 'category', 'description']
        labels = {
            'title': 'نام اثر',
            'creator': 'نام پدیدآورنده',
            'category': 'دسته‌بندی',
            'description': 'توضیح (اختیاری)',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full border rounded-lg px-3 py-2'}),
            'creator': forms.TextInput(attrs={'class': 'w-full border rounded-lg px-3 py-2'}),
            'category': forms.Select(attrs={'class': 'w-full border rounded-lg px-3 py-2'}),
            'description': forms.Textarea(attrs={'class': 'w-full border rounded-lg px-3 py-2', 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'انتخاب کنید'
