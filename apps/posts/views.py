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


# TODO : 글 보기/수정/삭제 권한 줄 것

class MemoListView(viewsets.ModelViewSet):
    # 내가 쓴 것 & 내가 팔로하고있는 사람들이 쓴 것 중에서 그 사람들이 나에게 오픈한 것

    serializer_class = MemoListSerializer

    def get_queryset(self):
        queryset = None
        uid = self.kwargs['uid']
        if uid is not None :
            user = UserProfile.objects.filter(pk=uid).get()
            grp = list(user.groupedby.all())
            muted = list(user.muted.all())
            projects = []
            for g in grp :
                if g.group.user not in muted :
                    prj = list(g.group.canread.all())
                    projects += prj
            queryset = Memo.objects.filter(project__in=projects).order_by('-created_at')

        return queryset

    def retrieve(self, request, uid):
        queryset = self.get_queryset()
        user = UserProfile.objects.filter(pk=uid).get()

        if queryset :
            instance = []
            for q in queryset :
                cmtlist = []
                clplist = []
                comment = q.comment.all()
                clap = q.clap.all()
                cmtlen = len(comment)
                clplen = len(clap)
                is_claped_memo = 0
                if len(q.clap.filter(user=user)) != 0 :
                    is_claped_memo = 1

                for cmt in comment :
                    is_claped_comment = 0
                    new_clp = cmt.clap.filter(user=user)
                    if len(new_clp) != 0 :
                        is_claped_comment = 1
                    new_cmt = {
                        'cid' : cmt.id,
                        'uid' : cmt.user.id,
                        'user' : cmt.user.username,
                        'comment' : cmt.comment,
                        'created_at' : cmt.created_at,
                        'is_claped' : is_claped_comment
                    }
                    cmtlist.append(new_cmt)
                for clp in clap :
                    clplist.append(clp.user.username)
                try :
                    # 프론트용으로 주소 붙여 내보내기(나중에 주소 고쳐야 함)
                    path = q.image.name
                    if len(path) != 0 :
                        path = 'http://127.0.0.1:8000/media/' + path
                    memo = {
                        'uid' : q.user.pk,
                        'mid' : q.pk,
                        'user' : q.user.username,
                        'project' : q.project.pname,
                        'contents' : q.contents,
                        'image' : path,
                        'number' : q.number,
                        'created_at' : q.created_at,
                        'commentcount' : cmtlen,
                        'clapcount' : clplen,
                        'is_claped' : is_claped_memo,
                        'comments' : cmtlist
                    }
                    instance.append(memo)
                    pass
                except :
                    memo = {
                        'uid': q.user.pk,
                        'user': q.user.username,
                        'project': q.project.pname,
                        'contents': q.contents,
                        'image': '',
                        'number': q.number,
                        'created_at': q.created_at,
                        'commentcount': cmtlen,
                        'clapcount': clplen,
                        'is_claped': is_claped_memo,
                        'comments': cmtlist
                    }
                    instance.append(memo)
        else :
            instance = None

        return Response(instance)


# TODO : delete는 왜 메시지 리턴을 못할까?
# TODO : 메모 수정시 프로젝트 수정을 하고 싶으면 어떻게 할지 고민해볼 것(넘버 붙는 것때문에..)
class MemoView(viewsets.ModelViewSet):

    serializer_class = MemoSerializer
    parser_classes = (MultiPartParser, JSONParser, )  # 파일필드용

    def get_queryset(self):
        queryset = None
        if len(self.kwargs) != 0 :
            mid = self.kwargs['mid']
            if mid != None :
                queryset = Memo.objects.filter(pk=mid)
        elif self.request.data.get('id') :
            mid = self.request.data.get('id')
            queryset = Memo.objects.filter(pk=mid)
        else :
            uid = self.request.data.get('user')
            if uid is not None :
                queryset = UserProfile.objects.filter(pk=uid)
        return queryset

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        try:
            obj = queryset.get()
            return obj
        except:
            return None

    def perform_create(self, serializer):
        data = serializer.validated_data
        user = self.get_object()
        pid = data.get('project')
        data['error'] = ''

        # user 정보가 없을 경우 오류 리턴
        if (user == None):
            data['error'] = "User not exists"
            serializer.save()

            # # 신규프로젝트 생성을 선택했을 경우를 위한 항목(기존 프로젝트를 선택했을 경우 None)
            # pname = data.get('pname')
            # grp = data.get('group')
            # group = user.groups.filter(pk=grp)
            # if len(group) != 1 :
            #     return HttpResponseNotFound("Error")
            # group = group.get()

            # # 신규프로젝트 생성을 선택했을 경우, 프로젝트 생성 진행
            # if (pid == 'etc') & (pname != None) :
            #     new_project = Project.objects.create(
            #         user = user,
            #         pname = pname,
            #         group = group
            #     )
            #     pid = new_project.pk

        project = Project.objects.filter(pk=pid, user=user)

        if len(project) == 1 :
            project = project.get()
            data['user'] = user
            data['project'] = project

            # 해당 프로젝트에 포함된 게시글 수량을 계산하여 +1
            number = len(Memo.objects.filter(project=project))+1
            data['number'] = number

            serializer.save()

        # 기타 오류 사항에 에러 리턴
        elif (len(project) == 0) :
            data['error'] = "Project not exists"
            serializer.save()
        else :
            data['error'] = 'Error'
            serializer.save()

    # def perform_update(self, serializer):
    #     data = serializer.validated_data
    #     user = self.get_object()
    #     mid = data.get('id')
    #     data['error'] = ''
    #
    #     if (user != None) & (mid != None) :
    #         memo = Memo.objects.filter(user=user, pk=mid)
    #         if len(memo) == 1 :
    #             instance = memo.get()
    #             serializer.save()
    #         else :
    #             data['error'] = "Error"
    #             serializer.save()
    #     else :
    #         data['error'] = 'Pleace check the user id or memo id'
    #         serializer.save()


