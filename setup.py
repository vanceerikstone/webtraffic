from setuptools import setup

setup(name='web_traffic',
      version='0.1',
      description='Parse web traffic stats',
      url='http://github.com/lancetarn/web_traffic',
      author='Lance Erickson',
      author_email='lancetarn@gmail.com',
      license='MIT',
      packages=['web_traffic'],
      install_requires=[
          "pandas",
          "requests",
          "boto3",
      ],
      zip_safe=False)
