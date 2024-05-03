from django import forms

from socialblog.models import Blog, Comment

class LoginForm(forms.Form):
    username = forms.CharField(label="Имя пользователя")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["username"].widget.attrs["id"] = "usernameInput"
        # Это сделано для красивой анимации
        self.fields["username"].widget.attrs["placeholder"] = ""
        self.fields["password"].widget.attrs["class"] = "form-control"
        self.fields["password"].widget.attrs["id"] = "passwordInput"
        # Это сделано для красивой анимации
        self.fields["password"].widget.attrs["placeholder"] = ""
class BlogForm(forms.Form):
    title = forms.CharField(label="Заголовок", min_length=3, max_length=100)
    text = forms.CharField(label="Текст", widget=forms.Textarea, min_length=10, max_length=500)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields["title"].widget.attrs["class"] = "form-control"
        self.fields["title"].widget.attrs["id"] = "titleInput"
        self.fields["text"].widget.attrs["class"] = "form-control"
        self.fields["text"].widget.attrs["id"] = "textInput"
        self.fields["text"].widget.attrs["rows"] = 5

    def save(self, user):
        if self.is_valid():
            Blog(
                author=user,
                title=self.cleaned_data.get("title"),
                text=self.cleaned_data.get("text"),
            ).save()
            
class CommentForm(forms.Form):
    text = forms.CharField(max_length=100)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["text"].widget.attrs["class"] = "form-control"
        
    def save(self, blog):
        if self.is_valid():
            Comment(
                blog=blog,
                text=self.cleaned_data.get("text"),
            ).save()