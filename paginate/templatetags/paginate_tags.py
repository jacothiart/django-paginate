from django import template
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

register = template.Library()

@register.simple_tag(takes_context=True)
def paginate(context, object_list):
    page_count = getattr(
            settings,
            'PAGINATE_PAGE_COUNT',
            5)
    
    page_left = getattr(
            settings,
            'PAGINATE_PAGE_LEFT',
            3) + 1
    
    page_right = getattr(
            settings,
            'PAGINATE_PAGE_RIGHT',
            3) + 1
    
    paginator = Paginator(object_list, page_count)
    
    page = context['request'].GET.get('page')        
    pages = []
    
    try:
        object_list = paginator.page(page)
        context['current_page'] = int(page)
        pages = get_left(context['current_page'], page_left) + get_right(context['current_page'], page_right, paginator.num_pages)
    except PageNotAnInteger:
        object_list = paginator.page(1)
        context['current_page'] = 1
        pages = get_right(context['current_page'], page_right, paginator.num_pages)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)
        context['current_page'] = paginator.num_pages
        pages = get_left(context['current_page'], page_left)
        
    context['object_list'] = object_list
    context['paginator'] = paginator
    context['pages'] = pages
    
    return ''

def get_left(current_page, page_left):
    l = [current_page - i for i in range(page_left) if (current_page - i) > 0 and (current_page - i) < current_page]
    l.sort()
    return l
    
def get_right(current_page, page_right, num_pages):
    return [i for i in range(current_page + page_right) if i >= current_page and i <= num_pages]