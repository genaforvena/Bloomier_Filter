import hashlib


def _key_to_int_list(key):
    pass


class BloomierHasher:
    def __init__(self, hash_seed, m, k, q):
        self._hash_seed = hash_seed
        self._m = m
        self._k = k
        self._q = q

    def get_neighborhood(self, key):
        hashes = map(abs, _key_to_int_list(key))
        hashes = map(lambda x: x % self._m, hashes)
        return hashes

    def get_m(self, key):
        #TODO
        pass


class Hash:
    def __init__(self, key, hash_seed):
        self._data = bytearray()
        self._data.append(hash(key))

        self._salt = hash_seed

        self._md = hashlib.md5()

        self._buffer = list()
        self._top_off()

    def read(self):
        if not self._buffer:
            self._top_off()

        # TODO subtract Byte.MIN_VALUE from self._buffer.pop() call result.
        return self._buffer.pop()

    def _top_off(self):
        self._md.update()
        self._md.update(self._data)

        for b in self._md.digest():
            self._buffer.add(b)

        self._salt += 1

