#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

class StringFolder(object):
	"""
	source : http://www.mobify.com/blog/sqlalchemy-memory-magic/
	Class that will fold strings. See 'fold_string'.
	This object may be safely deleted or go out of scope when
	strings have been folded.
	"""

	def __init__(self):
		self.unicode_map = {}

	def fold_string(self, s):
		"""
		Given a string (or unicode) parameter s, return a string object
		that has the same value as s (and may be s). For all objects
		with a given value, the same object will be returned. For unicode
		objects that can be coerced to a string with the same value, a
		string object will be returned.
		If s is not a string or unicode object, it is returned unchanged.
		:param s: a string or unicode object.
		:return: a string or unicode object.
		"""
		# If s is not a string or unicode object, return it unchanged
		if not isinstance(s, basestring):
			return s

		# If s is already a string, then str() has no effect.
		# If s is Unicode, try and encode as a string and use intern.
		# If s is Unicode and can't be encoded as a string, this try
		# will raise a UnicodeEncodeError.
		try:
			return intern(str(s))
		except UnicodeEncodeError:
			# Fall through and handle s as Unicode
			pass

		# Look up the unicode value in the map and return
		# the object from the map. If there is no matching entry,
		# store this unicode object in the map and return it.
		t = self.unicode_map.get(s, None)
		if t is None:
			# Put s in the map
			t = self.unicode_map[s] = s
		return t
