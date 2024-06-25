from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.template.response import TemplateResponse
from .models import BlogPage


def index(request):
    tag = request.GET.get('tag')
    if tag:
        blog_posts = BlogPage.objects.live().public().filter(tags__name=tag).order_by('-date')
    else:
        blog_posts = BlogPage.objects.live().public().order_by('-date')
    
    paginator = Paginator(blog_posts, 5)
    page_number = request.GET.get('page')

    try:
        blog_posts_paginated = paginator.page(page_number)
    except PageNotAnInteger:
        blog_posts_paginated = paginator.page(1)
    except EmptyPage:
        blog_posts_paginated = paginator.page(paginator.num_pages)
# could also use render() from django.shortcuts
    return TemplateResponse(
        request,
        "blog/index_page.html",
        {
            "blog_posts": blog_posts_paginated,
        },
    )