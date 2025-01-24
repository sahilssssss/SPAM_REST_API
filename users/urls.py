from django.urls import path
from .views import UserRegistration, MarkSpam, SearchByName, SearchByPhoneNumber

urlpatterns = [ 
    path('register/', UserRegistration.as_view(), name='register'),
    path('mark-spam/', MarkSpam.as_view(), name='mark_spam'),
    path('search-by-name/', SearchByName.as_view(), name='search_by_name'),
    path('search-by-phone/', SearchByPhoneNumber.as_view(), name='search_by_phone'),
]
