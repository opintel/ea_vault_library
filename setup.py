from setuptools import setup

setup(name='opi_vault_library',
    version='0.1',
    description='A Python package for file protection process',
    url='https://github.com/opintel/ea_vault_library',
    author='OPI',
    author_email='j.castaneda@opianalytics.com',
    license='MIT',
    packages=['ea_vault_library'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requirest=['PyPDF2','pycryptodome','python-dotenv'],
    zip_safe=False)
