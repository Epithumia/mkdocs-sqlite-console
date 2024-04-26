from setuptools import setup, find_packages

setup(
    name='mkdocs-sqlite-console',
    version='1.0.5b',
    description='A MkDocs plugin that adds a sqlite IDE.',
    long_description="""A MkDocs plugin that adds a sqlite IDE.
    
    The IDE can load a database file given as a parameter, pre-run SQL before user input, and run the user's SQL code.
    
    This plugin uses SQL.js as a worker, which should prevent issues with large databases and query results. 
    """,
    keywords=['mkdocs', 'sqlite'],
    url='',
    author='Rafaël Lopez',
    author_email='rafael.lopez@universite-paris-saclay.fr',
    license='MIT',
    python_requires='>=3.0',
    install_requires=[
        'mkdocs>=1.0.4'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
    packages=find_packages(),
    entry_points={
        'mkdocs.plugins': [
            'sqlite-console = mkdocs_sqlite_console:SQLiteConsole'
        ]
    },
    package_data={
        "": ["css/*", "js/*"],
    },
    include_package_data=True
)
