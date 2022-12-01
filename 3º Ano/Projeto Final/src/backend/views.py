
from django.shortcuts import  get_object_or_404
from rest_framework.response import Response
from backend import models
from backend import serializers
from datetime import datetime
from rest_framework.permissions import IsAuthenticated
from backend import permissions
import re

from rest_framework.views import APIView

# Create your views here.

class changePassword(APIView):
    permission_classes = (IsAuthenticated,permissions.IsCurrentPassword )
    def post(self, request):
        self.check_object_permissions(request,None)
        new = request.data.get('new')
        if not new:
            new = request.user.username
        request.user.set_password(new)
        request.user.save()
        return Response(status=200)


class insertUsers(APIView):
    def post(self, request):
        serializer = serializers.User(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()
        instance = serializer.validated_data
        instance.pop('password')
        return Response(instance, status=201)


class getUser(APIView):
    permission_classes = (IsAuthenticated, )
    def get(self, request, username):
        user = get_object_or_404(models.User.objects.filter(username=username))
        serializer = serializers.User(instance=user)
        return Response(serializer.data, status=200)

class profile(APIView):
    permission_classes = (IsAuthenticated, )
    def get(self,request):
        user = get_object_or_404(models.User.objects.filter(username=request.user.username))
        serializer = serializers.User(instance=user)
        return Response(serializer.data, status=200)



class getQuestions(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        questions = models.Question.objects.all()
        if request.user.type == 'A':
            serializer = serializers.LoadQuestionForAuthor(instance=questions,many=True)
        else:
            serializer = serializers.LoadQuestionForPlayer(instance=questions,many=True)

        return Response(serializer.data,status=200)
    
class getQuestion(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, id):
        question = get_object_or_404(models.Question.objects.filter(id=id))
        if request.user.type == 'A':
            serializer = serializers.LoadQuestionForAuthor(instance=question)
        else:
            serializer = serializers.LoadQuestionForPlayer(instance=question)
        return Response(serializer.data,status=200)

class getQuestionsAuthor(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        questions = models.Question.objects.filter(author=request.user.id)
        serializer = serializers.LoadQuestionForAuthor(instance=questions,many=True)
        return Response(serializer.data,status=200)

    


class insertQuestion(APIView):
    permission_classes = (IsAuthenticated,permissions.IsAuthor,)
    def post(self, request):
        self.check_object_permissions(request,None)
        data = request.data
        data.update({'author':request.user.id})
        serializer = serializers.SaveQuestion(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

class updateQuestion(APIView):
    permission_classes = (IsAuthenticated, permissions.IsOwner,)
    def post(self, request, id):
        question = get_object_or_404(models.Question.objects.filter(id=id))
        self.check_object_permissions(request,question)
        data = request.data
        data.update({'author':request.user.id})
        serializer = serializers.SaveQuestion(question,data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

class deleteQuestion(APIView):
    permission_classes = (IsAuthenticated, permissions.IsOwner,)
    def post(self, request, id):
        question = get_object_or_404(models.Question.objects.filter(id=id))
        self.check_object_permissions(request,question)
        question.delete()
        
        return Response(status=200)


class getQuizzes(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        quizzes = models.Quiz.objects.all()
        if request.user.type == 'A':
            serializer = serializers.LoadQuizForAuthor(instance=quizzes,many=True)
        else:
            serializer = serializers.LoadQuizForPlayer(instance=quizzes,many=True)

        return Response(serializer.data,status=200)

class getQuiz(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, id):
        quiz = get_object_or_404(models.Quiz.objects.filter(id=id))
        if request.user.type == 'A':
            serializer = serializers.LoadQuizForAuthor(instance=quiz)
        else:
            serializer = serializers.LoadQuizForPlayer(instance=quiz)
        return Response(serializer.data,status=200)

class getQuizAuthor(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        quizzes = models.Quiz.objects.filter(author=request.user.id)
        serializer = serializers.LoadQuizForAuthor(instance=quizzes,many=True)
        return Response(serializer.data,status=200)


class insertQuiz(APIView):
    permission_classes = (IsAuthenticated,permissions.IsAuthor,)
    def post(self, request):
        self.check_object_permissions(request,None)
        data = request.data
        data.update({'author': request.user.id})
        for question in data.get('questions'):
            question.update({'author': request.user.id})
        serializer = serializers.SaveQuiz(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

class updateQuiz(APIView):
    permission_classes = (IsAuthenticated, permissions.IsOwner,)
    def post(self, request,id):
        quiz = get_object_or_404(models.Quiz.objects.filter(id=id))
        self.check_object_permissions(request,quiz)
        data = request.data
        data.update({'author':request.user.id})
        for question in data.get('questions'):
            question.update({'author': request.user.id})
        serializer = serializers.SaveQuiz(quiz,data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

class deleteQuiz(APIView):
    permission_classes = (IsAuthenticated, permissions.IsOwner,)
    def post(self, request, id):
        quiz = get_object_or_404(models.Quiz.objects.filter(id=id))
        self.check_object_permissions(request,quiz)
        quiz.delete()
        
        return Response(status=200)

class insertHistory(APIView): 
    permission_classes = (IsAuthenticated,permissions.IsPlayer) 
    def post(self, request):
        self.check_object_permissions(request,None)
        data = request.data
        data.update({'correct':0})
        data.update({'player':request.user.id})
        formatted_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data.update({'date':str(formatted_date)})

        if 'answer' in request.data and 'question' in request.data:
            options = models.Option.objects.filter(question=request.data.get('question'),correct=True)
            question = get_object_or_404(models.Question.objects.filter(id=request.data.get('question')))
            if not options:
                return Response(status=404)
            for option in options:
                answer = option.answer
                type = question.type
                if type == 'SA' and bool(re.match(answer+'$',request.data.get('answer').strip())):
                    data.update({'correct':1})
                    break
                elif request.data.get('answer') == answer:
                    data.update({'correct':1})
                    break
         
        serializer = serializers.SaveHistory(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)




class historyUser(APIView):
    permission_classes = (IsAuthenticated,permissions.IsPlayer) 
    def get(self, request):
        self.check_object_permissions(request,None)
        history = models.History.objects.filter(player=request.user.id)
        serializer = serializers.LoadHistory(instance=history,many=True)
        result = serializer.data
        return Response(result, status=200)


class historyQuestion(APIView):
    permission_classes = (IsAuthenticated,permissions.IsOwner,) 
    def get(self, request, id):
        question = get_object_or_404(models.Question.objects.filter(id=id))
        self.check_object_permissions(request,question)
        history = models.History.objects.filter(question=id)
        serializer = serializers.LoadHistory(instance=history,many=True)
        result = serializer.data
        return Response(result, status=200)





