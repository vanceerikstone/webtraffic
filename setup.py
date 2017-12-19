from setuptools import setup

setup(name='webtraffic',
      version='0.1',
      description='Parse web traffic stats',
      url='http://github.com/lancetarn/webtraffic',
      author='Lance Erickson',
      author_email='lancetarn@gmail.com',
      license='MIT',
      packages=['webtraffic'],
      entry_points={
          "console_scripts": ['webtraffic=webtraffic.cli:main']
      },
      install_requires=[
          "pandas",
          "requests",
          "xmltodict",
      ],
      zip_safe=False)
