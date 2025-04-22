# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install otsdaq-fermitestbeam
#
# You can edit this file again by typing:
#
#     spack edit otsdaq-fermitestbeam
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

import os
import sys

from spack import *

def sanitize_environments(env, *vars):
    for var in vars:
        env.prune_duplicate_paths(var)
        env.deprioritize_system_paths(var)

class OtsdaqFermilabtestbeam(CMakePackage):
    """The toolkit is used to control the Ph2_ACF for the CMS tracker project."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://github.com/andresfelquintero/otsdaq_fermilabtestbeam"
    url = "https://github.com/andresfelquintero/otsdaq_fermilabtestbeam.git"
    git = "https://github.com/andresfelquintero/otsdaq_fermilabtestbeam.git"


#    homepage = "https://gitlab.cern.ch/otsdaq/otsdaq_fermilabtestbeam"
#    url = "https://gitlab.cern.ch/otsdaq/otsdaq_fermilabtestbeam.git"
#    git = "https://gitlab.cern.ch/otsdaq/otsdaq_fermilabtestbeam.git"

    #Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers("github_user1", "github_user2")

    #Add the SPDX identifier of the project's license below.
    # See https://spdx.org/licenses/ for a list.
    license("UNKNOWN")

    #Add proper versions and checksums here.
    #Branches master and develop for this repository are exactly the same
#    version('local', path='/home/aquinter/otsdaq/otsdaq_fermilabtestbeam')
#    print(">>> DEBUG: Using custom package.py for otsdaq-fermilabtestbeam")

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
#    depends on("otsdaq-suite")

    #def cmake_args(self):
    #    # FIXME: Add arguments other than
    #    # FIXME: CMAKE_INSTALL_PREFIX and CMAKE_BUILD_TYPE
    #    # FIXME: If not needed delete this function
    #    args = []
    #    return args
    
    def cmake_args(self):
        args = []

    # Add dependencies that provide CMake config files via CMAKE_PREFIX_PATH
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
