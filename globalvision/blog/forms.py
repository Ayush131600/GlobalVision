from django import forms
from .models import BlogPost

class BlogPostSubmissionForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'author_name_manual', 'category', 'body', 'cover_image']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter blog title...'}),
            'body': forms.Textarea(attrs={'placeholder': 'Write your blog post here...', 'rows': 8}),
            'category': forms.Select(choices=[
                ('Tech', 'Tech'),
                ('Lifestyle', 'Lifestyle'),
                ('Travel', 'Travel'),
                ('Food', 'Food'),
                ('Other', 'Other')
            ]),
        }

    author_name_manual = forms.CharField(label="Author Name", max_length=150, required=True)

    def save(self, commit=True):
        instance = super().save(commit=False)
        # We can store the manual author name in a note or use the logged in user
        if commit:
            instance.save()
        return instance
