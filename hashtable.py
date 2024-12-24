"""
Hashtable and supporting classes.
"""


class KeyValuePair:
    """
    A data class holding a key and a value, to be used with a Hashtable.
    """

    def __init__(self, key: str, value):
        self.key = key
        self.value = value


class Hashtable:
    """
    A Hashtable implementation, storing key/value pairs efficiently.
    """

    def __init__(self, num_buckets=9):
        """
        Create a new instance of a hashtable.
        :param num_buckets: The number of buckets to start with; defaults to 9.
        """
        self.alpha = 3  ## A decent alpha for a chaining hashtable
        """This is a 'target' value-- if the load factor ever gets bigger than this, resize. """
        self.num_buckets = num_buckets
        """Number of buckets ('chains') in this hashtable """
        self.num_elements = 0
        """Number of elements stored in this hashtable"""
        self.buckets = [[] for _ in range(self.num_buckets)]  ## List of lists
        """The buckets that store the data"""
        pass

    def put(self, key: str, value):
        """
        Put a Key/Value into the hashtable.
        :param key: The key
        :param value: The value to store with the key
        :return:
        """
        ## Use the Key to determine which bucket the data goes into, but store the data as a KeyValuePair.
        bucket_index = hash(key) % self.num_buckets
        for bucket in self.buckets[bucket_index]:
            if bucket.key == key:
                bucket.value = value
                return
        self.buckets[bucket_index].append(KeyValuePair(key, value))
        self.num_elements += 1

        if self.load_factor() >= self.alpha:
            self.resize()

    def get(self, key: str):
        """
        Given a key, return the value associated with it.
        If the key is not in the Hashtable, raise a KeyError.
        :param key: The key that the data is stored by.
        :return: The value associated with the given key.
        """
        ## Note: A KeyValuePair is stored in the Hashtable, but only return the *value*, not the KeyValuePair.
        bucket_index = hash(key) % self.num_buckets
        for bucket in self.buckets[bucket_index]:
            if bucket.key == key:
                return bucket.value

        raise KeyError

    def key_exists(self, key:str) -> bool:
        """
        If the provided key exists in the Hashtable, return True; otherwise return False.
        :param key: The key to look for in this Hashtable
        :return: True if the provided key exists in the Hashtable.
        """
        try:
            self.get(key)
            return True
        except KeyError:
            return False

    def load_factor(self):
        """
        Internal helper function to calculate the current load factor for this table.
        :return: The load factor for this table (number of elements stored divided by the number of buckets)
        """
        return self.num_elements / self.num_buckets

    def resize(self) -> None:
        """
        Resizes this Hashtable to improve performance.
        """
        ## If the load factor is > threshold
        ## Create a new hashtable
        new_num_buckets = self.num_buckets * 9
        new_hashtable = Hashtable(new_num_buckets)
        ## Take elements out of this hashtable and put them in the new hashtable
        for bucket in self.buckets:
            for pair in bucket:
                new_hashtable.put(pair.key, pair.value)
        ## Set self equal to the new hashtable
        self.__dict__.update(new_hashtable.__dict__) ## <--- This is how you "set slef equal to the new hashtable"

        ### DON'T DO THIS
        # new_buckets = [] * 25
        # for bucket in self.buckets:
        #     for elem in bucket:
        #         new_bucket = elem.key / 25
        #         new_buckets[new_bucket] = elem
        #
        # self.buckets = new_buckets

    def num_elems(self) -> int:
        """
        Calculates the actual number of elements in this Hashtable.
        Used for sanity-checking and testing.
        :return:
        """
        return self.num_elements

    def remove(self, key: str) -> KeyValuePair:
        """
        Removes the data associated with the provided Key from this Hashtable.
        Raise a KeyError if the key is not in the Hashtable.
        :param key: The key of which data to remove.
        :return: The KeyValuePair that was removed from this Hashtable.
        """
        bucket_index = hash(key) % self.num_buckets
        for i, bucket in enumerate(self.buckets[bucket_index]):
            if bucket.key == key:
                removed_kvp = self.buckets[bucket_index].pop(i)
                self.num_elements -= 1
                return removed_kvp
        raise KeyError

    def __iter__(self):
        """
        Helper function to provide easy iteration over the elements of this Hashtable.
        :return: A HashtableIterator that provides the elements in this Hashtable.
        """
        return HashtableIterator(self)
        pass

    def keys(self) -> [str]:
        """
        Returns a list of all the keys in this Hashtable.
        :return: A list of all the keys
        """
        return [item.key for index, item in enumerate(self)]


class HashtableIterator:
    """
    An iterator that provides iteration over all the elements in this Hashtable.
    """

    def __init__(self, hashtable):
        self.bucket_iterator = hashtable.buckets.__iter__()  ## Let us iterate through the buckets
        self.list_iterator = self.bucket_iterator.__next__().__iter__()

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return self.list_iterator.__next__()
        except StopIteration:
            ## No more elements in this bucket; go to the next one
            try:
                self.list_iterator = self.bucket_iterator.__next__().__iter__()
                return self.__next__()  ## Recursive call so we can move on from an empty bucket
            except StopIteration:
                ## No more buckets left to visit
                raise StopIteration
