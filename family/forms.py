from django import forms
from django.forms import ModelForm, inlineformset_factory, BaseInlineFormSet
from .models import FamilyHead, City, Hobby, FamilyMember, statusChoice
import re
from datetime import datetime, date

class FamilyHeadForm(ModelForm):
    class Meta:
        model = FamilyHead
        fields = [
            "name", "surname", "dob", "mobno", "address",
            "state", "city", "pincode",
            "marital_status", "wedding_date", "photo"
        ]
        widgets = {
            "dob": forms.DateInput(attrs={"type": "date"}),
            "wedding_date": forms.DateInput(attrs={"type": "date"}),
            "marital_status": forms.RadioSelect(), 
            'name': forms.TextInput(attrs={'autocomplete': 'name'}),
        }
        labels = {
            "dob": "Date of Birth",
            "mobno": "Mobile Number",
            "marital_status": "Marital Status",
            
        }

    def clean(self):
        cleaned_data = super().clean()
        # name
        name = self.cleaned_data.get('name')
        if not name:
            self.add_error('name','Name is required.')
        elif len(name) < 3:
            self.add_error('name', 'Name must be at least 3 characters.')
        elif re.search(r'\d', name):
            self.add_error('name', 'Name cannot contain numbers.')
        # surname
        surname = self.cleaned_data.get('surname')
        if not surname:
            self.add_error('surname','Surname is required.')
        elif len(surname) < 3:
            self.add_error('surname', 'Surname must be at least 3 characters.')
        elif re.search(r'\d', surname):
            self.add_error('surname', 'Surname cannot contain numbers.')
        # dob
        dob = self.cleaned_data.get('dob')
        if not dob:
            self.add_error('dob', 'Date of Birth is required.')
        else:
            # birth_date = datetime.strptime(dob, "%Y-%m-%d")
            age = (datetime.now().date() - dob).days // 365
            if age < 21:
                self.add_error('dob', 'Age must be at least 21 years old.')
        # mob no
        mobno = self.cleaned_data.get('mobno')
        if not mobno:
            self.add_error('mobno', 'Mobile No. is required.')
        elif not re.match(r"^[0-9]{10}$", mobno):
            self.add_error('mobno', 'Mobile number must be exactly 10 digits.')
        # address
        address = self.cleaned_data.get('address')
        if not address:
            self.add_error('address', 'Address is required.')
        # state
        state = self.cleaned_data.get('state')
        if not state:
            self.add_error('state', 'State is required.')
        # city
        city = self.cleaned_data.get('city')
        if not city:
            self.add_error('city', 'City is required.')
        # pincode
        pincode = self.cleaned_data.get('pincode')
        if not pincode:
            self.add_error('pincode', 'Pincode is required.')
        elif not re.match(r"^[0-9]{6}$", pincode):
            self.add_error('pincode', 'Pincode must be exactly 6 digits.')
        # marital status
        marital_status = self.cleaned_data.get('marital_status')
        if not marital_status:
            self.add_error('marital_status', 'Please select Marital Status')
        # wedding date
        wedding_date = self.cleaned_data.get('wedding_date')
        if marital_status == 'Married' and not wedding_date:
            self.add_error('wedding_date', 'Wedding date is required.')
        # photo
        photo = self.cleaned_data.get('photo')
        if not photo:
            self.add_error('photo', 'Photo is required.')
        else:
            filename = photo.name
            if not re.search(r'\.(jpg|png)$', filename, re.IGNORECASE):
                self.add_error('photo', 'Only JPG, PNG allowed.')
            else:
                photo.seek(0, 2)
                size_kb = photo.tell() / 1000 / 1000
                photo.seek(0)
                if size_kb > 2:
                    self.add_error('photo', 'Photo size must be less than 2 MB.')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False
        self.fields['surname'].required = False
        self.fields['dob'].required = False
        self.fields['mobno'].required = False
        self.fields['address'].required = False
        self.fields['pincode'].required = False
        self.fields['marital_status'].required = False
        self.fields['wedding_date'].required = False
        self.fields['photo'].required = False

        self.fields['city'].queryset = City.objects.none()
        if 'state' in self.data:
            try:
                state_id = int(self.data.get('state'))
                self.fields['city'].queryset = City.objects.filter(state_id=state_id)
            except (ValueError, TypeError):
                pass 
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.state.city_set

class HobbyForm(ModelForm):
    class Meta:
        model = Hobby
        fields = ('hobby',)

class HobbyInlineFormSet(BaseInlineFormSet):
    def clean(self):
        cleaned_data = super().clean()
        for form in self.forms:
            hobby = form.cleaned_data.get('hobby')
            if not hobby:
                form.add_error('hobby','Hobby is required.')
    def save(self, commit=True):
        instances = super().save(commit=False)
        for obj in self.deleted_objects:
            obj.status = 9
            if commit:
                obj.save()
        for instance in instances:
            if commit:
                instance.save()
        return instances
    
HobbyFormSet = inlineformset_factory(FamilyHead, Hobby, form=HobbyForm, extra=1, formset=HobbyInlineFormSet)


class FamilyMemberForm(ModelForm):
    class Meta:
        model = FamilyMember
        fields = ['member_name', 'member_dob', 'member_marital', 'member_wedDate', 'education', 'member_photo']
        widgets = {
            "member_dob": forms.DateInput(attrs={"type": "date"}),
            "member_marital": forms.RadioSelect(),
            "member_wedDate": forms.DateInput(attrs={"type": "date"}),
        }
        labels = {
            "member_name": "Name",
            "member_dob": "Date of Birth",
            "member_marital": "Marital Status",
            "member_wedDate": "Wedding Date",
            "member_photo": "Photo",
        }


class MemberInlineFormSet(BaseInlineFormSet):
    def clean(self):
        cleaned_data = super().clean()
        for form in self.forms:
            # member_name
            member_name = form.cleaned_data.get('member_name')
            if not member_name:
                form.add_error('member_name','Name is required.')
            elif len(member_name) < 3:
                form.add_error('member_name', 'Name must be at least 3 characters.')
            elif re.search(r'\d', member_name):
                form.add_error('member_name', 'Name cannot contain numbers.')
            # member_dob
            member_dob = form.cleaned_data.get('member_dob')
            if not member_dob:
                form.add_error('member_dob', 'Date of Birth is required.')
            # marital status
            member_marital = form.cleaned_data.get('member_marital')
            if not member_marital:
                form.add_error('member_marital', 'Please select Marital Status')
            # member wed date 
            member_wedDate = form.cleaned_data.get('member_wedDate')
            if member_marital == 'Married' and not member_wedDate:
                form.add_error('member_wedDate', 'Wedding date is required if married.')
            # photo
            member_photo = form.cleaned_data.get('member_photo')
            if member_photo:
                filename = member_photo.name
                if not re.search(r'\.(jpg|png)$', filename, re.IGNORECASE):
                    form.add_error('member_photo', 'Only JPG, PNG allowed.')
                else:
                    member_photo.seek(0, 2)
                    size_kb = member_photo.tell() / 1000 / 1000
                    member_photo.seek(0)
                    if size_kb > 2:
                        form.add_error('member_photo', 'Photo size must be less than 2 MB.')

    def save(self, commit=True):
        instances = super().save(commit=False)

        for obj in self.deleted_objects:
            obj.status = 9
            if commit:
                obj.save()
        for instance in instances:
            if commit:
                instance.save()
        return instances

MemberFormset = inlineformset_factory(FamilyHead, FamilyMember, form=FamilyMemberForm, extra=0, formset=MemberInlineFormSet)