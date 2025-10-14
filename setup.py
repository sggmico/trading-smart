from setuptools import setup, find_packages

setup(
    name="smart-trading",
    version="0.1.0",
    description="AI-driven cryptocurrency trading bot",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "python-binance>=1.0.19",
        "ccxt>=4.2.25",
        "pandas>=2.2.0",
        "numpy>=1.26.3",
        "scikit-learn>=1.4.0",
        "python-dotenv>=1.0.1",
        "pyyaml>=6.0.1",
        "loguru>=0.7.2",
    ],
    extras_require={
        "dev": [
            "pytest>=8.0.0",
            "pytest-cov>=4.1.0",
            "black>=24.1.1",
            "flake8>=7.0.0",
            "mypy>=1.8.0",
            "jupyter>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "smart-trading=src.main:main",
        ],
    },
)
