from setuptools import setup, find_packages

setup(
    name="medgraph-navigator",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "networkx>=3.1",
        "python-arango>=7.5.0",
        "langchain>=0.1.0",
        "torch>=2.0.0",
        "numpy>=1.24.0",
        "pandas>=2.0.0",
        "cugraph-cu11>=23.12.0",
        "cudf-cu11>=23.12.0"
    ],
    extras_require={
        "dev": ["pytest>=7.3.1", "pytest-cov>=4.0.0"]
    },
)
