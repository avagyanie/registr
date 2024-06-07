from typing import Any, Dict
from django.shortcuts import render, redirect
from .models import *
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from .forms import NewsForm, MessageForm, NewsCommentForm, SubscriberForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters.views import FilterView
from .filters import NewsFilter
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.db.models import Q
from django.core.mail import send_mail
from datetime import datetime


# Create your views here.
User = get_user_model()


def about(request):
    team = Team.objects.all()
    team_members = TeamMember.objects.all()
    info = Info.objects.all()
    return render(request=request, template_name="about.html", context={"team": team,
                                                                        "team_members": team_members,
                                                                        "info": info,
}) 


class Base(LoginRequiredMixin, CreateView):
    def get_queryset(self):
        queryset = super(Base, self).get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


class NewsBase(Base):
    model = News
    context_object_name = "news"
    form_class = NewsForm
    success_url = reverse_lazy("my_news")
    success_text = ""
    
    def form_valid(self, form):
        messages.success(self.request, self.success_text)
        return super().form_valid(form)


class CreateNewsComment(CreateView):
    model = NewsComment
    form_class = NewsCommentForm

    def get_success_url(self)-> str:
        return reverse_lazy("news_details", kwargs = {"pk": self.request.POST.get("news")})

    def form_valid(self, form):
        form.instance.owner = self.request.user
        news_id = self.request.POST.get("news")
        news = get_object_or_404(News, id = news_id)
        form.instance.news = news
        return super().form_valid(form)


class CreateNews(NewsBase):
    template_name = "create_news.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Your new post has been completed.")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        info_instance = Info.objects.all()
        context['info'] = info_instance 
        return context


class MyNews(NewsBase, FilterView):
    template_name = "core/news_list.html"
    filterset_class = NewsFilter
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        info_instance = Info.objects.all()
        context['info'] = info_instance 
        return context


class MyNewsDetail(NewsBase, DetailView):
   
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        data = super().get_context_data(**kwargs)
        info_instance = Info.objects.all()
        data['info'] = info_instance 
        data["comment_form"] = NewsCommentForm
        data["comments"] = NewsComment.objects.filter(news=data["news"])
        return data
    
    def get(self, request: HttpRequest, *args, **kwargs):
         self.object = self.get_object()
         self.object.view_count += 1
         self.object.save()
         context = self.get_context_data(object=self.object)
         return self.render_to_response(context)


class NewsDetails(DetailView):
    model = News
    context_object_name = "news"
    template_name = "news-detail.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        comment_form = NewsCommentForm()
        data['comment_form'] = NewsCommentForm
        data['comments'] = NewsComment.objects.filter(news=data["news"])
        info_instance = Info.objects.all()
        data['info'] = info_instance
        return data
    

    def get(self, request: HttpRequest, *args, **kwargs):
        self.object = self.get_object()
        self.object.view_count += 1
        self.object.save()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)



class MyNewsUpdate(NewsBase, UpdateView):
    success_text = "News instance is updated!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        info_instance = Info.objects.all()
        context['info'] = info_instance
        return context


class MyNewsDelete(LoginRequiredMixin, DeleteView):
    model = News
    context_object_name = "news"
    success_url = reverse_lazy("my_news")

    def get_queryset(self):
        queryset = super(MyNewsDelete, self).get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset

    def form_valid(self, form):
        messages.info(self.request, "News instance is deleted!")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        info_instance = Info.objects.all()
        context['info'] = info_instance
        return context


def single_post(request):
    news = News.objects.all()
    return render(request, "single-post.html", context={"news": news})

    
class Filter(LoginRequiredMixin, FilterView):
    template_name = "core/all_news.html"
    filterset_class = NewsFilter
    paginate_by = 3

    def get_queryset(self):
        queryset = super(Filter, self).get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


class Filters(FilterView):
    model = News
    context_object_name = "news"
    filterset_class = NewsFilter

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        most_viewed_news = News.objects.order_by('-view_count')[:5]
        newest_news=News.objects.order_by('-date')[:5]
        context['most_viewed_news'] = most_viewed_news
        context['newest_news'] = newest_news
        return context


class Home(Filters):
    template_name = "index.html"
    paginate_by = 9

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super(Home, self).get_queryset()
        return queryset.order_by('-date')

    def post(self, request, *args, **kwargs):
        messageForm = MessageForm(request.POST)
        if messageForm.is_valid():
            messageForm.save()
            messages.success(request, "Your Message has been sent!")
        return redirect("{% url 'home'%}")
    
    def get_context_data(self, **kwargs):
        info_instance = Info.objects.all()
        context = super().get_context_data(**kwargs)
        context['info'] = info_instance
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
        return context


def category(request):
    news = News.objects.all()
    return render(request, "category.html", context={"news": news})


class ContacView(Home):
    template_name = "contact.html"
    
    def get_context_data(self, **kwargs):
        contact_instances = Contact.objects.all()
        
        context = super().get_context_data(**kwargs)
        context['contact'] = contact_instances
        return context


def search_result(request):
    query = request.GET.get('search')
    news_filter = NewsFilter(request.GET, queryset=News.objects.all())
    info = Info.objects.all()

    context = {
        'query': query,
        'news_filter': news_filter,
        'info': info,
    }

    if query:
        news_filter_qs = news_filter.qs.filter(Q(title__icontains=query) | Q(description__icontains=query))
        context['news_filter'] = news_filter_qs

    return render(request, 'search-result.html', context)


def search_suggestions(request):
    search_query = request.GET.get('q', '')

    news = News.objects.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))

    suggestions = [{'title': news.title, 'description': news.description}
                   for news in news]

    return JsonResponse(suggestions, safe=False)


def subscribe(request):
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            try:
                subscriber = form.save()
                send_mail(
                    'Welcome to Our Newsletter',
                    'Thank you for subscribing!',
                    'infopulse.newsapp@gmail.com',
                    [subscriber.email],
                    fail_silently=False,
                )
                messages.success(request, 'Thank you for subscribing to our newsletter. You will receive our latest updates in your inbox.')
                return redirect('home')
            except Exception as e:
                messages.warning(request, 'An error occurred while sending the confirmation email. Please try again later.')
                return redirect('home')
        else:
            messages.warning(request, 'Please provide a valid email address.')
            return redirect('home')
    else:
        form = SubscriberForm()
        return redirect('home')


def subscribe_success(request):
    return render(request, 'index.html')
