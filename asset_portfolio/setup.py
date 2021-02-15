from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='portfolio',
    version='0.0.1',
    description='Best asset portfolio based on maximazing the sharpe ratio',
    long_description=readme(),
    classifiers=[
        'License :: OSI Approved :: MIT Licence',
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.6',
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
        "numpy == 1.18.5",
        "flask == 1.1.1",
        "pandas == 0.25.3",
        "plotly == 4.9.0",
        "matplotlib == 3.0.3",
        "requests == 2.20.1",
        "yfinance == 0.1.54",
        "scipy == 1.4.1",
    ],

    include_package_data=True,
    zip_safe=False,

    entry_points={
        'console_scripts': ['start-portfolio=portfolio_docker:portfolio_app']
    }
)
