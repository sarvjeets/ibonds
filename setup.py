from setuptools import find_packages, setup

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='ibonds',
    version='1.0.2',
    author='Sarvjeet Singh',
    author_email='sarvjeet@gmail.com',
    description=('Library to calculate the current value of a '
                 'Series I Savings bond (I Bond)'),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/sarvjeets/ibonds',
    license="MIT",
    platforms='any',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
    py_modules=['ibonds'],
    packages=find_packages(exclude=['tests', 'tests.*']),
    include_package_data=True,
    install_requires=[
        'PyYAML~=6.0',
        'requests~=2.28',
    ],
    test_suite='tests',
    python_requires='>=3.7',
)
