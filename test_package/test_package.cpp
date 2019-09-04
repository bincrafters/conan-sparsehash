#include <cassert>

#include <sparsehash/dense_hash_map>
#include <sparsehash/dense_hash_set>
#include <sparsehash/sparse_hash_map>
#include <sparsehash/sparse_hash_set>

void testSparseHashMap() {
    google::sparse_hash_map<int, int> sparseHashMap;

    // sparse_hash_map does not need set_empty_key configuration
    sparseHashMap.set_deleted_key(999);

    sparseHashMap[1] = 1;
    sparseHashMap[2] = 2;

    assert(sparseHashMap[1] == 1);
    assert(sparseHashMap[2] == 2);

    assert(sparseHashMap.find(2) != sparseHashMap.end());
    assert(sparseHashMap.find(3) == sparseHashMap.end());

    sparseHashMap.erase(2);
    assert(sparseHashMap.find(2) == sparseHashMap.end());
}

void testSparseHashSet() {
    google::sparse_hash_set<int> sparseHashSet;

    // sparse_hash_set does not need set_empty_key configuration
    sparseHashSet.set_deleted_key(999);

    sparseHashSet.insert(1);
    sparseHashSet.insert(2);

    assert(sparseHashSet.find(1) != sparseHashSet.end());
    assert(sparseHashSet.find(3) == sparseHashSet.end());
}

void testDenseHashMap() {
    google::dense_hash_map<int, int> denseHashMap;

    denseHashMap.set_empty_key(0);
    denseHashMap.set_deleted_key(999);

    denseHashMap[1] = 1;
    denseHashMap[2] = 2;

    assert(denseHashMap[1] == 1);
    assert(denseHashMap[2] == 2);

    assert(denseHashMap.find(2) != denseHashMap.end());
    assert(denseHashMap.find(3) == denseHashMap.end());

    denseHashMap.erase(2);
    assert(denseHashMap.find(2) == denseHashMap.end());
}

void testDenseHashSet() {
    google::dense_hash_set<int> denseHashSet;

    denseHashSet.set_empty_key(0);
    denseHashSet.set_deleted_key(999);

    denseHashSet.insert(1);
    denseHashSet.insert(2);

    assert(denseHashSet.find(1) != denseHashSet.end());
    assert(denseHashSet.find(3) == denseHashSet.end());
}

int main() {
    testDenseHashMap();
    testDenseHashSet();
    testSparseHashMap();
    testSparseHashSet();
}
