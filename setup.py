from setuptools import setup, find_packages
with open('readme.md', 'r') as f:
    long_description = f.read()
setup(
    name="cached_requests",
    version="0.1.4",
    author="ThefCraft",
    author_email="sisodiyalaksh@gmail.com",
    url="https://github.com/thefcraft/cached_requests",
    description="A Python library that provides a simple and effective caching layer for web requests.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "cached_requests": ["*.pyi", "py.typed"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["requests"]
)