from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='webscraper_hist',
    version='0.0.1',
    description='Webscraper for historical info of the cryptocurrencies',
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
        "pandas==0.25.3",
        "DateTime==4.3",
        "flask==1.1.1",
        "bs4==0.0.1",
        "requests==2.20.1",
        "apscheduler ==3.6.3"
    ],

    include_package_data=True,
    zip_safe=False,

    entry_points={
        'console_scripts': ['start-webscraper_hist=webscraper_hist_docker:webscraper_hist_app']
    }
)
