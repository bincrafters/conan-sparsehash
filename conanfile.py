from conans import AutoToolsBuildEnvironment, ConanFile, tools
import os


class SparsehashConan(ConanFile):
    name = "sparsehash"
    version = "2.0.3"
    description = "Conan recipe for Google sparse hash library"
    homepage = "https://github.com/sparsehash/sparsehash"
    license = "BSD-3-Clause"
    topics = ("conan", "libsparsehash",
              "dense_hash_map", "sparse_hash_map",
              "dense_hash_set", "sparse_hash_set")
    author = "Xiaoge Su <magichp|at|gmail.com>"
    url = "https://github.com/bincrafters/conan-sparsehash"
    exports = ["LICENSE"]
    _autotools = None

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    def source(self):
        sha256="05e986a5c7327796dad742182b2d10805a8d4f511ad090da0490f146c1ff7a8c"
        tools.get("{}/archive/sparsehash-{}.tar.gz".format(self.homepage, self.version), sha256=sha256)
        extracted_directory = "{}-{}-{}".format(self.name, self.name, self.version)
        os.rename(extracted_directory, self._source_subfolder)

    def _configure_autotools(self):
        if not self._autotools:
            self._autotools = AutoToolsBuildEnvironment(self)
            self._autotools.configure(configure_dir=self._source_subfolder)
        return self._autotools

    def build(self):
        autotools = self._configure_autotools()
        autotools.make()

    def package(self):
        self.copy(pattern="COPYING", dst="licenses", src=self._source_subfolder)
        autotools = self._configure_autotools()
        autotools.install()
        tools.rmdir(os.path.join(self.package_folder, "lib"))
        tools.rmdir(os.path.join(self.package_folder, "share"))

    def package_id(self):
        self.info.header_only()
