import codecs
from setuptools import setup, find_packages

VERSION = '0.0.0'

entry_points = {
    "z3c.autoinclude.plugin": [
		'target = nti.app',
	],
    'console_scripts': [
        "nti_analytics_resource_views = nti.app.analytics_pandas.scripts.resource_views:main"
    ],
}

setup(
	name='nti.app.analytics_pandas',
	version=VERSION,
	author='Josh Zuech',
	author_email='josh.zuech@nextthought.com',
	description="NTI Analytics Pandas",
	long_description=codecs.open('README.rst', encoding='utf-8').read(),
	license='Proprietary',
	keywords='Analytics Pandas',
	classifiers=[
		'Intended Audience :: Developers',
		'Natural Language :: English',
		"Programming Language :: Python",
		"Programming Language :: Python :: 2",
		"Programming Language :: Python :: 2.7",
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3.5",
		"Programming Language :: Python :: Implementation :: CPython",
	],
	packages=find_packages('src'),
	package_dir={'': 'src'},
	namespace_packages=['nti', 'nti.app'],
	install_requires=[
		'setuptools',
        'nti.app.contenttypes.reports',
        'nti.app.pyramid_zope',
		'nti.analytics_pandas',
        'nti.contenttypes.reports',
        'nti.externalization',
        'nti.mimetype',
        'pyramid',
        'pytz',
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
        'zope.security',
        'zope.traversing',
        'zope.viewlet',
	],
	entry_points=entry_points
)

