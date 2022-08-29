from re import template
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import loader

from .models import Booking, SchoolObject

def index(request):
    booking_list = Booking.objects.all().order_by('id').values("book_date","id", "start", "end", "status_id__name","school_object_id__object_name", "school_object_id__object_campus_id__name","user_id__login" )
    print(booking_list)
    template = loader.get_template('bot/index.html')
    context = {
        'booking_list': booking_list,

    }
    return HttpResponse(template.render(context, request))

# Create your views here.
