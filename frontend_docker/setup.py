from setuptools import setup, find_packages

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='frontend_crypto',
    version='0.0.1',
    description='Cripto currency portfolio',
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
    author='Luis Gerardo Guzmán',
    author_email='luguzman.rojas@outlook.com',
    license='MIT',

    python_requires='>=3.6',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        "flask==1.1.1",
        "dnspython==1.16.0",
        "pymongo==3.9.0",
        "requests==2.20.1",
        "dash==1.4.0",
        "dash_html_components==1.0.1",
        "DateTime==4.3",
        "pandas == 0.25.3"
    ],

    include_package_data=True,
    zip_safe=False,

    entry_points={
        'console_scripts': ['start-front=frontend_crypto:start_app']
    }
)
