
from distutils.core import setup

setup(
    name='dayone-journal-py',
    version='0.0.1dev',
    author="Rob Tillotson",
    author_email="rob@pyrite.org",
    url="http://github.com/robtillotson/dayone-journal-py",
    packages=['dayone','dayone/cli'],
    scripts=['scripts/dayone'],
    license="Python",
    long_description=open('README.txt').read(),
    requires=['baker','Markdown'],
    provides=['dayone'],
    )

