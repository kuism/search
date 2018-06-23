from rest_framework import serializers
from search.models import Search


class SearchSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Search
        fields = '__all__'
