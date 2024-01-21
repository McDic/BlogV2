import re
import typing
from datetime import datetime

import pytz

EARLY_EVENT_PRIORITY: typing.Final[float] = 1e9
LATE_EVENT_PRIORITY: typing.Final[float] = -1e9
VERSION: typing.Final[str] = "0.0.4"

INDEX_TITLE: typing.Final[str] = "Main Page"
TITLE_SUFFIX: typing.Final[str] = " - McDic's Blog"
INDEX_RECENTLY_UPDATED_POSTS: typing.Final[
    str
] = """
*Following is a list of posts where each post is either
one of %d recently updated posts or updated in recent %d days.*
""".strip()
META_KEY_ADDITIONAL_CONTENTS: typing.Final[str] = "additional_contents"
EXCERPT_DIVIDER: typing.Final[str] = "<!-- more -->"
INDEX_SRC_URI: typing.Final[str] = "index.md"
METADATA_NOT_AVAILABLE: typing.Final[str] = "Not available"

MIN_DATETIME: typing.Final[datetime] = datetime.min.replace(tzinfo=pytz.UTC)

RE_POST_FINDER: typing.Final[re.Pattern] = re.compile(
    r"^posts\/[a-zA-Z\-]+\/[a-zA-Z\-]*[0-9]+\.md$"
)
RE_POSTINDEX_FINDER: typing.Final[re.Pattern] = re.compile(r"^series\/[a-zA-Z\-]+\.md$")
