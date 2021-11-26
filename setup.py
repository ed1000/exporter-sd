#!/usr/bin/env python3

from setuptools import setup, find_packages


setup(
    name="osm_exporter_sd",
    description="OSM Exporter Service Discovery",
    long_description="OSM Exporter Service Discovery",
    version="v1.0.0",
    author="Eduardo Sousa",
    author_email="eduardo.sousa@canonical.com",
    maintainer="Canonical Ltd.",
    maintainer_email="eduardo.sousa@canonical.com",
    url="https://www.canonical.com",
    license="Apache 2.0",
    packages=find_packages(exclude=["temp", "local"]),
    include_package_data=True,
    setup_requires=["setuptools-version-command"],
)
