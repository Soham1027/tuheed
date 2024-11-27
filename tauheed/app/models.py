from django.db import models
from django.contrib.auth.models import AbstractUser

# class BackOfficeStaff(models.Model):
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     email = models.EmailField(max_length=50, unique=True)
#     password = models.CharField(max_length=100)
#     is_active = models.BooleanField(default=False)

#     def __str__(self):
#         return f"{self.first_name} {self.last_name}"

#     class Meta:
#         db_table = "back_office_staff"


class UserData(AbstractUser):
    USER_TYPE_CHOICES = (
        ('1', 'Admin'),
        ('2', 'Staff'),
        ('3', 'User'),
    )
    EDUCATION_EMPLOYMENT_CHOICES = (
        ('SCHOOL', 'School'),
        ('COLLEGE', 'College'),
        ('EMPLOYMENT', 'Employment'),
    )


    gender = models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1)
    join_type = models.CharField(choices=USER_TYPE_CHOICES, max_length=1, default='3')  # Matches STAaccounts p_type
    date_of_birth = models.DateField(blank=True, null=True)
    parent_name = models.CharField(max_length=50)
    parent_surname = models.CharField(max_length=100)
    parent_phone_number = models.CharField(max_length=20)
    school_college_or_employment = models.CharField(choices=EDUCATION_EMPLOYMENT_CHOICES, max_length=20)
    diversity = models.CharField(max_length=100)
    photo_consent = models.BooleanField(default=False)
    term_and_condition_gdpr = models.BooleanField(default=False)
    discount_card=models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    groups = models.ManyToManyField('auth.Group', related_name='user_data_groups', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='user_data_permissions', blank=True)


    def __str__(self):
        return f"{self.username}"

    class Meta:
        db_table = "users"

class Sport(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "sports"


class BookingHistory(models.Model):
    PAYMENT_METHODS = (
        ('1', 'Cash'),
        ('2', 'Credit Card'),
        ('3', "Wep"),
    )   
    
    payment_methods = models.CharField(choices=PAYMENT_METHODS, max_length=25, null=True, blank=True)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, related_name="bookings")
    booking_date = models.DateField()
    slot_time = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(UserData, on_delete=models.CASCADE, related_name="booking_history")
    amount = models.IntegerField(null= True, blank= True)

    def __str__(self):
        return f"Booking by {self.user.username} - {self.sport.name} on {self.booking_date}"

    class Meta:
        db_table = "booking_history"