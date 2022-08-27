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


# TODO : 유저 정보 수정(프로필사진 추가/변경, 상메 추가/변경, 닉네임 변경 등)

# TODO : 비밀번호 변경 구현

# TODO : 비밀번호 찾기 구현


# 프로필 조회 등도 여기서 할지 아니면 앱을 나눌지 고민!
# 달력보기도 리턴해야 하기 때문에 조회에서 할 일이 많음 > 여기부터는 정확히 화면구성 짜고 나서 리턴값에 따라 앱 나눠서 생각할 것

# TODO : 계정정보 조회 구현(내 정보 보기)

# TODO : 프로필정보 조회 구현(팔로잉/팔로워/나의 프로젝트)


