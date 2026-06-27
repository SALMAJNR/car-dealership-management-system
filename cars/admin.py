from django.contrib import admin
from .models import Brand, Category, Dealer, Car, Customer, CarImage
from .models import UserProfile


admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Dealer)
admin.site.register(UserProfile)
admin.site.register(Car)
admin.site.register(Customer)
admin.site.register(CarImage)