class CommentView(viewsets.ModelViewSet):

    serializer_class = CommentSerializer
    parser_classes = (JSONParser,)

    def get_queryset(self):
        queryset = None
        if len(self.kwargs) != 0 :
            cid = self.kwargs['cid']
            if cid != None :
                queryset = Comment.objects.filter(pk=cid)
        elif self.request.data.get('id') :
            cid = self.request.data.get('id')
            queryset = Comment.objects.filter(pk=cid)
        else :
            uid = self.request.data.get('user')
            if uid is not None :
                queryset = UserProfile.objects.filter(pk=uid)
        return queryset

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        try:
            obj = queryset.get()
            return obj
        except:
            return None

    def perform_create(self, serializer):
        data = serializer.validated_data
        user = self.get_object()
        mid = data.get('memo')
        data['error'] = ''

        # user 정보가 없을 경우 오류 리턴
        if (user == None):
            data['error'] = "User not exists"
            serializer.save()

        memo = Memo.objects.filter(pk=mid)

        if len(memo) == 1 :
            memo = memo.get()
            data['user'] = user
            data['memo'] = memo
            data['alertto'] = memo.user

            serializer.save()

        # 기타 오류 사항에 에러 리턴
        elif (len(memo) == 0) :
            data['error'] = "Memo not exists"
            serializer.save()
        else :
            data['error'] = 'Error'
            serializer.save()


class ClapView(viewsets.ModelViewSet):

    serializer_class = ClapSerializer
    parser_classes = (JSONParser,)

    def get_queryset(self):
        queryset = None
        uid = self.request.data.get('user')
        if uid is not None :
            queryset = UserProfile.objects.filter(pk=uid)
        return queryset

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        try:
            obj = queryset.get()
            return obj
        except:
            return None

    def perform_create(self, serializer):
        data = serializer.validated_data
        user = self.get_object()
        data['error'] = ''

        # user 정보가 없을 경우 오류 리턴
        if (user == None):
            data['error'] = "User not exists"
            serializer.save()

        data['didclaped'] = 0
        target = ''

        if data.get('memo') :
            mid = data.get('memo')
            target = Memo.objects.filter(pk=mid)
            data['type'] = 'memo'
            if len(target) != 1 :
                data['error'] = 'Error'
                serializer.save()
            else :
                target = target.get()
                check = Clap.objects.filter(memo=target, user=user)
                if len(check) != 0 :
                    data['clapinstance'] = check.get()
                    data['didclaped'] = 1

        elif data.get('comment') :
            cid = data.get('comment')
            target = Comment.objects.filter(pk=cid)
            data['type'] = 'comment'
            if len(target) != 1 :
                data['error'] = 'Error'
                serializer.save()
            else :
                target = target.get()
                check = Clap.objects.filter(comment=target, user=user)
                if len(check) != 0 :
                    data['clapinstance'] = check.get()
                    data['didclaped'] = 1

        data['user'] = user
        data['target'] = target
        data['alertto'] = target.user
        serializer.save()


# TODO : 알림 보기 구현(누군가가 나를 팔로/게시글에 코멘트/박수쳤을 때 새로운 객체가 생성됨. 내가 확인하고 나면 내이름으로 달린 객체 모두 삭제)
class AlertView(viewsets.ModelViewSet):
    # 알람개수 리턴

    serializer_class = AlertSerializer

    def get_queryset(self):
        queryset = None
        uid = self.kwargs['uid']
        if uid is not None :
            user = UserProfile.objects.filter(pk=uid).get()
            queryset = Alert.objects.filter(user=user, read=0).order_by('-created_at')
        return queryset

    def retrieve(self, request, uid):
        queryset = self.get_queryset()
        instance = str(len(queryset))

        return Response(instance)


class AlertDetailView(viewsets.ModelViewSet):
    # 알람개수 리턴

    serializer_class = AlertSerializer

    def get_queryset(self):
        queryset = None
        uid = self.kwargs['uid']
        if uid is not None :
            user = UserProfile.objects.filter(pk=uid).get()
            queryset = Alert.objects.filter(user=user).order_by('-created_at')
        return queryset

    def retrieve(self, request, uid):
        queryset = self.get_queryset()
        if queryset :
            instance = []

            for q in queryset :
                alert = {}
                comment = ''
                link = ''
                detail = ''
                by = q.user.username
                date = q.created_at
                if q.comment != None :
                    comment = f'{by} 님이 코멘트를 남겼습니다.'
                    link = ''
                    detail = q.comment.comment
                elif q.clap != None :
                    comment = f'{by} 님이 박수를 쳤습니다.'
                    link = ''
                    detail = ''
                elif q.follow != None :
                    comment = f'{by} 님이 팔로우했습니다.'
                    link = ''
                    detail = ''
                alert['comment'] = comment
                alert['link'] = link
                alert['detail'] = detail
                alert['date'] = date
                instance.append(alert)
                q.read = 1
                q.save()
        else :
            instance = None
        return Response(instance)





# TODO : 해당 내용에 대한 조회 구현(필요한 경우가 뭐뭐 있는지 생각해 볼 것)
