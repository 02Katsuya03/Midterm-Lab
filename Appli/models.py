from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.timezone import now
import random

class School(models.Model):
    Name = models.CharField(max_length=100)
    Address = models.CharField(max_length=255, blank=True, null=True)
    Contact_Number = models.CharField(max_length=15, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.Name = self.Name.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.Name

class Profile(models.Model):
    SEX = [
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),   
    ]

    ROLES = [
        ('User', 'User'),
        ('ADMIN', 'Admin')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    middle_name = models.CharField(max_length=30, blank=True)  
    sex = models.CharField(max_length=10, choices=SEX)         
    phone_number = models.CharField(max_length=15)              
    role = models.CharField(max_length=10, choices=ROLES, default='User')
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.user)


class LostItem(models.Model):
    CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),
        ('clothing', 'Clothing'),
        ('accessories', 'Accessories'),
        ('documents', 'Documents'),
        ('keys', 'Keys'),
        ('books_stationary', 'Books & Stationary'),
        ('bags_luggage', 'Bags & Luggage'),
        ('sporting_goods', 'Sporting Goods'),
        ('toys_games', 'Toys & Games'),
        ('money', 'Money')
    ]

    item_id = models.CharField(max_length=10, unique=True, blank=True, default='') 
    item_name = models.CharField(max_length=100)
    item_type = models.CharField(max_length=10, default='Lost')
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    date_lost = models.DateField()
    date_added = models.DateTimeField(default=now)
    location_lost = models.CharField(max_length=100)
    contact_information = models.CharField(max_length=100)
    lost_by = models.CharField(max_length=100, blank=True, null=True)
    school = models.ForeignKey('School', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='lost_items/', blank=True, null=True)
    is_claimed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item_name} - {self.category}"

    def save(self, *args, **kwargs):
        if not self.item_id:
            self.item_id = self._generate_unique_item_id()
        super().save(*args, **kwargs)

    def _generate_unique_item_id(self):
        while True:
            random_id = f"LT-{random.randint(10000000, 99999999)}"
            if not LostItem.objects.filter(item_id=random_id).exists():
                return random_id
            
class FoundItem(models.Model):
    CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),
        ('clothing', 'Clothing'),
        ('accessories', 'Accessories'),
        ('documents', 'Documents'),
        ('keys', 'Keys'),
        ('books_stationary', 'Books & Stationary'),
        ('bags_luggage', 'Bags & Luggage'),
        ('sporting_goods', 'Sporting Goods'),
        ('toys_games', 'Toys & Games'),
        ('money', 'Money')
    ]

    item_id = models.CharField(max_length=10, unique=True, blank=True, default='')  
    item_name = models.CharField(max_length=100)
    item_type = models.CharField(max_length=10, default='Found')
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    date_found = models.DateField()
    date_added = models.DateTimeField(default=now)
    location_found = models.CharField(max_length=100)
    contact_information = models.CharField(max_length=100)
    found_by = models.CharField(max_length=100, blank=True, null=True)
    school = models.ForeignKey('School', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='found_items/', blank=True, null=True)
    is_claimed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item_name} - {self.category}"

    def save(self, *args, **kwargs):
        if not self.item_id:
            self.item_id = self._generate_unique_item_id()
        super().save(*args, **kwargs)

    def _generate_unique_item_id(self):
        while True:
            random_id = f"FT-{random.randint(10000000, 99999999)}"
            if not FoundItem.objects.filter(item_id=random_id).exists():
                return random_id

class HistoryLog(models.Model):
    ACTION_CHOICES = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
    ]
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    item_name = models.CharField(max_length=255)
    performed_by = models.CharField(max_length=200, null=True)  
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True, blank=True) 
    timestamp = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=10, choices=Profile.ROLES, null=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.action.capitalize()} - {self.item_name} by {self.performed_by}"
    

class F2FClaim(models.Model):
    lost_item = models.ForeignKey(LostItem, on_delete=models.CASCADE)
    found_item = models.ForeignKey(FoundItem, on_delete=models.CASCADE, null=True, blank=True)  
    claimed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    claimed_at = models.DateTimeField(auto_now_add=True)
    appointment_required = models.BooleanField(default=False)  
    
    def __str__(self):
        return f"Claimed by {self.claimed_by.username} for {self.lost_item.item_name}"

    def save(self, *args, **kwargs):
        if self.lost_item:
            self.claimed_at = self.lost_item.date_lost  
        super().save(*args, **kwargs)


class OnlineClaim(models.Model):
    lost_item = models.ForeignKey(LostItem, on_delete=models.CASCADE)
    found_item = models.ForeignKey(FoundItem, on_delete=models.CASCADE, null=True, blank=True)  
    claimed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    claimed_at = models.DateTimeField(auto_now_add=True)
    appointment_date = models.DateTimeField()  
    is_confirmed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Online claim by {self.claimed_by.username} for {self.lost_item.item_name}"

    def save(self, *args, **kwargs):
        if self.lost_item:
            self.claimed_at = self.lost_item.date_lost  
        super().save(*args, **kwargs)
