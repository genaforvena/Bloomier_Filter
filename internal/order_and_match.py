import sys

from internal.hasher import BloomierHasher
from internal.tweaker import SingletonFindingTweaker


class OrderAndMatchFinder:
    def __init__(self, keys, m, k, q, hash_seed_hint = sys.maxsize + 1):
        self._keys = keys
        self._m = m
        self._k = k
        self._q = q
        self._hash_seed = hash_seed_hint
        self._tau = []
        self._pi = []
        self._order_and_match
        self._hasher

    def find(self, timeout_ms):
        has_timed_out = False

        # TODO set timer to change has_timed_out value after timeout_ms

        self._hasher = BloomierHasher(self._hash_seed, self._m, self._k, self._q)

        for i in range(sys.maxsize):
            if self._find_match(self._keys):
                self._order_and_match = OrderAndMatch(self._hash_seed, self._pi, self._tau)
                return self._order_and_match

            self._hash_seed += 1

        return self._order_and_match

    def is_found(self):
        return self._order_and_match is not None

    def _find_match(self, remaining_keys):
        if not remaining_keys:
            return True

        pi_queue = []
        tau_queue = []

        tweaker = SingletonFindingTweaker(remaining_keys, self._hasher)

        for key in remaining_keys:
            iota = tweaker.tweak(key)
            if iota >= 0:
                pi_queue.add(key)
                tau_queue.add(iota)

        if not pi_queue:
            return False

        remaining_keys -= pi_queue

        if remaining_keys:
            if not self._find_match(remaining_keys):
                return False

        self._pi += pi_queue
        self._tau += tau_queue

        return True


class OrderAndMatch:
    def __init__(self, hash_seed, pi_list, tau_list):
        self.hash_seed = hash_seed
        self.pi_list = pi_list
        self.tau_list = tau_list
