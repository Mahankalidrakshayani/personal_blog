from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Category, Tag, Comment, Profile
from django.utils.text import slugify


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        if 'password' in self.fields:
            self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        for field in self.fields.values():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email address already exists.")
        return email


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['headline', 'bio', 'avatar', 'website', 'github', 'twitter', 'linkedin']
        widgets = {
            'headline': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Senior Software Engineer'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Tell readers about yourself...'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://yourwebsite.com'}),
            'github': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://github.com/username'}),
            'twitter': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://x.com/username'}),
            'linkedin': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://linkedin.com/in/username'}),
        }


class PostForm(forms.ModelForm):
    tag_input = forms.CharField(
        required=False,
        label="Tags",
        help_text="Separate tags with commas (e.g., Python, Web Development, Design)",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'python, django, backend, tutorial'
        })
    )

    class Meta:
        model = Post
        fields = ['title', 'category', 'summary', 'content', 'featured_image', 'status', 'is_featured']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Enter an engaging blog post title...'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'summary': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Brief summary or teaser (optional; automatically generated if left blank)...'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control code-editor',
                'rows': 14,
                'placeholder': 'Write your blog post content here... You can use standard paragraphs or HTML tags.'
            }),
            'featured_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Prepopulate tag_input from existing tags
            existing_tags = self.instance.tags.all()
            self.fields['tag_input'].initial = ", ".join([t.name for t in existing_tags])

    def save(self, commit=True, author=None):
        instance = super().save(commit=False)
        if author:
            instance.author = author
        if commit:
            instance.save()
            # Handle tags
            raw_tags = self.cleaned_data.get('tag_input', '')
            tag_names = [t.strip().strip('#') for t in raw_tags.split(',') if t.strip()]
            tag_objects = []
            for name in tag_names:
                tag, _ = Tag.objects.get_or_create(
                    name=name,
                    defaults={'slug': slugify(name)}
                )
                tag_objects.append(tag)
            instance.tags.set(tag_objects)
            self.save_m2m()
        return instance


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write a respectful and constructive comment...',
                'maxlength': '1000'
            })
        }
        labels = {
            'content': ''
        }
