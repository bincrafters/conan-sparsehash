from conans import (
    AutoToolsBuildEnvironment, ConanFile, tools
)

import os
import subprocess


SPARSE_HASH_TEST_FILES = [
    "hashtable_test",
    "libc_allocator_with_realloc_test",
    "simple_compat_test",
    "simple_test",
    "sparsetable_unittest",
    "template_util_unittest",
    "type_traits_unittest"
]


class SparsehashConan(ConanFile):
    name = "libsparsehash"
    version = "2019.07.18"
    license = "MIT"
    author = "Xiaoge Su <magichp|at|gmail.com>"
    url = "https://github.com/xis19/conan-sparsehash"
    description = "Conan recipe for Google sparse hash library"
    topics = ("conan", "libsparsehash", "dense_hash_map", "sparse_hash_map", "dense_hash_set", "sparse_hash_set")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    exports = ["LICENSE"]

    def source(self):
        git = tools.Git("sparsehash")
        git.clone("https://github.com/sparsehash/sparsehash.git", "master")

    def build(self):
        with tools.chdir("sparsehash"):
            autotools = AutoToolsBuildEnvironment(self)
            autotools.configure()
            autotools.make()

            # Run the tests sparsehash
            for test in SPARSE_HASH_TEST_FILES:
                subprocess.check_call(os.path.join('.', test))

    def package(self):
        self.copy("*", dst="include/sparsehash", src="sparsehash/src/sparsehash")

    def package_id(self):
        self.info.header_only()
