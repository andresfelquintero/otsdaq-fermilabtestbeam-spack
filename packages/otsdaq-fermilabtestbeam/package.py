import os
import sys

from spack import *
from spack.package import *


def sanitize_environments(env, *vars):
    for var in vars:
        env.prune_duplicate_paths(var)
        env.deprioritize_system_paths(var)

class OtsdaqFermilabtestbeam(CMakePackage):
    """The toolkit is used to control the Ph2_ACF for the CMS tracker project."""

    homepage = "https://github.com/andresfelquintero/otsdaq_fermilabtestbeam"

    version("develop", preferred=True)
    version('master', branch='master', submodules=True, get_full_repo=True)
    version("latest", branch="master", submodules=True, get_full_repo=True)
    version("frozen", commit="b54ee85b5f5ebe1f3ca86d8365a93ed4d1e59ec9", submodules=True, get_full_repo=True)

    print("We are using these dependencies, check me out #2")
    #Add dependencies if required.
    depends_on("cetmodules", type="build")
    depends_on("otsdaq")
    depends_on("otsdaq-utilities")
    depends_on("root +x +threads +tmva")
    depends_on("otsdaq-components")
    depends_on("trace")
    depends_on("epics-base")
    depends_on("fhicl-cpp")
    depends_on("xerces-c")
    depends_on("messagefacility")
    depends_on("artdaq-core")
    depends_on("artdaq")
    
    def cmake_args(self):
        args = []

        deps = [
            "messagefacility",
            "fhicl-cpp",
            "cetmodules",
            "otsdaq",
            "otsdaq-utilities",
            "otsdaq-components",
            "xerces-c",
            "trace"
        ]

        for dep in deps:
            args.append(self.define("CMAKE_PREFIX_PATH", self.spec[dep].prefix))

        return args


    def setup_build_environment(self, env):
        env.set("OTSDAQ_CMSTRACKER_DIR", self.prefix)
        env.prepend_path("LD_LIBRARY_PATH", self.spec["messagefacility"].prefix.lib)

    def setup_run_environment(self, env):
        prefix = self.prefix
        # Set the main directory where we can find the burnin box installed package
        env.set("OTSDAQ_CMSTRACKER_DIR", prefix)
        # Ensure we can find the libraries
        env.set("OTSDAQ_CMSTRACKER_LIB", prefix.lib)
        # Ensure we can find the binaries
        env.set("OTSDAQ_CMSTRACKER_BIN", prefix.bin)
        # Ensure we can find the plugin libraries.
        env.prepend_path("CET_PLUGIN_PATH", prefix.lib)


    def setup_dependent_run_environment(self, env, dependent_spec):
        prefix = self.prefix
        # Ensure we can find plugin libraries.
        env.prepend_path("CET_PLUGIN_PATH", prefix.lib)
