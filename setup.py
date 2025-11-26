from setuptools import setup, find_packages

with open("tagcall/README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="tagcall",
    version="0.1.0",
    author="汪忠仁",
    author_email="510540795@qq.com",
    description="A lightweight, model-agnostic function calling framework using <function-call> tags",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wangzhongren/tagcall",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.7",
    install_requires=[
        "beautifulsoup4>=4.9.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black",
            "flake8",
        ],
    },
    include_package_data=True,
)