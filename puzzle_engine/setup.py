from setuptools import setup, find_packages

requires = [
    'gurobipy',
    'marshmallow==2.13.4',
]

setup(
    name='puzzle_engine',
    version='0.0.1-dev',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    entry_points="""\
    [console_scripts]
    puzzle_engine = puzzle_engine.cli:cli
    """
)
