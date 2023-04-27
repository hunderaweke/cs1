from setuptools import setup, find_packages

setup(
    name="cs1-robots",
    version='0.1.6.2',
    author='David Letscher and Michael H. Goldwasser',
    author_email='',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='',
    keywords='cs1robots',
    install_requires=[
        'pillow',
        'tkinter',
    ],
)
