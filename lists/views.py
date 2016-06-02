# Third party
from django.core.exceptions import ValidationError
from django.shortcuts import (
    redirect,
    render,
)

from lists.models import (
    Item,
    List,
)


def home_page(request):
    return render(request, 'lists/home.html')


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    error = ''

    if request.method == 'POST':
        item = Item(text=request.POST['item_text'], list=list_)
        try:
            item.full_clean()
        except ValidationError:
            error = "You can't have an empty list item."
        else:
            item.save()
            return redirect('/lists/{list_.id}/'.format(list_=list_))
    return render(request, 'lists/list.html', {'list': list_, 'error': error})


def new_list(request):
    list_ = List.objects.create()
    item = Item(text=request.POST['item_text'], list=list_)
    try:
        item.full_clean()
    except ValidationError:
        list_.delete()
        return render(
            request,
            'lists/home.html',
            {'error': "You can't have an empty list item."}
        )
    else:
        item.save()
    return redirect('/lists/{list_.id}/'.format_map(locals()))
