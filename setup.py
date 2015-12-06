import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

requires = [
    'sqlalchemy',
    'python-pycamera',
    'pybluez',
    ]

setup(name='homehub',
      version='0.1',
      description='homehub',
      classifiers=[
        "Programming Language :: Python",
        ],
      author='',
      author_email='',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='homehub',
      install_requires=requires,
      entry_points="""\
      """,
      )

