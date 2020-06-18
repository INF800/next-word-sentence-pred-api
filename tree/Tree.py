from tree.Words import words

class Node:
    def __init__(self, val, _ht, _rank=None):
        self.val = val
        self.children = {}
        # we will use ranks for two things,
        #   - to know if same word
        #   - to know popularity
        self._rank = _rank
        self._ht = _ht
        self._isDisappeared = False # track disappeared words [1 of 2]

class Tree:
    def __init__(self):
        self.root = Node('root', _ht=-1)
        self.q_rank = None # used by search

    def insert(self, data):
        """
        In this recursion,
            - initialize epmty root node
            - until there are no more lettrs in `word` to be inserted (in loop)
            - take root as `parent` and append child1
                - take child1 as `parent` and append child2
                    - take child2 as `parent` and append child3
                        ...
        """
        parent = self.root
        for idx, letter in enumerate(data[0]):
            if letter in parent.children:
                # track disappeared [2 of 2]
                parent.children[letter]._isDisappeared = True
                # - instead of overwriting, to parent, continue downwards - with NEXT letter
                # - overwrite _rank to know that it belongs to difft word BUT always overwrite
                #   the SMALLEST RANK! helpful
                parent = parent.children[letter]
                parent._rank = parent._rank if (parent._rank < data[1]) else data[1]
                continue
            parent.children[letter] = Node(letter, _rank=data[1], _ht=idx)
            parent = parent.children[letter]

    def traverse(self):
        self.__traverse(self.root)

    def __traverse(self, node):
        # base
        if node.children == {}:
            # ------------------------------------
            disappeared_tracker = f"<{'-'*60} Disappeared" if node._isDisappeared else ""
            prefix = (" "*node._ht) * 3 + "|__"
            print(prefix + node.val, node._rank, "END", disappeared_tracker) # -- END -- is appparent end
            # ------------------------------------
            return
        # ------------------------------------
        disappeared_tracker = f"<{'-'*60} Disappeared" if node._isDisappeared else ""
        prefix = (" "*node._ht) * 3 + "|__"
        print(prefix + node.val, node._rank, disappeared_tracker)
        # ------------------------------------
        # traverse recursively
        for child_node in node.children: 
            self.__traverse(node.children[child_node])

    def search(self, q_str):
        """
        We use logic that rank(q_str) always eq to rank(expecter_str) 
        => O(n') [n' - len of query not ecpected str]
        
        - i. find the rank(will be unique) of query str's final letter in seq.
        - ii. Suggest the word with same rank(same as idx) using list

        Note: 
            - we will store rank in `self.q_rank` of tree. 
            - If it is 'None' word not found
        """
        # write rank of final letter in seq. to `self.q_rank` 
        self.__search_rank(self.root, q_str)

    def __search_rank(self, node, q_str, CUR=0):
        if node.children == {}:
            self.q_rank = (node._rank, node.val)
            return

        self.q_rank = (node._rank, node.val)
        for child_node in node.children:
            if CUR<len(q_str):
                if node.children[child_node].val == q_str[CUR]:
                    self.__search_rank(node.children[child_node], q_str, CUR=CUR+1)

# 1. Initialize 
tree = Tree()
# 2. Build tree
for rank, word in enumerate(words):
    tree.insert((word, rank))