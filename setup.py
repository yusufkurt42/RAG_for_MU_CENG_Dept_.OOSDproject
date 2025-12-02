from setuptools import setup, find_packages

setup(
    name="rag-project",
    version="1.0.0",
    packages=find_packages(where="python"),
    package_dir={"": "python"},
    python_requires=">=3.8",
    install_requires=[
        # No external dependencies required for base functionality
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
        ]
    },
    author="CSE3063 Group 8",
    description="A Retrieval-Augmented Generation (RAG) system implementation",
)
