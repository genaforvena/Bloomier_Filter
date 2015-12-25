class SingletonFindingTweaker:
    def __init__(self, keys, hasher):
        self._keys = keys
        self._hasher = hasher

        hashes_seen = {}
        self._non_singletons = {}

        for k in keys:
            neighborhood = hasher.get_neighborhood(k)

            self._non_singletons += neighborhood & hashes_seen
            hashes_seen += neighborhood

    def tweak(self, key):
        neighborhood = self._hasher.get_neighborhood(key)
        for i in len(neighborhood):
            if neighborhood[i] not in self._non_singletons:
                return i

        return -1
