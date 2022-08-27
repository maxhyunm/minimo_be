from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *
from apps.projects.views import *

memolist = MemoListView.as_view({
    'get' : 'retrieve'
})

memo = MemoView.as_view({
    'post' : 'create',
    'put': 'update',
})
onememo = MemoView.as_view({
    'delete': 'destroy'
})
comment = CommentView.as_view({
    'post' : 'create',
    'put': 'update',
})
onecmt = CommentView.as_view({
    'delete': 'destroy'
})
clap = ClapView.as_view({
    'post' : 'create'
})

prjlist = GetPrjView.as_view({
    'get' : 'retrieve'
})

alertcount = AlertView.as_view({
    'get' : 'retrieve'
})

alertdetail = AlertDetailView.as_view({
    'get' : 'retrieve'
})

urlpatterns = format_suffix_patterns([
    path('auth/', include('rest_framework.urls', namespace='restframework')),
    path('memolist/<int:uid>/', memolist, name='memolist'),             # memolist
    path('memo/', memo, name='postmemo'),                               # postmemo
    path('memo/', memo, name='editmemo'),                               # editmemo
    path('memo/<int:mid>/', onememo, name='deletememo'),                # deletememo
    path('comment/', comment, name='postcomment'),                      # postcomment
    path('comment/', comment, name='editcomment'),                      # editcomment
    path('comment/<int:cid>/', onecmt, name='deletecomment'),           # deletecomment
    path('clap/', clap, name='addclap'),                                # addclap
    path('prjlist/<int:uid>/', prjlist, name='prjlist'),                # projectlist
    path('alert/<int:uid>/', alertcount, name='alertcount'),            # alertcount
    path('alertdetail/<int:uid>/', alertdetail, name='alertdetail'),    # alertdetail
])
