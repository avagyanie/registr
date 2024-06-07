from django import forms
from .models import News, Message, NewsComment, Subscriber


class NewsForm(forms.ModelForm):
    NEWS_TYPES = (
        ("1", "Political"),
        ("2", "Business"),
        ("3", "International"),
        ("4","National"),
        ("5","Lifestyle"),
        ("6", "Sport"),
        ("7", "Cultural"),
        ("8", "Crime")
    )

    title = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    description = forms.CharField(label="", widget=forms.Textarea(attrs={'placeholder': 'News Description'}))
    news_type = forms.ChoiceField(label="", choices=NEWS_TYPES, widget=forms.Select())
    image = forms.ImageField(label="")
    
    class Meta:
        model = News

        fields = ["title", "description", "news_type", 'image']


class MessageForm(forms.ModelForm):
    full_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)
    subject = forms.CharField(max_length=100, required=True)
    message = forms.CharField(max_length=1000, required=True)

    class Meta:
        model = Message
        exclude = ()


class NewsCommentForm(forms.ModelForm):
    text = forms.Textarea()

    class Meta:
        model = NewsComment
        fields = ["text"]


class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']
