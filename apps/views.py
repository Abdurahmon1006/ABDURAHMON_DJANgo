from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.core.mail import send_mail
from django.conf import settings
import random


def random_percent():
    return f"{random.randint(0, 100)}%"

def random_delay():
    return f"{random.uniform(0.1, 3):.2f}s"

def about(request):
    particles = [{
        'top': random_percent(),
        'left': random_percent(),
        'delay': random_delay()
    } for _ in range(30)]  # 30 ta zarracha

    return render(request, 'about.html', {'particles': particles})  # ✅ BU YER TO‘G‘RILANDI


# Create your views here.
def home(request):
    return render(request, 'index.html')

def components(request):
    return render(request, 'components.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        email = request.POST.get('email')
        message = request.POST.get('message')
        full_message = f"{email} dan sizga quyidagi habar keldi:\n\n\n{message}"

        try:
            send_mail(
                f'{name} sizga habar yubordi.',
                full_message,
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER, ],
                fail_silently=False,
            )
            return redirect('index')
        except Exception as e:
            print(f"Email yuborishda xato: {e}")
            return HttpResponse(f"Xato yuz berdi: {e}")

    return render(request, 'contact.html')

def work(request):
    works = ish.objects.all()
    return render(request, 'work.html', {'works': works})

def works(request):
    # Endi works sahifasida yutuqlar ko'rsatiladi
    yutuqlar = yutuq.objects.all()
    return render(request, 'works.html', {'yutuqlar': yutuqlar})

def yutuq_detail(request, id):
    yutuq_obj = yutuq.objects.get(id=id)
    return render(request, 'yutuq_detail.html', {'yutuq': yutuq_obj})
