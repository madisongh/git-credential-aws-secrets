from setuptools import setup, find_packages

setup(
    name='git_credential_aws_secrets',
    version='0.0.2',
    packages=find_packages(),
    license='MIT',
    author='Matt Madison',
    author_email='matt@madison.systems',
    entry_points={
        'console_scripts': [
            'git-credential-aws-secrets = git_credential_aws_secrets.credentials:main',
        ]
    },
    install_requires=['botocore',
                      'aws-secretsmanager-caching']
)