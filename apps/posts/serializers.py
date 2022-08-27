from rest_framework import serializers
from .models import *
from django.core.exceptions import ValidationError

class MemoListSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Memo
        fields = '__all__'


class MemoSerializer(serializers.ModelSerializer) :
    id = serializers.CharField(label='memo id', write_only=True, required=False)
    user = serializers.CharField(label='user id', write_only=True)
    project = serializers.CharField(label='user id', write_only=True)
    contents = serializers.CharField(label='contents', write_only=True)
    image = serializers.FileField(label='image', write_only=True, required=False)
    message = serializers.CharField(read_only=True)

    def create(self, data):
        if data.get('error') == '' :
            instance = Memo.objects.create(
                        user = data.get('user'),
                        project = data.get('project'),
                        contents = data.get('contents'),
                        image = data.get('image'),
                        number = data.get('number')
                    )
            message = {"message":"successfully posted"}
            return message
        else :
            message = data.get('error')
            return ValidationError(message, code=400)

    def update(self, instance, data):
        if instance :
            if data.get('image') != None:
                instance.contents = data.get('contents')
                instance.image = data.get('image')
            else:
                instance.contents = data.get('contents')
            instance.save()
            message = {"message":"successfully updated"}
            return message
        else :
            message = "Error"
            return ValidationError(message, code=400)

    def destroy(self, instance):
        if instance:
            instance.delete()
            message = {"message":"successfully deleted"}
            return message
        else :
            message = "Error"

    class Meta :
        model = Memo
        fields = ('id', 'user', 'project', 'contents', 'image', 'message')
        read_only_fields = ('message', )


class CommentSerializer(serializers.ModelSerializer) :
    id = serializers.CharField(label='comment id', write_only=True, required=False)
    user = serializers.CharField(label='user id', write_only=True, required=False)
    memo = serializers.CharField(label='memo id', write_only=True, required=False)
    comment = serializers.CharField(label='comment', write_only=True, required=False)
    message = serializers.CharField(read_only=True)

    def create(self, data):
        if data.get('error') == '' :
            instance = Comment.objects.create(
                        user = data.get('user'),
                        memo = data.get('memo'),
                        comment = data.get('comment')
                    )
            alert = Alert.objects.create(
                user = data.get('alertto'),
                comment = instance
            )
            message = {"message":"successfully posted"}
            return message
        else :
            message = data.get('error')
            return ValidationError(message, code=400)

    def update(self, instance, data):
        if instance :
            instance.comment = data.get('comment')
            instance.save()
            message = {"message":"successfully updated"}
            return message
        else :
            message = "Error"
            return ValidationError(message, code=400)

    def destroy(self, instance):
        if instance:
            instance.delete()
            message = {"message":"successfully deleted"}
            return message
        else :
            message = "Error"

    class Meta :
        model = Comment
        fields = ('id', 'user', 'memo', 'comment', 'message')
        read_only_fields = ('message', )


class ClapSerializer(serializers.ModelSerializer) :
    id = serializers.CharField(label='clap id', write_only=True, required=False)
    user = serializers.CharField(label='user id', write_only=True)
    memo = serializers.CharField(label='memo id', write_only=True, required=False)
    comment = serializers.CharField(label='comment', write_only=True, required=False)
    message = serializers.CharField(read_only=True)

    def create(self, data):
        if data.get('error') == '' :
            if data.get('didclaped') == 0 :
                if data.get('type') == 'memo' :
                    instance = Clap.objects.create(
                                user = data.get('user'),
                                memo = data.get('target')
                            )
                    alert = Alert.objects.create(
                        user = data.get('alertto'),
                        clap = instance
                    )
                    message = {"message":"successfully posted"}
                    return message
                else :
                    instance = Clap.objects.create(
                        user=data.get('user'),
                        comment=data.get('target')
                    )
                    alert = Alert.objects.create(
                        user=data.get('alertto'),
                        clap=instance
                    )
                    message = {"message": "successfully posted"}
                    return message
            else :
                clap = data.get('clapinstance')
                clap.delete()
                message = {"message": "successfully deleted"}
                return message

        else :
            message = data.get('error')
            return ValidationError(message, code=400)


    class Meta :
        model = Clap
        fields = ('id', 'user', 'memo', 'comment', 'message')
        read_only_fields = ('message', )


class AlertSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Alert
        fields = '__all__'





# class MemoSerializer(serializers.ModelSerializer) :
#     uid = serializers.CharField(label='user id', write_only=True)
#     pid = serializers.CharField(label='project id', write_only=True)
#     mid = serializers.CharField(label='memo id', write_only=True, required=False)
#     pname = serializers.CharField(label='new project name', write_only=True, required=False)
#     group = serializers.CharField(label='allowed group', write_only=True, required=False)
#     contents = serializers.CharField(label='contents', write_only=True)
#     image = serializers.FileField(label='image', write_only=True, required=False)
#     message = serializers.CharField(read_only=True)
#
#     def create(self, data):
#         instance = Memo.objects.create(
#             user = data.get('user'),
#             project = data.get('project'),
#             contents = data.get('contents'),
#             image = data.get('image'),
#             number = data.get('number')
#         )
#         message = {"message": "successfully posted"}
#         return message
#
#     def partial_update(self, instance, data):
#         print('!')
#         if data.get('image') != None:
#             instance.contents = data.get('contents')
#             instance.image = data.get('image')
#         else:
#             instance.contents = data.get('contents')
#         instance.save()
#         message = {"message": "successfully updated"}
#         return message
#
#     class Meta:
#         model = Memo
#         fields = ('uid', 'pid', 'mid', 'pname', 'group', 'contents', 'image', 'message', )
#         read_only_fields = ('message', )

