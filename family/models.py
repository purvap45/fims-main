from django.db import models

class statusChoice(models.IntegerChoices):
    ACTIVE = 1
    INACTIVE = 0
    DELETE = 9

class MaritalStatus(models.TextChoices):
    MARRIED = "Married"
    UNMARRIED = "Unmarried"

class BaseModel(models.Model):
    status = models.IntegerField(
        choices=statusChoice.choices,
        default=statusChoice.ACTIVE.value,
    )

    class Meta:
        abstract = True

    def soft_delete(self):
        self.status = statusChoice.DELETE
        self.save(update_fields=["status"])

    def delete(self, *args, **kwargs):
        # override hard delete with soft delete
        self.soft_delete()

class State(BaseModel):
    state_name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices = statusChoice.choices, default=statusChoice.ACTIVE.value)

    class Meta:
        db_table = "state"
        ordering = ["state_name"]

    def __str__(self):
        return self.state_name

    def soft_delete(self):
        super().soft_delete()
        # cascade: cities
        self.city_set.update(status=statusChoice.DELETE)
        # cascade: family heads -> inactive
        FamilyHead.objects.filter(state=self).update(status=statusChoice.INACTIVE)
    

class City(BaseModel):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    city_name = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices = statusChoice.choices, default=statusChoice.ACTIVE.value)

    class Meta:
        db_table = "city"

    def __str__(self):
        return self.city_name

    def soft_delete(self):
        super().soft_delete()
        # cascade: family heads -> inactive
        FamilyHead.objects.filter(city=self).update(status=statusChoice.INACTIVE)

class FamilyHead(BaseModel):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    dob = models.DateField()
    mobno = models.CharField(max_length=15)
    address = models.TextField()
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null = True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null = True, blank=True)
    pincode = models.CharField(max_length=6)
    marital_status = models.CharField(max_length=10, choices=MaritalStatus.choices, default='')
    wedding_date = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to="pictures")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices = statusChoice.choices, default=statusChoice.ACTIVE.value)

    class Meta:
        db_table = "family_head" 

    def __str__(self):
        return self.name

    def soft_delete(self):
        super().soft_delete()
        # cascade: members
        self.members.update(status=statusChoice.DELETE)
        # cascade: hobbies
        self.hobbies.update(status=statusChoice.DELETE)
    

class Hobby(BaseModel):
    hobby = models.CharField(max_length=50)
    family_head = models.ForeignKey(FamilyHead, on_delete=models.CASCADE, related_name="hobbies")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices = statusChoice.choices, default=statusChoice.ACTIVE.value)
 
    class Meta:
        db_table = "hobby"

    def __str__(self):
        return self.hobby

class FamilyMember(BaseModel):
    family_head = models.ForeignKey(FamilyHead, on_delete=models.CASCADE, related_name="members")
    member_name = models.CharField(max_length=50)
    member_dob = models.DateField()
    member_marital = models.CharField(max_length=10, choices=MaritalStatus.choices, default='')
    member_wedDate = models.DateField(null=True, blank=True)
    education = models.CharField(max_length=10, null=True, blank=True)
    member_photo = models.ImageField(upload_to="pictures", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices = statusChoice.choices, default=statusChoice.ACTIVE.value)

    class Meta:
        db_table = "family_member"

    def __str__(self):
        return self.member_name
    
    