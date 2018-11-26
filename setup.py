from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='SabertoothPacketSerial',
      version='0.2.2',
      description='Library for Dimenson Engineering Sabertooth speed controller',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/dpoulson/SabertoothPacketSerial',
      author='Darren Poulson',
      author_email='darren.poulson@gmail.com',
      license='GPL',
      packages=setuptools.find_packages(),
      zip_safe=False)
