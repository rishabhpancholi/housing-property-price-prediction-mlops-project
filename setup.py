from setuptools import find_packages, setup
from typing import List

def get_requirements()-> List[str]:
    """
    This function will return the list of requirements

    """
    requirement_lst:List[str] = []
    try:
        with open('requirements.txt','r') as file:
            # Read lines from the file
            lines = file.readlines()
            # Process each line
            for line in lines:
                requirement = line.strip()
                # Ignore the empty lines and ignore -e .
                if requirement and requirement!="-e .":
                    requirement_lst.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file not found")

    return requirement_lst

setup(
    name='housing-property-price-prediction',
    version='0.1.0',
    description='Housing Property Price Predictor End-to-End MLOps Project',
    author='Rishabh Pancholi',
    author_email='rishabhpancholi134@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements()
)