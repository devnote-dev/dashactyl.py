from setuptools import setup
from dashdactyl import __version__


long_desc = ''
with open('./README.md') as f:
    s = f.readlines()
    long_desc = '\n'.join(s)
    del s


setup(name='dashdactyl',
        author='Devonte',
        url='https://github.com/devnote-dev/dashdactyl.py',
        license='MIT',
        version=__version__,
        packages=['dashdactyl'],
        description='An interactive API wrapper for Dashdactyl in Python.',
        long_description=long_desc,
        long_desription_content_type='text/markdown',
        include_package_data=True,
        install_requires=['requests'],
        python_requires='>=3.8.0',
        classifiers=[
            'Development Status :: 2 - Pre-Alpha',
            'License :: OSI Approved :: MIT License',
            'Intended Audience :: Developers',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9'])
