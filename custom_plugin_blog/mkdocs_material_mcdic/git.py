import errno
import os
import subprocess
import typing
from datetime import datetime
from pathlib import Path


def get_date_from_git(
    path: str | Path, date_type: typing.Literal["created", "updated"]
) -> datetime:
    """
    Get a created/last-updated date of given file from the git commit history.
    If it is not an existing file nor registered on the git commit history,
    raises an error.
    """
    path = Path(path)
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path)
    args: list[str | Path] = ["git", "log", "--format=%ad", "--date=iso-strict"]
    if date_type == "created":
        args.append("--reverse")
    args.append(path)
    headtail = subprocess.Popen(
        ["head", "-1"], stdin=subprocess.PIPE, stdout=subprocess.PIPE
    )
    gitlog = subprocess.Popen(args, stdout=headtail.stdin)
    gitlog.communicate()
    out, err = headtail.communicate()
    if not out:
        raise FileNotFoundError("No git history found")
    return datetime.fromisoformat(out.decode().strip())
