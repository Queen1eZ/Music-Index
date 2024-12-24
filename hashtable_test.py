from hashtable import *

import pytest


class TestHashtable:

    def test_create(self):
        hashtable = Hashtable()
        assert hashtable.num_buckets == 9  ## Default
        assert hashtable.num_elements == 0
        assert hashtable.buckets is not None
        assert len(hashtable.buckets) == 9

    def test_create_non_default_size(self):
        num_buckets = 5
        hashtable = Hashtable(num_buckets)
        assert hashtable.num_buckets == num_buckets  ## Default
        assert hashtable.num_elements == 0
        assert hashtable.buckets is not None
        assert len(hashtable.buckets) == num_buckets

    def test_insert_correct_bucket(self):
        hashtable = Hashtable(5)
        key = 1
        value = "testing"
        target_bucket = hash(key) % hashtable.num_buckets
        hashtable.put(key, value)
        assert len(hashtable.buckets[target_bucket]) == 1
        assert hashtable.buckets[target_bucket][0].value == "testing"
        assert hashtable.buckets[target_bucket][0].key == 1

    def test_put_two_values(self):
        """(10pts) Test overwriting a value for an existing key."""
        hashtable = Hashtable(5)
        key = 1
        hashtable.put(key, "a")
        hashtable.put(key, "b")
        assert hashtable.get(key) == "b"  # Value should be updated
        assert hashtable.num_elements == 1  # Element count should remain the same

    def test_put_multiple_items(self):
        """Test inserting multiple items with no hash collisions."""
        hashtable = Hashtable(5)
        hashtable.put(0, 'testing1')
        hashtable.put(8, 'testing2')
        hashtable.put(25, 'testing3')

        # Verify each item is stored in the correct bucket
        for key, value in [(0, 'testing1'), (8, 'testing2'), (25, 'testing3')]:
            target_bucket = hash(key) % hashtable.num_buckets
            # Find the KeyValuePair with the expected key
            item = [kvp for kvp in hashtable.buckets[target_bucket] if kvp.key == key][0]
            # print(item)
            assert item is not None
            assert item.value == value
        assert hashtable.num_elements == 3

    def test_remove(self):
        hashtable = Hashtable(5)
        key = 1
        value = "testing"
        target_bucket = hash(key) % hashtable.num_buckets
        hashtable.put(key, value)
        assert len(hashtable.buckets[target_bucket]) == 1
        assert hashtable.buckets[target_bucket][0].value == "testing"
        assert hashtable.buckets[target_bucket][0].key == 1

        removed_kvp = hashtable.remove(1)
        assert removed_kvp.key == 1
        assert removed_kvp.value == "testing"
        assert len(hashtable.buckets[target_bucket]) == 0
        assert hashtable.num_elems() == 0
        assert hashtable.num_elements == 0

    def test_remove_nonexistent_key(self):
        hashtable = Hashtable(5)
        key = 1
        value = "testing"
        target_bucket = hash(key) % hashtable.num_buckets
        hashtable.put(key, value)
        assert len(hashtable.buckets[target_bucket]) == 1
        assert hashtable.buckets[target_bucket][0].value == "testing"
        assert hashtable.buckets[target_bucket][0].key == 1

        with pytest.raises(KeyError):
            removed_kvp = hashtable.remove(3)

    def test_get_existing_key(self):
        """ Test retrieving an existing key."""
        hashtable = Hashtable(5)
        hashtable.put(10, "testing")
        assert hashtable.get(10) == "testing"

    def test_get_non_existent_key(self):
        hashtable = Hashtable(5)
        key = 1
        value = "testing"
        target_bucket = hash(key) % hashtable.num_buckets
        hashtable.put(key, value)
        assert len(hashtable.buckets[target_bucket]) == 1
        assert hashtable.buckets[target_bucket][0].value == "testing"
        assert hashtable.buckets[target_bucket][0].key == 1

        with pytest.raises(KeyError):
            value = hashtable.get(15)

    def test_get_with_collision(self):
        """Test retrieving items when there are collisions."""
        hashtable = Hashtable(1)  # Force all keys into the same bucket
        hashtable.put(1, "value1")
        hashtable.put(2, "value2")
        hashtable.put(3, "value3")

        # Check retrieval of each key
        assert hashtable.get(1) == "value1"
        assert hashtable.get(2) == "value2"
        assert hashtable.get(3) == "value3"

    ## This is just for sanity checking; it helps us ensure that we
    ##   update Hashtable.num_elements in all the right places
    def test_num_elems(self):
        hashtable = Hashtable(5)
        hashtable.put(1, "testing")
        assert hashtable.num_elems() == 1
        assert hashtable.num_elems() == hashtable.num_elements

        hashtable.put(2, "testing")
        assert hashtable.num_elems() == 2
        assert hashtable.num_elems() == hashtable.num_elements

    def test_resize(self):
        hashtable = Hashtable(3)

        assert hashtable.num_elements == 0
        assert hashtable.num_buckets == 3

        for i in range(8):
            hashtable.put(i, f"testing{i}")
            assert hashtable.num_elements == i + 1
            assert hashtable.num_buckets == 3

        for i in range(8, 20):
            hashtable.put(i, f"testing{i}")
            print(hashtable.num_elements, i)
            assert hashtable.num_elements == i + 1
            assert hashtable.num_buckets == 27

        for i in range(20):
            value = hashtable.get(i)
            assert value == f"testing{i}"

    def test_resize_triggered_after_remove(self):
        """Test that resizing still occurs after a key is removed when the threshold is exceeded."""
        hashtable = Hashtable(2)

        # Add items to reach just below the resize threshold
        for i in range(5):  # With alpha=3, threshold for resizing is 3 * 2 = 6
            hashtable.put(i, f"value{i}")

        # Verify no resize yet
        initial_num_buckets = hashtable.num_buckets
        assert initial_num_buckets == 2

        # Remove an item and then add a new item to reach the threshold
        hashtable.remove(0)
        hashtable.put(5, "value5")  # Now we are at threshold again
        hashtable.put(6, "value6")
        # Check if resizing occurred as expected after reaching the threshold
        assert hashtable.num_buckets > initial_num_buckets

        # Verify that all elements are still retrievable
        for i in range(1, 7):
            assert hashtable.get(i) == f"value{i}"


class TestHashtableIterator():

    def test_basic(self):
        bucket1 = [11, 12, 13]
        bucket2 = [14]
        bucket3 = [15, 16]
        bucket4 = []
        bucket5 = [17, 18, 19, 110]

        results = [11, 12, 13, 14, 15, 16, 17, 18, 19, 110]

        hashtable = Hashtable(5)
        ## NOTE: I'm "breaking the abstraction" so we can test the enumerator specifically
        hashtable.buckets = [bucket1, bucket2, bucket3, bucket4, bucket5]
        for index, item in enumerate(hashtable):
            assert item == results[
                index]  ## The items being returned here aren't KVPs, just numbers, because I broke the abstraction with the buckets

    def test_basic_iterator(self):
        hashtable = Hashtable()
        for i in range(10):
            hashtable.put(i, f"value{i}")

        ## We want to check that the iterator returns all the elements, and none that aren't in there
        seen = [False] * 10
        for index, item in enumerate(hashtable):
            assert item.value == f"value{item.key}"
            if seen[item.key]:
                assert False  ## This means we are seeing a KVP multiple times
            else:
                seen[item.key] = True
        ## Ensures that all items were seen
        for item in seen:
            assert item
