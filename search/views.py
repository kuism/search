from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer

from search.models import Search


class SearchViewSet(viewsets.ModelViewSet):

    def list(self, request, *args, **kwargs):
        data = request.GET.copy()
        response = []
        if "word" in data:
            response = Search().search_text(data["word"])

        print(response)
        return Response({"data": response})

