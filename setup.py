from setuptools import setup, find_packages

setup(
    name='RIG',
    version='0.1.0',
    author_email='your.email@example.com',
    description='rule_instance_generator',
    long_description_content_type='text/markdown',
    long_description=open('README.md', mode="r", encoding="utf-8").read(),
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'RIG': ['llama.cpp/*', 'llama.cpp/**/*'],  # Include all files in the llama.cpp directory
    },
    install_requires=[
        "numpy",
        "torch",
        "transformers",
        "polars",
        "llama-cpp-python",
        "sentence-transformers",
        "pandas",
        "gradio",
    ]
)

