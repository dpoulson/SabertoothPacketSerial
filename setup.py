from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='SabertoothPacketSerial',
      version='0.1',
      description='Library for Dimenson Engineering Sabertooth speed controller',
      url='https://github.com/dpoulson/SabertoothPacketSerial',
      author='Darren Poulson',
      author_email='darren.poulson@gmail.com',
      license='GPL',
      packages=['SabertoothPacketSerial'],
      zip_safe=False)
