from django.apps import AppConfig
from django.db.models.signals import pre_save


class SearchConfig(AppConfig):
    name = 'search'

    def ready(self):
        print("readt called")
        from search.trienode import Trie
        node = Trie()
