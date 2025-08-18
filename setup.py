from setuptools import find_packages, setup

with open("README.md", "r", encoding = "utf-8") as f:
    long_description = f.read()

with open("requirements.txt", "r") as f:
    requirements = [lib.strip() for lib in f.readlines()]

setup(
    name = "housing-property-price-predictor",
    version = "0.1.0",
    author = "Rishabh Pancholi",
    author_email = "rishabhpancholi134@gmail.com",
    description = "Housing property price prediction ML pipeline",
    long_description = long_description,
    long_description_content_type="text/markdown",
    url = "https://github.com/rishabhpancholi/housing-property-price-prediction-mlops-project",
    packages = find_packages(),
    install_requires = requirements,
    python_requires = ">=3.8"
)