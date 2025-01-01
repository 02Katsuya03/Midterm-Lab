from django.urls import path
from .views import LostDashboardView, LostSchool, LostListView, LostViewItem, LostDetailView, LostAddItemView, LostUpdateItemView, LostDeleteItemView, ClaimView
from .views import FoundDashboardView, FoundListView, FoundViewItem, FoundDetailView, FoundAddItemView, FoundUpdateItemView, FoundDeleteItemView
from .views import IntroPageView, LoginUserView, LoginAdminView, AdminPageView
from .views import RegisterUserView, RegisterAdminView
from .views import logout_view, UserPageView
from . import views

urlpatterns = [
    path('intro/', IntroPageView.as_view(), name='intro'),
    path('logout/', logout_view, name='logout'), 
    path('login_user/', LoginUserView.as_view(), name='login_user'),
    path('login_admin/', LoginAdminView.as_view(), name='login_admin'),
    path('register_user/', RegisterUserView.as_view(), name='register_user'),
    path('register_admin/', RegisterAdminView.as_view(), name='register_admin'),
    path('user/', UserPageView.as_view(), name='user'),
    path('', AdminPageView.as_view(), name='administrator'),

    path('lost_dashboard/', LostDashboardView.as_view(), name='lost_dashboard'),
    path('lost_school/', LostSchool.as_view(), name='lost_school'),
    path('lost_listview/', LostListView.as_view(), name='lost_listview'),
    path('lost_viewitem/', LostViewItem.as_view(), name='lost_viewitem'),
    path('lost_detailview/<str:item_id>', LostDetailView.as_view(), name='lost_detailview'),
    path('lost_additem/create', LostAddItemView.as_view(), name='lost_additem'),
    path('lost_updateitem/<str:item_id>/edit', LostUpdateItemView.as_view(), name='lost_updateitem'),
    path('lost_updateitem/<str:item_id>/delete', LostDeleteItemView.as_view(), name='lost_deleteitem'),
   
    path('found_dashboard/', FoundDashboardView.as_view(), name='found_dashboard'),
    path('found_listview/', FoundListView.as_view(), name='found_listview'),
    path('found_viewitem/', FoundViewItem.as_view(), name='found_viewitem'),
    path('found_detailview/<str:item_id>', FoundDetailView.as_view(), name='found_detailview'),
    path('found_additem/create', FoundAddItemView.as_view(), name='found_additem'),
    path('found_updateitem/<str:item_id>/edit', FoundUpdateItemView.as_view(), name='found_updateitem'),
    path('found_updateitem/<str:item_id>/delete', FoundDeleteItemView.as_view(), name='found_deleteitem'),

    path('claim/', ClaimView.as_view(), name='claim')
]
