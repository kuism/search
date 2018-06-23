import os
module_dir = os.path.dirname(__file__)  # get current directory
from search.spelling_corrector import correction

def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


class TrieNode:
    def __init__(self):
        self.children = {}
        self.word = None  # it will store at end of the word

    def __insert__(self, word, frequency, pos=0):
        """ Insert A word In The Trie"""
        letter = word[pos]
        if letter not in self.children:
            self.children[letter] = TrieNode()

        # when the string reaches its end
        # the end node will store the word
        if pos + 1 == len(word):
            self.children[letter].word = {
                "w": word,
                "f": frequency
            }
        else:
            self.children[letter].__insert__(word, frequency, pos+1)

        return True

    def __get_all__(self, text=None):
        """ Get All Words In The Trie"""
        x = []

        # return all words recursievely
        for key, node in self.children.items():
            if node.word is not None:
                x.append(node.word)

            x += node.__get_all__(text)
        return x

    # this will calculate the edit distance of a string from a given text
    # it gives no of edits requried to make str2 from str1
    def __edit_distance__(self, str1, str2, m, n):
        # Create a table to store results of subproblems
        dp = [[0 for x in range(n + 1)] for x in range(m + 1)]

        for i in range(m + 1):
            for j in range(n + 1):

                # If first string is empty, only option is to
                # isnert all characters of second string
                if i == 0:
                    dp[i][j] = j  # Min. operations = j

                # If second string is empty, only option is to
                # remove all characters of second string
                elif j == 0:
                    dp[i][j] = i  # Min. operations = i

                # If last characters are same, ignore last char
                # and recur for remaining string
                elif str1[i - 1] == str2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]

                # If last character are different, consider all
                # possibilities and find minimum
                else:
                    dp[i][j] = 1 + min(dp[i][j - 1],  # Insert
                                       dp[i - 1][j],  # Remove
                                       dp[i - 1][j - 1])  # Replace

        return dp[m][n]

    def __search__(self, text, pos=0):
        """ Search For A string in Trie"""
        if pos < len(text):
            resp = []
            if text[pos] in self.children:
                return resp + self.children[text[pos]].__search__(text, pos+1)
            else:
                # if the item does'nt matches any children
                # it will get all the words from the corresponding node
                # and will calculate the edit distance from the search string
                resp = self.__get_all__(text)
                for item in resp:
                    item['edit_distance'] = self.__edit_distance__(item["w"], text, len(item["w"]), len(text))
                resp = sorted(resp, key=lambda x: (x["edit_distance"], -x["f"], len(item["w"])))
                return resp
        else:
            resp = self.__get_all__(text)
            if self.word is not None and self.word["w"] == text:
                resp = [self.word] + resp
            return resp


class SuffixTrieNode:
    # words will store the words which are ending with the prefix
    def __init__(self):
        self.children = {}
        self.words = []  # it will store words

    def __insert__(self, word, original_word, frequency, pos=0):
        """ Insert A word In The Trie"""
        letter = word[pos]
        if letter not in self.children:
            self.children[letter] = SuffixTrieNode()

        if pos + 1 == len(word):
            self.children[letter].words.append({
                "w": original_word,
                "f": frequency
            })
        else:
            self.children[letter].__insert__(word, original_word, frequency, pos+1)

        return True

    def __get_all__(self, text=None):
        """ Get All Words In The Trie"""
        x = []

        for key, node in self.children.items():
            if len(node.words) > 0:
                x = x + node.words

            x += node.__get_all__(text)
        return x

    def __search__(self, text, pos=0):
        """ Search For A string in Trie"""
        if pos < len(text):
            resp = []
            if text[pos] in self.children:
                return resp + self.children[text[pos]].__search__(text, pos+1)
            else:
                return []
        else:
            resp = self.__get_all__(text)
            if len(self.words) > 0:
                resp = self.words + resp
            return resp

@singleton
class Trie:
    def __init__(self):
        print("trie creating")
        self.root = TrieNode()
        self.suffixNode = SuffixTrieNode()

        file_path = os.path.join(module_dir, 'word_search.tsv')
        file = open(file_path, 'r')
        for line in file:
            word, frequency = line[0:-2].split("\t")
            self.insert(word, int(frequency))
            for i in range(1, len(word)-3):
                if len(word[i:]) >= 3:
                    self.suffix_insert(word[i:], word, int(frequency))

    def insert(self, word, frequency):
        self.root.__insert__(word, frequency)

    def suffix_insert(self, word, originalWord, frequency):
        self.suffixNode.__insert__(word, originalWord, frequency)

    def search(self, text):
        # it will search for a corrected text
        result = self.root.__search__(correction(text))
        # result = self.root.__search__(text)
        suffix_result = self.suffixNode.__search__(text)
        return result + suffix_result




# this will create the Trie Node
Trie()