from setuptools import setup, find_packages, find_namespace_packages

with open('requirements.txt') as f:
    requirements = f.readlines()

long_description = 'Rokso migration package for mysql database migrations'

setup(
        name ='rokso',
        version ='0.1.15',
        author ='Ankur Pandey',
        author_email ='matrixbegins@gmail.com',
        url ='https://github.com/matrixbegins/rokso-migrations',
        description ='Rokso migration package for mysql database migrations.',
        long_description = long_description,
        long_description_content_type ="text/markdown",
        license ='MIT',
        packages=find_namespace_packages(include=['rokso', 'rokso.*', 'rokso.lib.*']),
        entry_points ={
            'console_scripts': [
                'rokso = rokso.rokso:main'
            ]
        },
        python_requires='>=3.3',
        classifiers = [
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Development Status :: 3 - Alpha",
            "Operating System :: POSIX :: Linux",
            "Operating System :: MacOS",
            "Operating System :: MacOS :: MacOS X",
            "Topic :: Database",
            "Programming Language :: Python :: 3.8",
        ],
        keywords ='MySql, database-migration, python-database-migration',
        install_requires = requirements,
        zip_safe = False
)
