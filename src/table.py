
class Table:

    _table: dict
    _neighbors: set

    def __init__(self):
        self._table = dict()
        self._neighbors = set()

    def set_table(self, id, vector, hop, neighbor=False):
        if neighbor: self._neighbors.add(id)
        self._table[id] = (vector, hop)

    def get_table(self):
        return self._table

    def get_table_value(self, key):
        return self._table[key]

    def get_neighbors(self):
        return self._neighbors

    def clear_neighbors(self):
        self._neighbors.clear()
