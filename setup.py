#!/usr/bin/env python3  
import os
import pathlib

from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()  

# Version: use PACKAGE_VERSION env (set by CI) or fallback to default
# CI can set e.g. 1.2.0.dev run_number or 1.2.0 for tagged releases
_default_version = "1.2.0"
version = os.environ.get("PACKAGE_VERSION", _default_version)

# Get the long description from the README file  
long_description = (here / "README.md").read_text(encoding="utf-8")  

# Get a list of requirements  
requirements = [i.strip() for i in open("requirements.txt").readlines()]  

setup(
      name="pygoat",  
      version=version,  
      description="Intentionally vuln web Application Security in django",  
      long_description=long_description,  
      long_description_content_type="text/markdown",  
      url="https://github.com/adeyosemanputra/pygoat",  
      classifiers=[  
            "Programming Language :: Python :: 3",
      ],
      packages=find_packages(exclude="tests"),
      python_requires=">=3.7, <4",
      install_requires=requirements,
)
