#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from ..utils import orm_dataframe

from .assessments import QueryAssignmentViews
from .assessments import QueryAssignmentsTaken
from .assessments import QueryAssignmentDetails
from .assessments import QuerySelfAssessmentViews
from .assessments import QuerySelfAssessmentsTaken
from .assessments import QuerySelfAssessmentDetails

from .bookmarks import QueryBookmarksCreated

from .chats import QueryChatsInitiated
from .chats import QueryChatsJoined

from .courses import QueryCourses

from .enrollments import QueryCourseDrops
from .enrollments import QueryEnrollmentTypes
from .enrollments import QueryCourseEnrollments
from .enrollments import QueryCourseCatalogViews

from .forums import QueryForumsCreated
from .forums import QueryForumCommentLikes
from .forums import QueryForumsCommentsCreated
from .forums import QueryForumCommentFavorites

from .highlights import QueryHighlightsCreated

from .notes import QueryNoteLikes
from .notes import QueryNotesViewed
from .notes import QueryNotesCreated
from .notes import QueryNoteFavorites

from .profile_views import QueryEntityProfileViews
from .profile_views import QueryEntityProfileActivityViews
from .profile_views import QueryEntityProfileMembershipViews

from .social import QueryContactsAdded
from .social import QueryContactsRemoved
from .social import QueryFriendsListsCreated
from .social import QueryFriendsListsMemberAdded
from .social import QueryFriendsListsMemberRemoved
from .social import QueryDynamicFriendsListsCreated
from .social import QueryDynamicFriendsListsMemberAdded
from .social import QueryDynamicFriendsListsMemberRemoved

from .topics import QueryTopicLikes
from .topics import QueryTopicsViewed
from .topics import QueryTopicsCreated
from .topics import QueryTopicFavorites

from .videos import QueryVideoEvents

from .resources import QueryResources

from .users import QueryUsers

from .resource_views import QueryCourseResourceViews
