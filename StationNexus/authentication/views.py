from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from django.shortcuts import redirect, render
from django.views.generic import View


class Login_View(View):
    def get(self, request, *args, **kwargs):
        form = AuthenticationForm()
        return render(request, "login.html", {"form": form})

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
        else:
            return redirect("login")

        if "next" in request.GET.keys():
            return redirect(request.GET["next"])
        else:
            return redirect("status")


class Logout_View(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("login")


class Debug_View(View):
    def get(self, request, *args, **kwargs):
        query_set = Group.objects.all()
        groups = []
        for g in query_set:
            groups.append(g.name)

        context = {"all_groups": groups}
        return render(request, "debug.html", context)
