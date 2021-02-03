import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simgen", # Replace with your own username
    version="0.0.1",
    author="Équipe CREEi",
    author_email="pierre-carl.michaud@hec.ca",
    description="Modele de microsimulation SimGen",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://creei-models.github.io/simgen",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
   'pandas',
   'numpy',
   'numba',
   'multiprocessing',
   'copy',
   'random',
   'os',
   'pickle',
   'inspect',
   'itertools'
    ],
    python_requires='>=3.6',
)