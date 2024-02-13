from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.urls import reverse_lazy
from votingapp.models import Category, CategoryItem
# from django.http import  HttpResponse
# from django.utils import timezone
# from datetime import timedelta

# Create your views here.
def index(request):
    categories=Category.objects.all()
    context={'categories': categories}
    return render(request, 'mainindex.html', context)

@login_required(login_url='login')
def detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    # category=Category.objects.get(slug=slug)
    categories=CategoryItem.objects.filter(category=category)

    msg= None

    if request.user.is_authenticated:
            if category.voters.filter(id=request.user.id).exists():
                msg="voted"

    if request.method == "POST":
        selected_id = request.POST.get("category_item")
        print(selected_id)
        item=CategoryItem.objects.get(id=selected_id)
        item.total_score += 1
        
        item_category = item.category
        item_category.total_score += 1

        item.voters.add(request.user)
        item_category.voters.add(request.user)

        item.save()
        item_category.save()
        

        return redirect("result", slug=category.slug)

    context={'categories':categories, 'category':category, 'msg': msg}
    return render(request, 'detail.html', context)

def result(request, slug):
    category= get_object_or_404(Category, slug=slug)
    items= CategoryItem.objects.filter(category=category)
    context = {"category":category, "items":items}
    return render(request, 'result.html', context)

def overallresult(request):
    items= CategoryItem.objects.all()
    total_votes_category = items.aggregate(Sum('total_score'))['total_score__sum'] or 0
    context={"items":items, "total_votes_category":total_votes_category}
    return render(request, 'overallresult.html', context)

def Manifesto(request, id):
    manifesto=CategoryItem.objects.get(id=id)
    context={"manifesto":manifesto}
    return render(request, 'manifesto.html', context)