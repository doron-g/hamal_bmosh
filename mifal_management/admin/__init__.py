from mifal_management.admin.bus import BusAdmin, HanichBusAssignmentInlineAdmin, BusStopAdmin
from mifal_management.admin.event import EventAdmin, EventRoshAdmin, EventGroupAdmin, HanichInEventAdmin
from mifal_management.admin.hanich import HanichAdmin, StatusHanichAdmin, HanichExtraQuestionAdmin
from mifal_management.admin.structure import GradeAdmin, MahozAdmin, KenAdmin

__all__ = ["HanichAdmin", "MahozAdmin", "KenAdmin", "GradeAdmin", "StatusHanichAdmin", "BusAdmin",
           "HanichBusAssignmentInlineAdmin", "BusStopAdmin", "HanichExtraQuestionAdmin", "EventAdmin", "EventRoshAdmin",
           "EventGroupAdmin", "HanichInEventAdmin"]
