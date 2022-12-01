from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from backend import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


urlpatterns = [
    path('profile/', views.profile.as_view()),
    path('profile/password/', views.changePassword.as_view()),
    path('users/', views.insertUsers.as_view()),
    path('users/<str:username>', views.getUser.as_view()),
    path('questions/',views.getQuestions.as_view()),
    path('questions/<int:id>',views.getQuestion.as_view()),
    path('questions/user/',views.getQuestionsAuthor.as_view()),
    path('questions/insert/',views.insertQuestion.as_view()),
    path('questions/update/<int:id>',views.updateQuestion.as_view()),
    path('questions/delete/<int:id>',views.deleteQuestion.as_view()),
    path('quizzes/',views.getQuizzes.as_view()),
    path('quizzes/<int:id>',views.getQuiz.as_view()),
    path('quizzes/user/',views.getQuizAuthor.as_view()),
    path('quizzes/insert/',views.insertQuiz.as_view()),
    path('quizzes/update/<int:id>',views.updateQuiz.as_view()),
    path('quizzes/delete/<int:id>',views.deleteQuiz.as_view()),
    path('history/',views.insertHistory.as_view()),
    path('history/user/',views.historyUser.as_view()),
    path('history/question/<int:id>',views.historyQuestion.as_view()),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/verify/', TokenVerifyView.as_view(), name='token_verify'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)