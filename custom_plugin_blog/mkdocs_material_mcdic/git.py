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
    args: list[str | Path] = ["git", "log", "-1", "--format=%ad", "--date=iso-strict"]
    if date_type == "updated":
        args.append("--reverse")
    args.append(path)
    gitlog = subprocess.run(args, stdout=subprocess.PIPE)
    return datetime.fromisoformat(gitlog.stdout.decode().strip())
