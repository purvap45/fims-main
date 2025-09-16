from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from family.models import FamilyMember, FamilyHead, State, City, statusChoice 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from family.forms import *
from django.http import JsonResponse
from family.forms import FamilyMemberForm
from django.db.models import Count, Q
import json

@login_required(login_url='login_page')
def dashboard(request):
    heads = FamilyHead.objects.all()
    members = FamilyMember.objects.all()
    states = State.objects.all()
    cities = City.objects.all()

    # Chart data: count members per state
    members_per_state = (
        FamilyHead.objects.values('state__state_name')
        .annotate(total=Count('id'))
        .order_by('state__state_name')
    )
    labels = [item['state__state_name'] for item in members_per_state]
    values = [item['total'] for item in members_per_state]

    context = {
        'members': members,
        'heads': heads,
        'states': states,
        'cities': cities,
        'chart_labels': json.dumps(labels),   # ✅ JSON string
        'chart_values': json.dumps(values),   # ✅ JSON string
    }
    return render(request, 'dashboard.html', context)

# @login_required(login_url='login_page')
# def dashboard(request):
#     heads = FamilyHead.objects.all()
#     members = FamilyMember.objects.all()
#     states = State.objects.all()
#     cities = City.objects.all()

#     # Chart data: count members per state
#     members_per_state = (
#         FamilyHead.objects.values('state__state_name')
#         .annotate(total=Count('id'))
#         .order_by('state__state_name')
#     )
#     labels = [item['state__state_name'] for item in members_per_state]
#     values = [item['total'] for item in members_per_state]

#     context = {
#         'members': members,
#         'heads': heads,
#         'states': states,
#         'cities': cities,
#         'chart_labels': json.dumps(labels),   # ✅ JSON string
#         'chart_values': json.dumps(values),   # ✅ JSON string
#     }
#     return render(request, 'dashboard.html', context)


@login_required(login_url='login_page')
def family_list(request):
    heads = FamilyHead.objects.annotate(member_count=Count('members', filter=~Q(members__status=9)))
    members = FamilyMember.objects.all()
    
    if request.GET.get('search'):
        name = heads.filter(name__icontains=request.GET.get('search'))
        mobno = heads.filter(mobno__icontains=request.GET.get('search'))
        state = heads.filter(state__state_name__icontains=request.GET.get('search'))
        city = heads.filter(city__city_name__icontains=request.GET.get('search'))
        heads = name.union(mobno, state, city)

    p = Paginator(heads, 10)  
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    totalPages = page_obj.paginator.num_pages
    context = {
        'members': members,
        'page_obj': page_obj,
        'lastPage': totalPages,
        'totalPagelist': [n+1 for n in range(totalPages)],
    }
    return render(request, 'family_list.html', context)

@login_required(login_url='login_page')
def view_family(request, pk):
    head = FamilyHead.objects.get(id=pk)
    members = FamilyMember.objects.filter(family_head_id=pk).exclude(status=statusChoice.DELETE).all()
    hobbies = Hobby.objects.filter(family_head_id=pk).exclude(status=statusChoice.DELETE).all()
    
    context = {
        'head': head,
        'members': members,
        'hobbies': hobbies
    }
    return render(request, 'view_family.html', context)

@login_required(login_url='login_page')
def update_head(request, pk):
    head = FamilyHead.objects.get(id=pk)
    head_form = FamilyHeadForm(instance=head)
    if request.method == 'POST':
        head_form = FamilyHeadForm(request.POST, request.FILES, instance=head)
        if head_form.is_valid():
            head_form.save()
            return redirect('view_family', pk=pk)
        else:
            print(head_form.errors)
            return JsonResponse({
                "success": False,
                "head_errors": head_form.errors,
            })
    context = {
        'head': head,
        'head_form': head_form
    }
    return render(request, 'update_head.html', context)

@login_required(login_url='login_page')
def add_hobby(request, pk):
    head = FamilyHead.objects.get(id=pk)
    HobbyFormSet = inlineformset_factory(FamilyHead, Hobby, form=HobbyForm, extra=1, formset=HobbyInlineFormSet)
    hobby_formset = HobbyFormSet(prefix="hobbies")
    if request.method == 'POST':
        hobby_formset = HobbyFormSet(request.POST, instance=head, prefix="hobbies")
        if hobby_formset.is_valid():
            hobby_formset.save()
            return redirect('view_family', pk=pk)
        # else:
        #     print(hobby_formset.errors)
        #     return JsonResponse({
        #         "success": False,
        #         "hobby_formset": hobby_formset.errors,
        #     })
    context = {
        'head': head,
        'hobby_formset': hobby_formset
    }
    return render(request, 'add_hobby.html', context)

