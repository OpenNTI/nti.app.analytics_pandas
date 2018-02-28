import codecs
from setuptools import setup
from setuptools import find_packages

entry_points = {
    "z3c.autoinclude.plugin": [
        'target = nti.app',
    ],
    'console_scripts': [
        "nti_analytics_resource_views = nti.app.analytics_pandas.scripts.resource_views:main"
    ],
}

TESTS_REQUIRE = [
    'nti.app.testing',
    'nti.testing',
    'zope.dottedname',
    'zope.testrunner',
]


def _read(fname):
    with codecs.open(fname, encoding='utf-8') as f:
        return f.read()


setup(
    name='nti.app.analytics_pandas',
    version=_read('version.txt').strip(),
    author='Josh Zuech',
    author_email='josh.zuech@nextthought.com',
    description="NTI Analytics Pandas",
    long_description=(_read('README.rst') + '\n\n' + _read("CHANGES.rst")),
    license='Apache',
    keywords='analytics pandas reports',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    url="https://github.com/NextThought/nti.app.analytics_pandas",
    zip_safe=True,
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    namespace_packages=['nti', 'nti.app'],
    tests_require=TESTS_REQUIRE,
    install_requires=[
        'setuptools',
        'nti.app.contenttypes.reports',
        'nti.app.pyramid_zope',
        'nti.analytics_pandas',
        'nti.contenttypes.reports',
        'nti.externalization',
        'nti.mimetype',
        'nti.schema',
        'pyramid',
        'pytz',
        'reportlab',
        'z3c.macro',
        'z3c.pagelet',
        'z3c.rml',
        'z3c.template',
        'zope.browserpage',
        'zope.component',
        'zope.container',
        'zope.i18nmessageid',
        'zope.interface',
        'zope.location',
        'zope.schema',
        'zope.security',
        'zope.traversing',
        'zope.viewlet',
    ],
    extras_require={
        'test': TESTS_REQUIRE,
        'docs': [
            'Sphinx',
            'repoze.sphinx.autointerface',
            'sphinx_rtd_theme',
        ],
    },
    entry_points=entry_points,
)
