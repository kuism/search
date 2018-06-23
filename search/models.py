from search.trienode import Trie
from django.db import models


class Search(models.Model):

    def search_text(self, text):
        node = Trie()
        results = node.search(text)
        if len(results) > 0 :
            if results[0]['w'] == text:
                item = results[0]
                return [item] + sorted(results[1:], key=lambda x: (-x["f"], len(x["w"])))
            else:
                return sorted(results, key=lambda x: (-x["f"], len(x["w"])))
        else:
            return []
