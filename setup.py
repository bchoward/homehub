import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
install_requires = [
    'hcsr04sensor',
    'pypinsobj',
    'picamera',
    'SQLAlchemy',
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