@login_required(login_url='login_page')
def update_hobby(request, pk):
    head = FamilyHead.objects.get(id=pk)
    HobbyFormSet = inlineformset_factory(FamilyHead, Hobby, form=HobbyForm, extra=0, formset=HobbyInlineFormSet)
    hobby_formset = HobbyFormSet(instance=head, prefix="hobbies",  queryset=Hobby.objects.exclude(status=statusChoice.DELETE))
    if request.method == 'POST':
        hobby_formset = HobbyFormSet(request.POST, instance=head, prefix="hobbies")
        if hobby_formset.is_valid():
            # for form in formset.deleted_forms:

            hobby_formset.save()
            return redirect('view_family', pk=pk)
    context = {
        'head': head,
        'hobby_formset': hobby_formset
    }
    return render(request, 'update_hobby.html', context)

@login_required(login_url='login_page')
def add_member(request, pk):
    head = FamilyHead.objects.get(id=pk)
    MemberFormset = inlineformset_factory(FamilyHead, FamilyMember, form=FamilyMemberForm, extra=1, formset=MemberInlineFormSet)
    member_formset = MemberFormset(prefix="members")
    if request.method == 'POST':
        member_formset = MemberFormset(request.POST, request.FILES, instance=head, prefix="members")
        if member_formset.is_valid():
            member_formset.save()
            return redirect('view_family', pk=pk)
        # else:
        #     print(member_formset.errors)
        #     return JsonResponse({
        #         "success": False,
        #         "member_formset": member_formset.errors,
        #     })
    context = {
        'head': head,
        'member_formset': member_formset
    }
    return render(request, 'add_member.html', context)

@login_required(login_url='login_page')
def update_member(request, pk):
    head = FamilyHead.objects.get(id=pk)
    MemberFormset = inlineformset_factory(FamilyHead, FamilyMember, form=FamilyMemberForm, extra=0, formset=MemberInlineFormSet)
    member_formset = MemberFormset(instance=head, prefix="members",  queryset=FamilyMember.objects.exclude(status=statusChoice.DELETE))
    if request.method == 'POST':
        member_formset = MemberFormset(request.POST, request.FILES, instance=head, prefix="members")
        if member_formset.is_valid():
            member_formset.save()
            return redirect('view_family', pk=pk)
        # else:
        #     print(member_formset.errors)
        #     return JsonResponse({
        #         "success": False,
        #         "member_formset": member_formset.errors,
        #     })
    context = {
        'head': head,
        'member_formset': member_formset
    }
    return render(request, 'update_member.html', context)

@login_required(login_url='login_page')
def delete_family(request, pk):
    head = FamilyHead.objects.get(id=pk)
    if request.method == 'POST':
        head.status = statusChoice.DELETE
        head.save()
        FamilyMember.objects.filter(family_head_id=head).update(status = statusChoice.DELETE)
        return redirect('family_list')
    context = {'head':head}
    return render(request, 'delete_family.html', context)


def update_family(request, pk):
    head = FamilyHead.objects.get(id=pk)

    HobbyFormSet = inlineformset_factory(
        FamilyHead, Hobby, form=HobbyForm, extra=0, can_delete=True
    )
    MemberFormSet = inlineformset_factory(
        FamilyHead, FamilyMember, form=FamilyMemberForm, extra=0, can_delete=True
    )

    head_form = FamilyHeadForm(instance=head)
    hobby_formset = HobbyFormSet(instance=head, prefix="hobbies")
    member_formset = MemberFormSet(instance=head, prefix="members")

    if request.method == "POST":
        head_form = FamilyHeadForm(request.POST, request.FILES, instance=head)
        hobby_formset = HobbyFormSet(request.POST, instance=head, prefix="hobbies")
        member_formset = MemberFormSet(request.POST, request.FILES, instance=head, prefix="members")

        if head_form.is_valid() and hobby_formset.is_valid() and member_formset.is_valid():
            head_form.save()
            hobby_formset.save()
            member_formset.save()
            return redirect('view_family', pk=pk)
            # return JsonResponse({"success": True})
        else:
            return JsonResponse({
                "success": False,
                "head_errors": head_form.errors,
                "hobby_errors": hobby_formset.errors,
                "member_errors": member_formset.errors,
            }, status=400)

    context = {
        "head_form": head_form,
        "hobby_formset": hobby_formset,
        "member_formset": member_formset,
        "head": head,
    }
    return render(request, "update_family.html", context)


# def update_member(request, pk):
#     member = FamilyMember.objects.get(id=pk)
#     form = FamilyMemberForm(instance=member)
#     if request.method == 'POST':
#         form = FamilyMemberForm(request.POST, request.FILES, instance=member)
#         if form.is_valid():
#             form.save()
#             return redirect('view_family', pk=member.family_head.id)
#         else:
#             print(form.errors)
#             return JsonResponse({
#                 "success": False,
#                 "member_formset": form.errors,
#             })
#     context = {
#         'member': member,
#         'form': form
#     }
#     return render(request, 'update_member.html', context)