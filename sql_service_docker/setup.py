from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='sql_historical',
    version='0.0.1',
    description='Historical database for crypto-currencies',
    long_description=readme(),
    classifiers=[
        'License :: OSI Approved :: MIT Licence',
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
    ],

    keywords='',
    url='',
    author='Luis Gerardo Guzmán Rojas',
    author_email='luguzman.rojas@outlook.com',
    license='MIT',

    python_requires='>=3.7',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        "flask==1.1.1",
        "pandas == 0.25.3",
        "xlrd >= 1.0.0",
        "sqlalchemy==1.3.20",
        "flask-mysqldb",
        "requests",
        "mysqlclient"
    ],

    include_package_data=True,
    zip_safe=False,

    entry_points={
        'console_scripts': ['start-sql_service=sql_service_port:sql_service_app']
    }
)
