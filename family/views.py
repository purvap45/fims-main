from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from .forms import FamilyHeadForm, HobbyFormSet, MemberFormset
from .models import City

# Create your views here.
def home(request):
    return render(request, 'index.html')

def get_cities(request, state_id):
    # state_id = request.GET.get('state_id')
    cities = City.objects.filter(state_id=state_id).all()
    data = list(cities.values('id', 'city_name'))
    return JsonResponse(data, safe=False)

def family_form(request):
    head_form = FamilyHeadForm()
    hobby_formset = HobbyFormSet(prefix="hobbies")
    member_formset = MemberFormset(prefix="members")
    if request.method == 'POST':
        head_form = FamilyHeadForm(request.POST, request.FILES)
        hobby_formset = HobbyFormSet(request.POST, instance=head_form.instance, prefix="hobbies")
        member_formset = MemberFormset(request.POST, request.FILES, instance=head_form.instance, prefix="members")
        if head_form.is_valid() and hobby_formset.is_valid() and member_formset.is_valid():
            head = head_form.save()
            hobby_formset.instance = head
            hobby_formset.save()
            member_formset.instance = head
            member_formset.save()
            return JsonResponse({"success": True})
        else:
            return JsonResponse({
                "success": False,
                "head_errors": head_form.errors,
                "hobby_errors": hobby_formset.errors,
                "member_errors": member_formset.errors,
            }, status=400)
    # for GET requests
    context = {
        'head_form': head_form,
        'hobby_formset': hobby_formset,
        'member_formset': member_formset
    }
    return render(request, 'family_form.html', context)

# def family_form(request):
#     head_form = FamilyHeadForm()
#     hobby_formset = HobbyFormSet(prefix="hobbies")
#     member_formset = MemberFormset(prefix="members")
#     if request.method == 'POST':
#         head_form = FamilyHeadForm(request.POST, request.FILES)
#         if head_form.is_valid():
#             head = head_form.save(commit=False) 
#             hobby_formset = HobbyFormSet(request.POST, instance=head)
#             member_formset = MemberFormset(request.POST, request.FILES, instance=head)
#             if hobby_formset.is_valid() and member_formset.is_valid():
#                 head.save()
#                 hobby_formset.save()
#                 member_formset.save()
#                 return JsonResponse({"success": True})
#                 # return redirect('home')
#             else:
#                 print("Head form errors:", head_form.errors)    
#                 print("Hobby formset errors:", hobby_formset.errors)
#                 print("Member formset errors:", member_formset.errors)
#                 return JsonResponse({"success": False, "errorMessage": head_form.errors })
    
#     context = {
#         'head_form': head_form,
#         'hobby_formset': hobby_formset,
#         'member_formset': member_formset
#     }
#     return render(request, 'family_form.html', context)
