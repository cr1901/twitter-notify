# Always prefer setuptools over distutils
from setuptools import setup
# To use a consistent encoding


setup(
    name="Twitter Notify",
    version=1,
    description="Twitter Notification Frontend",
    author="William D. Jones",
    author_email="thor0505@comcast.net",
    license="BSD",
    packages=["tnotify"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        ],
    include_package_data=True,
    install_requires=["tweepy", "colorama"],
    zip_safe=False
)
