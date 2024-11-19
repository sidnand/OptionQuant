from setuptools import setup, find_packages

setup(
    name="OptionQuant",
    version="0.1.0",
    description="A package for options trading strategies and analysis",
    author="Siddharth Nand",
    author_email="snand233@gmail.com",
    url="https://github.com/sidnand/OptionQuant",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "matplotlib",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)