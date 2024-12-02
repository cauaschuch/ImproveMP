from setuptools import setup, find_packages

setup(
    name='ImproveMP',
    version='0.1.0',
    description='Uma biblioteca feita para criar inputs automáticos para o Quantum Espresso, com dados do Materials Project',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Cauã Ferrazza Schuch, Eduardo Gadelha, Pedro Bueno e Luisa Belentani',
    author_email='caua.ferrazza@gmail.com',
    url='https://github.com/cauaschuch/ImproveMP',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'mp-api',
        'numpy'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
