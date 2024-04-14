from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.template.response import TemplateResponse
from .models import BlogPage


def blog_index(request):
    blog_posts = BlogPage.objects.live().public().order_by('-date')
    paginator = Paginator(blog_posts, 2)
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
        "blog/blog_index_page.html",
        {
            "blog_posts": blog_posts_paginated,
        },
    )



#    vindex = request.GET.get("query", Nonejkj)
#    page = request.GET.get("page", 1)
#
#    # Search
#    if search_query:
#        search_results = Page.objects.live().search(search_query)
#
#        # To log this query for use with the "Promoted search results" module:
#
#        # query = Query.get(search_query)
#        # query.add_hit()
#
#    else:
#        search_results = Page.objects.none()
#
#    # Pagination
#    paginator = Paginator(search_results, 10)
#    try:
#        search_results = paginator.page(page)
#    except PageNotAnInteger:
#        search_results = paginator.page(1)
#    except EmptyPage:
#        search_results = paginator.page(paginator.num_pages)
#
#    return TemplateResponse(
#        request,
#        "search/search.html",
#        {
#            "search_query": search_query,
#            "search_results": search_results,
#        },
#    )
#