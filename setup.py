from setuptools import setup, find_packages

setup(
    name="jalap-terminal-ai",
    version="0.1.0",
    description="An intelligent terminal assistant that understands your system context and helps you run commands safely",
    author="Your Name",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "requests>=2.28.0",
        "python-dotenv>=0.20.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "black>=22.0",
            "flake8>=4.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "jalap=jalap_terminal_ai.__main__:main",
        ],
    },
    python_requires=">=3.8",
)
    
