import setuptools


setuptools.setup(
    name='wallace_libs',
    version='0.0.1',
    description='wallace_libs',
    install_requires=[
        'requests==2.28.1',
        'google-cloud-core==1.6.0'
    ],
    packages=["wallace_libs"],
)
