import re
import typing
from datetime import datetime

import pytz

EARLY_EVENT_PRIORITY: typing.Final[float] = 1e9
LATE_EVENT_PRIORITY: typing.Final[float] = -1e9
VERSION: typing.Final[str] = "0.0.4"

INDEX_TITLE: typing.Final[str] = "Main Page"
TITLE_SUFFIX: typing.Final[str] = " - McDic's Blog"

SERIES_INDEX_PREFIX: typing.Final[
    str
] = """
# Series: %s

*Following is a list of all blog posts on category `%s`, sorted by numbering.*
""".strip()

METADATA_TABLE_MARKDOWN: typing.Final[
    str
] = """
### **[%s](/%s)**

| :%s: Updated | :%s: Created | :%s: Unique Visited |
| :---: | :---: | :---: |
| %s | %s | %s |
""".strip()

EXCERPT_READMORE: typing.Final[str] = "*[**(... Read more)**](/%s)*"

POST_MIGRATION_NOTICE: typing.Final[
    str
] = """
!!! migrated

    *This article is migrated from which I wrote on another website.*
""".strip()

RECENT_POSTS_PREFIX: typing.Final[
    str
] = """
# Recent Blog Posts

*Following is a list of most recent %d posts, sorted by updated date and created date.*
"""

MOST_VIEWED_POSTS_PREFIX: typing.Final[
    str
] = """
# Most Viewed Blog Posts

*Following is a list of most viewed %d posts, sorted by number of visited unique users.*
"""

ARCHIVES_PREFIX: typing.Final[
    str
] = """
# Archives: Year %d

*Following is a list of all blog posts created in year %d, sorted by created date.*
"""

META_KEY_ADDITIONAL_CONTENTS: typing.Final[str] = "additional_contents"
EXCERPT_DIVIDER: typing.Final[str] = "<!-- more -->"
INDEX_SRC_URI: typing.Final[str] = "index.md"
METADATA_NOT_AVAILABLE: typing.Final[str] = "Not available"

MIN_DATETIME: typing.Final[datetime] = datetime.min.replace(tzinfo=pytz.UTC)

RE_POST_FINDER: typing.Final[re.Pattern] = re.compile(
    r"^posts\/[a-zA-Z\-]+\/[a-zA-Z\-]*[0-9]+\.md$"
)
RE_POST_INDEX_FINDER: typing.Final[re.Pattern] = re.compile(
    r"^series\/[a-zA-Z\-]+\.md$"
)
RE_RECENT_POSTS_FINDER: typing.Final[re.Pattern] = re.compile(r"^sorted\/recent\.md$")
RE_MOST_VIEWED_FINDER: typing.Final[re.Pattern] = re.compile(
    r"^sorted\/most_viewed\.md$"
)
RE_ARCHIVES_FINDER: typing.Final[re.Pattern] = re.compile(r"^archives\/[0-9]+\.md$")
