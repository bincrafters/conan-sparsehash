from conans import AutoToolsBuildEnvironment, ConanFile, tools
import os


class SparsehashConan(ConanFile):
    name = "sparsehash"
    description = "The C++ associative containers"
    topics = ("conan", "libsparsehash", "dense_hash_map", "sparse_hash_map", "dense_hash_set", "sparse_hash_set")
    url = "https://github.com/bincrafters/conan-sparsehash"
    homepage = "https://github.com/sparsehash/sparsehash"
    license = "BSD-3-Clause"
    author = "Xiaoge Su <magichp|at|gmail.com>"
    
    _source_subfolder = "source_subfolder"
    _autotools = None
     
    def build_requirements(self):
        if tools.os_info.is_windows and "CONAN_BASH_PATH" not in os.environ and \
                tools.os_info.detect_windows_subsystem() != "msys2":
            self.build_requires("msys2/cci.latest")

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = "{}-{}-{}".format(self.name, self.name, self.version)
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_autotools(self):
        if not self._autotools:
            self._autotools = AutoToolsBuildEnvironment(self, win_bash=tools.os_info.is_windows)
            self._autotools.configure(configure_dir=os.path.join(self.build_folder, self._source_subfolder))
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
