from django.contrib import admin # type: ignore
from django.urls import path,include # type: ignore
from . import views
from django.conf import settings # type: ignore
from django.conf.urls.static import static # type: ignore
urlpatterns = [
    path('', views.home,name="home"),
    path('about/', views.about, name="about"),
    path('signup/', views.signup, name="signup"),
    path('login_view',views.login_view,name="login_view"),
    path('toc',views.toc,name="toc"),
    path('list_pdfs/', views.list_pdfs, name='list_pdfs'),  # List PDFs view
    path('student_access/<int:subject_id>/', views.student_access, name='student_access'),
    path('software_engineering', views.software_engineering, name='software_engineering'),
    path('ai',views.ai,name="ai"),
    path('rm',views.rm,name="rm"),
    path('cn',views.cn,name="cn"),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

