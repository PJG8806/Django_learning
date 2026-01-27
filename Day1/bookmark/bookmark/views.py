from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from bookmark.models import Bookmark

def bookmark_list(request):
    bookmarks = Bookmark.objects.all() # DB Bookmark테이블값 다 가져온다
    # objects.filter sql에서 where문 출력은 무조건 리스트로 출력한다
    # filter(컬럼명__gte 넣으면 이상이라는 조건, __gt는 초과
    # filter(컬럼명__lte 넣으면 이하이라는 조건, __lt는 미만
    # filter(컬럼명__icontains='' sql문에 like문 %%
    context = {
        'bookmarks': bookmarks
    }
    # return HttpResponse("<h1>북마크 리스트 페이지입니다.</h1>")
    return render(request, 'bookmark_list.html', context)

def bookmark_detail(request, pk):
    # try:
    #     bookmark = Bookmark.objects.get(pk=pk)
    # except:
    #     raise Http404

    bookmark = get_object_or_404(Bookmark, pk=pk) # 오류시 404 리턴

    context = {'bookmark': bookmark} # pk 값이면 이름을 pk 값으로 받는다
    return render(request, 'bookmark_detail.html', context)