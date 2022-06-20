from setuptools import setup, find_packages

from ovl import __version__


with open("README.md", "r") as read_me:
    long_description = read_me.read()

SERIALIZATION = []
PRECOMPILED_OPENCV = ["opencv-python"]
FRC_EXTRA_PACKAGES = ["pynetworktables"] + PRECOMPILED_OPENCV + SERIALIZATION

extra_requirements = {
    "cv": PRECOMPILED_OPENCV,
    "frc": FRC_EXTRA_PACKAGES,
}

setup(
    name="ovl",
    packages=find_packages(),
    version=__version__,
    license="apache-2.0",
    author="SerpentBit",
    author_email="ovl.contact.help@gmail.com",
    description="A modular and versatile Python package for computer vision"
                " object detection pipelines tailored for robotics applications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SerpentBit/ovl",
    install_requires=["numpy"],
    extras_require=extra_requirements,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows"
    ]
)
