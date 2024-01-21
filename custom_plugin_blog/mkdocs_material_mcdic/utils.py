import copy
import typing


def dict_get(
    d: typing.Mapping[str, typing.Any], *keys: str, default: typing.Any = None
) -> typing.Any:
    """
    Get `d[keys[0]][keys[1]]...` or `default` if not exsits.
    """
    current = d
    for key in keys:
        if isinstance(current, typing.Mapping) and key in current:
            current = current[key]
        else:
            return default
    return current


def dict_merge_inplace(
    target: typing.MutableMapping,
    new: typing.MutableMapping,
    override: bool = False,
    deepcopy: bool = True,
) -> typing.MutableMapping:
    """
    Merge `new` into `target` in place, and return `target`.
    """
    for key in new:
        if isinstance(target.get(key), typing.MutableMapping) and isinstance(
            new[key], typing.MutableMapping
        ):
            dict_merge_inplace(
                target[key], new[key], override=override, deepcopy=deepcopy
            )
        elif override or (key not in target):
            target[key] = copy.deepcopy(new[key]) if deepcopy else new[key]
    return target
