from django.shortcuts import render,redirect

from django.views import View
from django.db.models import Q
from django.core.paginator import Paginator 


from .models import Topic
from .forms import TopicForm

class IndexView(View):

    def get(self, request, *args, **kwargs):
        context = {}
        query   = Q()

        if "search" in request.GET:

            #全角スペースを半角スペースに変換、半角スペース区切りで文字列のリストに仕立てる。
            #(ex) 『"Django　教科書 入門"』 → 『"Django 教科書 入門"』 → 『["Django","教科書","入門"]』
            words       = request.GET["search"].replace("　"," ").split(" ")

            for word in words:
                query &= Q(comment__contains=word)


        #TIPS: .order_by()で並び替えしないと、paginatorでWARNINGが出る。
        topics      = Topic.objects.filter(query).order_by("id")


        paginator   = Paginator(topics,4)

        # ?page=2 などの指定がある場合
        if "page" in request.GET:
            context["topics"] = paginator.get_page(request.GET["page"])
        else:
            context["topics"] = paginator.get_page(1)


        return render(request,"bbs/index.html",context)

    def post(self, request, *args, **kwargs):


        form    = TopicForm(request.POST)

        if form.is_valid():
            form.save()
        else:
            print(form.errors)

        return redirect("bbs:index")

index   = IndexView.as_view()
