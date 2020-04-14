from distutils.core import setup

setup(
    name = 'biggu_routing',
    packages = ['biggu_routing'],
    version = 'v0.0.1',
    exclude=["test"],
    description = 'Routing for python web projects',
    author = 'Eduardo Salazar',
    author_email = 'eduardosalazar89@hotmail.es',
    url = 'https://github.com/esalazarv/biggu-routing.git',
    download_url = 'https://github.com/esalazarv/biggu-routing/archive/v0.0.1.zip',
    keywords = ['biggu_routing', 'router', 'routing'],
    license="MIT",
    classifiers = [
        "Programming Language :: Python :: 3.8",
    ],
    include_package_data=True,
    install_requires=[],
)