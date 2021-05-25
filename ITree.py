class ITree:
    def __init__(self, value=[], next=[], subNode=[]):
        # 节点的值
        self.value = value
        # 节点的子树
        self.next = next
        # 该节点下所有的值
        self.subNodes = subNode