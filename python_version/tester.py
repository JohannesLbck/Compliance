from hashmap import HashTable

hash_t = HashTable(20)

hash_t.load_disk("None.json")
print(hash_t)

hash_t.insert("Test", "value")
print(hash_t)
print()
hash_t.insert("Test1", "value")
print(hash_t)
print()
print("exists Test1?")
print(hash_t.exists("Test1"))
print("exists Test2?")
print(hash_t.exists("Test2"))
hash_t.delete("Test1")
print("exists Test1 after delete?")
print(hash_t.exists("Test1"))
print("get Test?")
print(hash_t.get("Test"))


hash_t.save_disk("Test.json")

hash_t.delete("Test")
print("exists Test after delete?")
print(hash_t.exists("Test"))
hash_t.load_disk("Test.json")
print("exists Test after loading the old version from file?")
print(hash_t.exists("Test"))
