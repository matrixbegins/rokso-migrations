from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.readlines()

long_description = 'Rokso migration package for mysql database migrations'

setup(
        name ='rokso',
        version ='0.1.0',
        author ='Ankur Pandey',
        author_email ='matrixbegins@gmail.com',
        url ='https://github.com/matrixbegins/rokso-migrations',
        description ='Rokso migration package for mysql database migrations.',
        long_description = long_description,
        long_description_content_type ="text/markdown",
        license ='MIT',
        packages = find_packages(),
        entry_points ={
            'console_scripts': [
                'rokso = rokso:main'
            ]
        },
        classifiers =(
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Dependent",
        ),
        keywords ='MySql, database-migration',
        install_requires = requirements,
        zip_safe = False
)