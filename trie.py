class M_Trie():
    def __init__(self):
        self.root = {"children":{}, "endOfWord": False}
        self._mtrie_initialize()
    
    def _mtrie_initialize(self):
        with open("word_list.txt", "r") as f:
            words = f.readlines()
        words = [word[:len(word)-1] for word in words]
        self.insert_words(words)
    
    def insert_words(self, words):
        def insert_recursive(current_node, current_index, word):
            if current_index == len(word):
                current_node["endOfWord"] = True
                return
            ch = word[current_index]
            if current_node["children"].get(ch) is None:
                current_node["children"][ch] = {"children":{}, "endOfWord": False}
            insert_recursive(current_node["children"][ch], current_index+1, word)
    
        for word in words:
            insert_recursive(self.root, 0, word)

    def search(self, word, starts_with=False):
        def search_recursive(current_node, current_index):
            if current_index == len(word):
                if starts_with:
                    return len(word) != 0
                return current_node["endOfWord"] 
            if current_node["children"].get(word[current_index]) is None:
                return False
            return search_recursive(current_node["children"].get(word[current_index]), current_index+1)
        
        return search_recursive(self.root, 0)

    def delete_word(self, word):
        def deleteWord_recursive(current_node, current_index):
            if current_index == len(word):
                if current_node["endOfWord"]:
                    current_node["endOfWord"] = False
                return True if len(current_node) == 0 else False

            node = current_node["children"].get(word[current_index])

            if node is not None:
                to_delete = deleteWord_recursive(node, current_index+1)
                if to_delete:
                    current_node["children"].pop(word[current_index])
                return True if len(current_node) == 0 else False
            return False

        deleteWord_recursive(self.root, 0)
    
    def get_all_words(self):
        words = []
        def getWord_recursive(current_node, sofar):
            if current_node.get("endOfWord"):
                words.append(sofar)
            for ch, children in current_node.get("children").items():
                getWord_recursive(children, sofar+ch)
        
        getWord_recursive(self.root, "")
        return words

def main():
    mtrie = M_Trie()
    words1 = mtrie.get_all_words()
    print(len(words1))
    print(f'is empty word present {mtrie.search("",True)}')
    mtrie.delete_word("ZWITTERIONI")
    mtrie.delete_word("ZWITTER")
    mtrie.delete_word("ZWITTERIONIC")
    mtrie.delete_word("ZWITTERION")
    mtrie.delete_word("A")
    mtrie.delete_word("AA")
    mtrie.delete_word("AAB")
    print(f'word AAL is present {mtrie.search("AAL",True)}')
    words2 = mtrie.get_all_words()
    print(len(words2))
    words2_dict = {word:True for word in words2}
    for word in words1:
        if words2_dict.get(word) is None:
            print(word) 
    with open("test.txt", 'w') as w:
        for word in words2:
            w.write(word+"\n")


if __name__ == "__main__":
    main()