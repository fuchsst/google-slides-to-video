from setuptools import setup, find_packages

setup(
    name='GoogleSlidesToVideo',
    version='0.1.0',
    author='Stefan Fuchs',
    author_email='admin@stefanfuchs.dev',
    description='A project to convert Google Slides speaker notes to video presentations',
    packages=find_packages(),
    install_requires=[
        'google-auth==2.29.0',
        'google-api-python-client==2.129.0',
        'tts>=0.22.0',
        'moviepy==1.0.3'
    ],
    python_requires='>=3.10',
)
