"""Setup scritp"""

from setuptools import setup, find_packages

setup(
      name="anubis",
      version="0.0.1",
      packages=find_packages(),  # Automatically finds the 'anubis' package
      install_requires=[
             "numpy",
             "matplotlib",
             "pandas",
             "seaborn",
             "scikit-learn",
             "matplotlib_venn",
      ],
      author="Your Name",
      description="A Python module for data analysis tasks",
  )
