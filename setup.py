from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in csc_hr/__init__.py
from csc_hr import __version__ as version

setup(
	name="csc_hr",
	version=version,
	description="HR Application for Corner Steel",
	author="ithead@ambibuzz.com",
	author_email="ithead@ambibuzz.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
