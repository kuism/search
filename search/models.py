from search.trienode import Trie
from django.db import models


class Search(models.Model):

    def search_text(self, text):
        node = Trie()
        results, suffix_results = node.search(text)
        suffix_results = sorted(suffix_results, key=lambda x: (-x["f"], len(x["w"])))
        if len(results) > 0 :
            if results[0]['w'] == text:
                item = results[0]
                results = [item] + sorted(results[1:], key=lambda x: (-x["f"], len(x["w"])))
            else:
                results = sorted(results, key=lambda x: (-x["f"], len(x["w"])))

        response = {
            "count":{
                "prefixMatches": len(results),
                "substringMatches": len(suffix_results)
            }
        }

        # formatting the results to contain items from bot suffix and prefix results
        if len(results) >= 15 and len(suffix_results) >= 10:
            response["matches"] = results[0:15] + suffix_results[0:10]
        elif len(results) >= 15 and len(suffix_results) < 10:
            response["matches"] = results[0:(25-len(suffix_results))] + suffix_results
        else:
            response["matches"] = (results + suffix_results)[0:25]

        return response