from setuptools import setup, find_packages

# This setup.py is kept for backwards compatibility.
# Prefer using pyproject.toml for configuration.

setup(
    name="owockibot",
    use_scm_version=True,
    packages=find_packages(exclude=["tests*"]),
    python_requires=">=3.8",
)
