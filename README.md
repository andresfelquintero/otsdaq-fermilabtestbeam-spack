Spack content for otsdaq-fermilab package.
It is set to install the contents on https://gitlab.cern.ch/otsdaq/otsdaq_fermilabtestbeam .

It includes some changes for newer versions of Spack. 
Particularly it now has to include this line
from spack.package import *  
because otherwise it won't get all these packages as it did before.
It also has to set a dependance on artdaq and artdaq-core.

Ideally this will be downloaded before installing the complete otsdaq-fermilabtestbeam package. 
