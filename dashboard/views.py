from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.forms import inlineformset_factory
import json, logging

from family.models import FamilyMember, FamilyHead, State, City, statusChoice, Hobby
from family.forms import FamilyHeadForm, FamilyMemberForm, HobbyForm, HobbyInlineFormSet, MemberInlineFormSet
from family.utils import decode_id

logger = logging.getLogger(__name__)


@login_required(login_url='login_page')
def dashboard(request):
    try:
        heads = FamilyHead.objects.exclude(status=statusChoice.DELETE)
        members = FamilyMember.objects.exclude(status=statusChoice.DELETE)
        states = State.objects.exclude(status=statusChoice.DELETE)
        cities = City.objects.exclude(status=statusChoice.DELETE)

        family_count = State.objects.annotate(total=Count("familyhead")).order_by("-total")[:5]
        data = list(family_count.values('state_name', 'total'))
        json_data = json.dumps(data)

        active_states = State.objects.filter(status=statusChoice.ACTIVE).count()
        inactive_states = State.objects.filter(status=statusChoice.INACTIVE).count()

        context = {
            'members': members,
            'heads': heads,
            'states': states,
            'cities': cities,
            'json_data': json_data,
            'active_states': active_states,
            'inactive_states': inactive_states,
        }
        return render(request, 'dashboard.html', context)

    except Exception as e:
        logger.exception("Error in dashboard view: %s", e)
        messages.error(request, "An unexpected error occurred while loading the dashboard.")
        return redirect('login_page')


@login_required(login_url='login_page')
def family_list(request):
    try:
        heads = FamilyHead.objects.annotate(
            member_count=Count('members', filter=~Q(members__status=9))
        ).exclude(status=statusChoice.DELETE).order_by('-created_at')

        members = FamilyMember.objects.all()

        # Search filter
        search_query = request.GET.get('search')
        if search_query:
            name = heads.filter(name__icontains=search_query)
            mobno = heads.filter(mobno__icontains=search_query)
            state = heads.filter(state__state_name__icontains=search_query)
            city = heads.filter(city__city_name__icontains=search_query)
            heads = name.union(mobno, state, city)

        # Pagination
        p = Paginator(heads, 10)
        page_number = request.GET.get('page')
        page_obj = p.get_page(page_number)
        totalPages = page_obj.paginator.num_pages

        context = {
            'members': members,
            'page_obj': page_obj,
            'lastPage': totalPages,
            'totalPagelist': [n + 1 for n in range(totalPages)],
        }

        # Handle AJAX pagination
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            family_html = render_to_string('list_template.html', context, request=request)
            return JsonResponse({'family_html': family_html})

        return render(request, 'family_list.html', context)

    except PageNotAnInteger:
        logger.warning("Page number not an integer.")
        return redirect('family_list')

    except EmptyPage:
        logger.warning("Empty page requested in paginator.")
        return redirect('family_list')

    except Exception as e:
        logger.exception("Error in family_list view: %s", e)
        messages.error(request, "Unable to load family list. Please try again later.")
        return redirect('dashboard')


@login_required(login_url='login_page')
def view_family(request, hashid):
    try:
        pk = decode_id(hashid)
        head = FamilyHead.objects.get(id=pk)
        members = FamilyMember.objects.filter(family_head_id=pk).exclude(status=statusChoice.DELETE)
        hobbies = Hobby.objects.filter(family_head_id=pk).exclude(status=statusChoice.DELETE)

        context = {'head': head, 'members': members, 'hobbies': hobbies}
        return render(request, 'view_family.html', context)

    except FamilyHead.DoesNotExist:
        messages.error(request, "Family not found.")
        return redirect('family_list')

    except Exception as e:
        logger.exception("Error in view_family: %s", e)
        messages.error(request, "An error occurred while loading family details.")
        return redirect('family_list')


@login_required(login_url='login_page')
def update_family(request, hashid):
    try:
        pk = decode_id(hashid)
        head = FamilyHead.objects.get(id=pk)

        HobbyFormSet = inlineformset_factory(FamilyHead, Hobby, form=HobbyForm, extra=0, can_delete=True, formset=HobbyInlineFormSet)
        MemberFormset = inlineformset_factory(FamilyHead, FamilyMember, form=FamilyMemberForm, extra=0, can_delete=True, formset=MemberInlineFormSet)

        head_form = FamilyHeadForm(instance=head)
        hobby_formset = HobbyFormSet(instance=head, prefix="hobbies", queryset=head.hobbies.exclude(status=statusChoice.DELETE))
        member_formset = MemberFormset(instance=head, prefix="members", queryset=head.members.exclude(status=statusChoice.DELETE))

        if request.method == 'POST':
            head_form = FamilyHeadForm(request.POST, request.FILES, instance=head)
            hobby_formset = HobbyFormSet(request.POST, instance=head, prefix="hobbies")
            member_formset = MemberFormset(request.POST, request.FILES, instance=head, prefix="members")

            if head_form.is_valid() and hobby_formset.is_valid() and member_formset.is_valid():
                family_head = head_form.save()
                hobby_formset.save()
                member_formset.save()
                family_head.set_status(family_head.status)
                return JsonResponse({"success": True, "message": "Family updated successfully."})
            else:
                return JsonResponse({
                    "success": False,
                    "head_errors": head_form.errors,
                    "hobby_errors": hobby_formset.errors,
                    "member_errors": member_formset.errors,
                }, status=400)

        context = {
            'head_form': head_form,
            'hobby_formset': hobby_formset,
            'member_formset': member_formset,
            'head': head,
        }
        return render(request, 'update_family.html', context)

    except FamilyHead.DoesNotExist:
        messages.error(request, "Family not found.")
        return redirect('family_list')

    except Exception as e:
        logger.exception("Error in update_family: %s", e)
        return JsonResponse({"success": False, "errorMessage": "Unexpected error occurred while updating family."}, status=500)


@login_required(login_url='login_page')
def delete_family(request, hashid):
    try:
        pk = decode_id(hashid)
        head = FamilyHead.objects.get(id=pk)
        head.soft_delete()
        messages.success(request, 'Family deleted successfully!')
        return redirect('family_list')

    except FamilyHead.DoesNotExist:
        messages.error(request, "Family not found.")
        return redirect('family_list')

    except Exception as e:
        logger.exception("Error in delete_family: %s", e)
        messages.error(request, "Unable to delete family. Please try again later.")
        return redirect('family_list')
    
