from django.shortcuts import render, redirect
from .forms import CustomerForm,PIC_Forms
from django.http import HttpResponse
# Create your views here.
def placeholder(request):
    return HttpResponse("Hello World")
def my_view(request):
    customer_form = CustomerForm(request.POST or None)
    pic_form = PIC_Forms(request.POST or None)
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            # return redirect('success_url')  # Replace 'success_url' with the URL you want to redirect to after successfully adding a customer
    else:
        form = CustomerForm()

    return render(request, 'page1.html', {'customer_form': customer_form})

