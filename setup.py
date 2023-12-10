from setuptools import find_packages, setup
from typing import List

HYPHEN_E_DOT = '-e .'
def get_requirements(file_path:str)->List[str]:
    '''
    This function will return a list of requirements
    '''
    requirements = []

    with open(file_path) as f:
        requirements = f.readlines()
        requirements = [requ.replace('\n'," ") for requ in requirements]
        

        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)
        return requirements

setup(
    name='student-performance-ml',
    version='0.1.0',
    author='Danny',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt'),
    author_email='dannychemm121@gmail.com',	
    url='https://github.com/dannychemm123/student-performance-ml',
    license='MIT',
    
)