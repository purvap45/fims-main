from django.shortcuts import render, redirect
from family.models import State, City, statusChoice
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import StateForm, CityForm
# Create your views here.

def state_list(request):
    states = State.objects.all()
    if request.GET.get('search'):
        states = states.filter(state_name__icontains=request.GET.get('search'))

    p = Paginator(states, 10)  
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    totalPages = page_obj.paginator.num_pages
    context = {
        'page_obj': page_obj,
        'lastPage': totalPages,
        'totalPagelist': [n+1 for n in range(totalPages)],
    }
    return render(request, 'state_list.html', context)

def create_state(request):
    state_form = StateForm()
    if request.method == 'POST':
        state_form = StateForm(request.POST)
        if state_form.is_valid():
            state_form.save()
            return redirect('state_list')
    context = {'state_form': state_form }
    return render(request, 'create_state.html', context)

def update_state(request, pk):
    state = State.objects.get(id=pk)
    state_form = StateForm(instance=state)
    if request.method == 'POST':
        state_form = StateForm(request.POST, instance=state)
        if state_form.is_valid():
            state_form.save()
            return redirect('state_list')
    context = {'state_form': state_form }
    return render(request, 'update_state.html', context)

def delete_state(request, pk):
    state = State.objects.get(id=pk)
    if request.method == 'POST':
        state.status = statusChoice.DELETE
        state.save()
        City.objects.filter(state_id=state).update(status = statusChoice.DELETE)
        return redirect('state_list')
    context = {'state':state}
    return render(request, 'delete_state.html', context)

def city_list(request):
    cities = City.objects.all()
    if request.GET.get('search'):
        cities = cities.filter(city_name__icontains=request.GET.get('search'))

    p = Paginator(cities, 10)  
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    totalPages = page_obj.paginator.num_pages
    context = {
        'page_obj': page_obj,
        'lastPage': totalPages,
        'totalPagelist': [n+1 for n in range(totalPages)],
    }
    return render(request, 'city_list.html', context)

def create_city(request):
    city_form = CityForm()
    if request.method == 'POST':
        city_form = CityForm(request.POST)
        if city_form.is_valid():
            city_form.save()
            return redirect('city_list')
    context = {'city_form': city_form }
    return render(request, 'create_city.html', context)

def update_city(request, pk):
    city = City.objects.get(id=pk)
    city_form = CityForm(instance=city)
    if request.method == 'POST':
        city_form = CityForm(request.POST, instance=city)
        if city_form.is_valid():
            city_form.save()
            return redirect('city_list')
    context = {'city_form': city_form }
    return render(request, 'update_city.html', context)
    
def delete_city(request, pk):
    city = City.objects.get(id=pk)
    if request.method == 'POST':
        city.status = statusChoice.DELETE
        city.save()
        return redirect('city_list')
    context = {'city':city}
    return render(request, 'delete_city.html', context)
