#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import z3c.pt.pagetemplate

from chameleon.zpt.template import PageTemplateFile

class _ViewPageTemplateFileWithLoad(z3c.pt.pagetemplate.ViewPageTemplateFile):
	"""
	Enables the load: expression type for convenience.
	"""
	# NOTE: We cannot do the rational thing and copy this
	# and modify our local value. This is because
	# certain packages, notably z3c.macro,
	# modify the superclass's value; depending on the order
	# of import, we may or may not get that change.
	# So we do the bad thing too and modify the superclass also

	@property
	def builtins(self):
		d = super(_ViewPageTemplateFileWithLoad, self).builtins
		d['__loader'] = self._loader
		# https://github.com/malthe/chameleon/issues/154
		# That's been fixed, so we should no longer
		# need to do this:
		# # We try to get iteration order fixed here:
		# result = OrderedDict()
		# for k in sorted(d.keys()):
		# 	result[k] = d[k]
		# return result
		return d

# Re-export our version
ViewPageTemplateFile = _ViewPageTemplateFileWithLoad

z3c.pt.pagetemplate.BaseTemplate.expression_types['load'] = PageTemplateFile.expression_types['load']

# monkey patch

import os
from six import string_types

from zope.browserpage import viewpagetemplatefile

from zope.pagetemplate.pagetemplatefile import package_home

# Make viewlets use our version of page template files
# Unfortunately, the zope.browserpage VPT is slightly
# incompatible in calling convention
from zope.viewlet import viewlet

from z3c.template import template

# Best to use a class not a function to avoid changing calling depth
class _VPT(ViewPageTemplateFile):

	def __init__(self, filename, _prefix=None, content_type=None):
		path = _prefix
		if not isinstance(path, string_types) and path is not None:
			# zope likes to pass the globals
			path = package_home(path)

		debug = os.getenv('DEBUG_TEMPLATES')
		auto_reload = os.getenv('RELOAD_TEMPLATES')
		ViewPageTemplateFile.__init__(self, filename, path=path, content_type=content_type,
									  auto_reload=auto_reload,
									  debug=debug)

if viewlet.ViewPageTemplateFile is viewpagetemplatefile.ViewPageTemplateFile:
	logger.debug("Monkey-patching zope.viewlet to use z3c.pt")
	viewlet.ViewPageTemplateFile = _VPT

if template.ViewPageTemplateFile is viewpagetemplatefile.ViewPageTemplateFile:
	logger.debug("Monkey-patching z3c.template to use z3c.pt")
	template.ViewPageTemplateFile = _VPT
