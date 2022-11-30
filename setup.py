from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="main",
    version="0.1.0",
    description="Python implementation of a photomosaic generator",
    entry_points={'console_scripts': ['main = main.photomosaic:main']},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ],
    package_dir={"": "main"},
    packages=find_packages(where="main"),
    python_requires=">=3, <4",
    install_requires=[],
)
