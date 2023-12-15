class SimpleQueue:
    def __init__(self, max_size = 100):
        self._items = []
        self._max_size = max_size

    def push(self, item):
        if len(self._items) >= self._max_size:
            self._items.pop(0)  # 移除最旧的元素
        self._items.append(item)

    def pop(self):
        if self._items:
            return self._items.pop(0)
        return None

    def empty(self):
        return not self._items
    
    def size(self):
        return len(self._items)
    
    def clear(self):
        self._items.clear()  # 清空队列