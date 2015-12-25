import sys


class ImmutableBloomierFilter:
    def __init__(self, dictionary, m, k, q, clss, timeout=0,
                 hash_seed_hint=0):
        self._m = m
        self._k = k
        self._q = q
        self._clss = clss

        self._table_entry_size = q / 8
        self._table = []

        if timeout != 0 and hash_seed_hint != 0:
            order_and_match_finder = OrderAndMatchFinder(dictionary.keys(), m, k, q, hash_seed_hint)
            order_and_match = order_and_match_finder.find(sys.maxint)
        elif timeout != 0:
            order_and_match_finder = OrderAndMatchFinder(dictionary.keys(), m, k, q)
            order_and_match = order_and_match_finder.find(timeout)
        elif hash_seed_hint != 0:
            order_and_match_finder = OrderAndMatchFinder(dictionary.keys(), m, k, q, hash_seed_hint)
            order_and_match = order_and_match_finder.find(sys.maxint)

        self._hash_seed = order_and_match.get_hash_seed()
        self._hasher = BloomierHasher(self._hash_seed, self._m, self._k, self._q)

        pi = order_and_match.get_pi()
        tau = order_and_match.get_tau()

        for i in len(pi):
            key = pi[i]
            value = dictionary[key]
            encoded_value = self._encode(value)

            neighborhood = self._hasher.get_neighbothood(key)
            mask = self._hasher.get_m(key)

            index_of_storage = neighborhood[tau[i]]
            # TODO init value to store
            value_to_store = []

            self._byte_array_xor(value_to_store, encoded_value)
            self._byte_array_xor(value_to_store, mask)

            neighborhood_set = {}
            for hash_value in neighborhood:
                neighborhood_set.add(hash_value)

            for hash_value in neighborhood_set:
                self._byte_array_xor(value_to_store, self._table[hash_value])

            self._table[index_of_storage] = value_to_store


    def get(self, key):
        pass
