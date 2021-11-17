import setuptools

with open('requirements.txt', 'rb') as handle:
    REQUIREMENTS = [
        r.decode('utf8') for r in handle.readlines()
    ]

setuptools.setup(
    name='BI-Demo-Dataflow',
    version='1.0',
    install_requires=REQUIREMENTS,
    packages=setuptools.find_packages(),
)