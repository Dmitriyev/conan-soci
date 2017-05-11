from conans import ConanFile, CMake, tools
import os


class SociConan(ConanFile):
    name = "SOCI"
    version = "3.2.3"
    license = "Boost Software License - Version 1.0"
    url = ""
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False],
               "with_db2": [True, False],
               "with_firebird": [True, False],
               "with_mysql": [True, False],
               "with_odbc": [True, False],
               "with_oracle": [True, False],
               "with_postgresql": [True, False],
               "with_sqlite3": [True, False]}
    default_options = "shared=False", "with_db2=False", "with_firebird=False",\
        "with_mysql=False", "with_odbc=False", "with_oracle=False",\
        "with_postgresql=False", "with_sqlite3=False"
    generators = "cmake"

    def source(self):
        tools.download(
            "https://github.com/SOCI/soci/archive/{}.tar.gz".format(self.version),
            "source.tar.gz")
        tools.unzip("source.tar.gz", ".")
        tools.replace_in_file("soci-{}/src/CMakeLists.txt".format(self.version),
                              "project(SOCI)", '''project(SOCI)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)
        self.build_dir = "./"

        cmake.definitions["WITH_DB2"] = "ON" if self.options.with_db2 else "OFF"
        cmake.definitions["WITH_FIREBIRD"] = "ON" if self.options.with_firebird else "OFF"
        cmake.definitions["WITH_MYSQL"] = "ON" if self.options.with_mysql else "OFF"
        cmake.definitions["WITH_ODBC"] = "ON" if self.options.with_odbc else "OFF"
        cmake.definitions["WITH_ORACLE"] = "ON" if self.options.with_oracle else "OFF"
        cmake.definitions["WITH_POSTGRESQL"] = "ON" if self.options.with_postgresql else "OFF"
        cmake.definitions["WITH_SQLITE3"] = "ON" if self.options.with_sqlite3 else "OFF"

        cmake.definitions["BUILD_SHARED_LIBS"] = "ON" if self.options.shared else "OFF"
        cmake.definitions["CMAKE_BUILD_TYPE"] = self.settings.build_type
        cmake.definitions["CMAKE_INSTALL_PREFIX"] = "{}/install".format(self.build_dir)

        cmake.configure(source_dir="soci-{}/src".format(self.version),
                        build_dir=self.build_dir)
        cmake.build(target="install")

    def package(self):
        self.copy("*.h", dst="include", src="install/include")
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["soci_core",
                              "soci_empty"]

        if self.options.with_db2:
            self.cpp_info.libs.append("soci_db2")

        if self.options.with_firebird:
            self.cpp_info.libs.append("soci_firebird")

        if self.options.with_mysql:
            self.cpp_info.libs.append("soci_mysql")

        if self.options.with_odbc:
            self.cpp_info.libs.append("soci_odbc")

        if self.options.with_oracle:
            self.cpp_info.libs.append("soci_oracle")

        if self.options.with_postgresql:
            self.cpp_info.libs.append("soci_postgresql")

        if self.options.with_sqlite3:
            self.cpp_info.libs.append("soci_sqlite3")