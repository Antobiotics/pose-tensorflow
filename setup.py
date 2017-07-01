#try:
from setuptools import setup
#except:
    #from distutils.core import setup

try:
    import multiprocessing
except ImportError:
    pass

setup(
    name="pose",
    version='1.0.0',
    description="Pose Estimator",
    author_email="greg@dice.fm",
    url="https://github.com/antobiotics/pose",
    platforms="Posix; MacOS X; Windows",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
    ],
    packages=[
        "pose",
        "pose.dataset",
        "pose.demo",
        "pose.nnet",
        "pose.util"
    ],
    install_requires=[
    ],
    dependency_links=[
    ]
)
