from setuptools import setup, find_packages
with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
    name="cs1-robots",
    version='0.1.6.2',
    author='David Letscher and Michael H. Goldwasser',
    packages=find_packages('src'),
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={'': 'src'},
    url='https://github.com/hunderaweke/cs1',
    author_email="hunderaweke@gmail.com",
    keywords='cs1robots',
    install_requires=[
        'pillow',
        'tkinter',
    ],
)
