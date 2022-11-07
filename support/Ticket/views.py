from django.http import HttpResponse
from django.shortcuts import render


def ticket_test(request):
    return HttpResponse("Ticket test page")