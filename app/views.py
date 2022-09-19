from django.http import HttpRequest
from django.shortcuts import render, redirect

from . import arrays
from .arrays_validation import clear_array


ARRAY_MANAGER: arrays.ArraysManager = arrays.ArraysManager()


def no_redirect(function):
    def wrapper(request: HttpRequest, *args, **kwargs):
        function(request, *args, **kwargs)
        return redirect(request.META['HTTP_REFERER'])

    return wrapper


def main(request: HttpRequest):
    context: dict = {
        'arrays': ARRAY_MANAGER.objects,
    }
    return render(request, 'app/main.html', context)


@no_redirect
def add_array(request: HttpRequest):
    array: str = request.POST.get('new-array', None)
    try:
        array: list[int | float] = clear_array(array)
        ARRAY_MANAGER.create(array)
    except ValueError:
        pass


@no_redirect
def delete_array(request: HttpRequest, array_id: int):
    ARRAY_MANAGER.delete(array_id)


@no_redirect
def process_arrays(request: HttpRequest):
    arrays.ProcessArrays()(arrays_manager=ARRAY_MANAGER)


@no_redirect
def save_changes(request: HttpRequest):
    for i, array_str in enumerate(request.POST.getlist('array', None)):
        try:
            array: list[int | float] = clear_array(array_str)
            ARRAY_MANAGER.objects[i] = array
        except ValueError:
            pass
