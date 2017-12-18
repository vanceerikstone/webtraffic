## Overview

This package contains a script can be used to iterate over a bucket
of .csv files and stream them down for parsing. Does not support buckets
containing more than 1000 items.

Currently the transformation performed is hard-coded into the package.
This could be updated to allow on-the-fly configuration if necessary

## Installation

This package requires python 3.4+. Suggested installation is to
create a virtualenv for isolation. This process varies by platform,
but a common *nix pattern to create a venv under the current directory
is:

`$ git clone https://github.com/vanceerikstone/webtraffic.git`
`$ cd webtraffic
`$ python3 -m venv env`
`$ source ./env/bin/activate`
`$ pip install -e .`

After installation, when the venv is active, there should be a 
`webtraffic` executable in the $PATH

`$ webtraffic -h` is available for help. 
