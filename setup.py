from distutils.core import setup

setup(name='XKCDland',
      version='0.0.1',
      description='A XKCD inspired game',
      license='MIT',
      url='https://github.com/Nanoseb/XKCDLand',
      packages=['XKCDLand'],
      scripts=['xkcdland'],
      install_requires=["pygame", "numpy", "PIL", ]

)
