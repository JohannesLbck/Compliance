import json
import os

class VerTree:

    # Create empty bucket list of given size
    def __init__(self, size):
        self.size = size
        self.hash_table = self.create_buckets()

    def create_buckets(self):
        return [[] for _ in range(self.size)]

    # save to disk
    def save_disk(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.tree, f)
    # load from disk
    def load_disk(self, filename):
        if os.path.exists(filename):
            pass
        else:
            self.save_disk(filename)
    
    # check if a key exists in the hashmap
    def exists(self, key):
        pass

    # Insert values into hash map
    def insert(self, key, val):
        pass

    # Return searched value with specific key
    def get(self, key):
        pass

    # Remove a value with specific key
    def delete(self, key):
        pas
        passs

    # To print the items of hash map
    def __str__(self):
        return "".join(str(item) for item in self.hash_table)

