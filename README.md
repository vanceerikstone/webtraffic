## Overview

This package contains a script can be used to iterate over a public bucket
of .csv files and stream them down for parsing. Does not currently support buckets
containing more than 1000 items.

Currently the transformation performed is hard-coded into the package.
This could be updated to allow on-the-fly configuration if necessary.
Other possible enhancements are filtering bucket objects by path or name.

## Installation

This package requires python 3.4+. Suggested installation is to
create a virtualenv for isolation. This process varies by platform,
but a common \*nix pattern to create a venv under the current directory
is:

```
$ python3 -m venv webtraffic-env
$ source ./webtraffic-env/bin/activate
$ pip install -e git://github.com/vanceerikstone/webtraffic/@v0.1.1#egg=webtraffic
```

Sorry Windows users; I do not have a machine available to verify the install for you.

## Usage
After installation, when the venv is active, there should be a 
`webtraffic` executable in your $PATH

`webtraffic -h` is available for help.

### List/verify objects in a bucket
`webtraffic -l my-bucket us-east-1`

### Process bucket contents to file
`webtraffic -o writeable/path/filename.csv my-bucket us-east-1`

