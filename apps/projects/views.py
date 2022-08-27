from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, JSONParser
from django.views.decorators.csrf import csrf_exempt
from .models import *
from users.models import UserProfile
from apps.projects.models import Project
from apps.social.models import Group
from .serializers import *
from rest_framework.response import Response

# TODO : 프로젝트 만들기/변경/삭제 구현.




# TODO : 구독/구독취소 구현 (보류)

# TODO : 위의 내용에 대한 조회 구현

class GetPrjView(viewsets.ModelViewSet):
    # 내가 쓴 것 & 내가 팔로하고있는 사람들이 쓴 것 중에서 그 사람들이 나에게 오픈한 것

    serializer_class = PrjListSerializer

    def get_queryset(self):
        queryset = None
        uid = self.kwargs['uid']
        if uid is not None:
            user = UserProfile.objects.filter(pk=uid).get()
            queryset = Project.objects.filter(user=user).values('id', 'pname')

        return queryset

    def retrieve(self, request, uid):
        queryset = self.get_queryset()
        if queryset :
            instance = [[i['id'], i['pname']] for i in queryset]

        else :
            instance = None

        return Response(instance)