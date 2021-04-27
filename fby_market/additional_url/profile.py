from django.urls import path
from main.modules.user.profile import ProfileView, ProfileEditView

urlpatterns = [
    path('', ProfileView.as_view(), name="profile"),
    path('edit/', ProfileEditView.as_view(), name="profile_edit"),
]
