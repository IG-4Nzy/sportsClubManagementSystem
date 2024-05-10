from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',views.index,name='index'),

    # auth 
    path('login',views.login,name='login'),
    path('logout_view',views.logout_view,name='logout_view'),
    path('register',views.register,name='register'),

    # admin 
    path('adminDash',views.adminDash,name='adminDash'),
    path('approve/<int:id>/',views.approve,name='approve'),
    path('reject/<int:id>/',views.reject,name='reject'),
    path('AdminviewMembers',views.AdminviewMembers,name='AdminviewMembers'),

    # club 
    path('clubProfileComplete',views.clubProfileComplete,name='clubProfileComplete'),
    path('clubDash',views.clubDash,name='clubDash'),
    path('addSports',views.addSports,name='addSports'),
    path('viewMembers',views.viewMembers,name='viewMembers'),
    path('removeSport/<int:id>/',views.removeSport,name='removeSport'),


    # member 
    path('memberDash',views.memberDash,name='memberDash'),
    path('enrollSports',views.enrollSports,name='enrollSports'),
    path('enroll/<int:id>/',views.enroll,name='enroll'),
    path('cancel/<int:id>/',views.cancel,name='cancel'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
