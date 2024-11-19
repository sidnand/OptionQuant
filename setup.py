from setuptools import setup, find_packages

setup(
    name="OptionQuant",
    version="1.0.0",
    author="Siddharth Nand",
    author_email="snand233@gmail.com",
    description="A package for options trading strategies and analysis",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sidnand/OptionQuant",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "matplotlib",
        "quantlib"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.13",
)