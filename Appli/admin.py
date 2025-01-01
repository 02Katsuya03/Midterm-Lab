from django.contrib import admin
from .models import School, LostItem, Profile, FoundItem
from django import forms

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'sex', 'phone_number', 'role', 'school')

admin.site.register(Profile, ProfileAdmin)

admin.site.register(School)

class LostItemAdmin(admin.ModelAdmin):
    list_display = ('item_id','item_name', 'category', 'date_lost', 
                  'location_lost', 'lost_by','contact_information', 'school')

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'date_lost':
            kwargs['widget'] = forms.DateInput(format='%d/%m/%Y')
        return super().formfield_for_dbfield(db_field, **kwargs)
    
admin.site.register(LostItem, LostItemAdmin)

class FoundItemAdmin(admin.ModelAdmin):
    list_display = ('item_id','item_name', 'category', 'date_found', 
                  'location_found', 'found_by','contact_information', 'school')

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'date_lost':
            kwargs['widget'] = forms.DateInput(format='%d/%m/%Y')
        return super().formfield_for_dbfield(db_field, **kwargs)

admin.site.register(FoundItem, FoundItemAdmin)




