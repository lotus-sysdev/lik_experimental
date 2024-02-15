from django.shortcuts import render, redirect
from .forms import CustomerForm
# Create your views here.
def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            # return redirect('success_url')  # Replace 'success_url' with the URL you want to redirect to after successfully adding a customer
    else:
        form = CustomerForm()
    return render(request, 'page1.html', {'form': form})
