from setuptools import setup, find_packages

setup(name='XKCDland',
      version='0.0.1',
      description='A XKCD inspired game',
      license='MIT',
      url='https://github.com/Nanoseb/XKCDLand',
      packages=find_packages(),
      scripts=['xkcdland'],
      install_requires=[
        "pygame",
        "numpy",
        "pillow",
      ]
)
