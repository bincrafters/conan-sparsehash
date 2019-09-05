from conans import (
    AutoToolsBuildEnvironment, ConanFile, tools
)

import os
import os.path
import subprocess


SOURCE_URL = "https://github.com/sparsehash/sparsehash"


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
    name = "sparsehash"

    homepage = SOURCE_URL
    version = "2.0.3"
    license = "BSD-3-Clause"
    topics = ("conan", "libsparsehash",
              "dense_hash_map", "sparse_hash_map",
              "dense_hash_set", "sparse_hash_set")
    settings = ("os", "compiler", "build_type", "arch")

    author = "Xiaoge Su <magichp|at|gmail.com>"
    url = "https://github.com/xis19/conan-sparsehash"
    description = "Conan recipe for Google sparse hash library"

    options = {}
    default_options = {}

    generators = "cmake"

    exports = ["COPYING"]

    _source_subfolder = "_source_subfolder"

    def source(self):
        tools.get(
            "{homepage}/archive/sparsehash-{version}.tar.gz".format(
                homepage=self.homepage,
                version=self.version
            ),
            sha256="05e986a5c7327796dad742182b2d10805a8d4f511ad090da0490f146c1ff7a8c"
        )
        extracted_directory = "{}-{}-{}".format(
            self.name, self.name, self.version
        )
        os.rename(extracted_directory, self._source_subfolder)

    def build(self):
        with tools.chdir(self._source_subfolder):
            # Even this is a header_only package, we still need to run a build
            # in order to generate sparseconfig.h
            autotools = AutoToolsBuildEnvironment(self)
            autotools.configure()
            autotools.make()

            if self.develop:
                # Run the tests sparsehash
                for test in SPARSE_HASH_TEST_FILES:
                    subprocess.check_call(os.path.join('.', test))

    def package(self):
        # Sparsehash uses "COPYING" instead of "LICENSE"
        self.copy(
            pattern="COPYING",
            dst="licenses",
            src=self._source_subfolder
        )
        self.copy(
            "*",
            dst="include/sparsehash",
            src=os.path.join(self._source_subfolder, 'src', 'sparsehash')
        )

    def package_id(self):
        self.info.header_only()
