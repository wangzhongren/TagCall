from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="tagcall",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Python library for tag-based function call parsing and registration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "beautifulsoup4>=4.9.0",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
    keywords="function-call, parsing, decorator, llm, ai, beautifulsoup",
)