class InMemoryRepository:
    def __init__(self):
        self._items = {}
        self._next_id = 1

    def list(self):
        return list(self._items.values())

    def get(self, item_id):
        return self._items.get(item_id)

    def next_id(self):
        item_id = self._next_id
        self._next_id += 1
        return item_id

    def save(self, item):
        self._items[item.id] = item
        return item

    def delete(self, item_id):
        self._items.pop(item_id, None)
