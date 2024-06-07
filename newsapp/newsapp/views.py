from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import logout
from django.shortcuts import redirect


# Create your views here.

# def home(request):
    # if request.user.is_authenticated:
    #     return HttpResponse(f"Home page for {request.user.email}")
    # return HttpResponse("You are not loged user!")
    # return render(request=request, template_name="index.html", context={})


# def logout_view(request):
#     logout(request)
#     return redirect("{% url 'home'%}")
