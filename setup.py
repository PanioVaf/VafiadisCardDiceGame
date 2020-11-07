from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    licensed = f.read()

setup(
    name='VafiadisCardDiceGame',
    description='Card and Dice Game',
    long_description=readme,
    author='Vafeiadis Panagiotis',
    author_email='pavafeia@gmail.com',
    url='https://github.com/PanioVaf/VafiadisCardDiceGame',
    license=licensed,
    packages=find_packages(exclude='tests')
)
