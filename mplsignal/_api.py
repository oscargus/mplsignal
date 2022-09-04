def check_in_iterable(_values, *, _print_supported_values=True, **kwargs):
    """
    For each *key, value* pair in *kwargs*, check that *value* is in *_values*.

    Parameters
    ----------
    _values : iterable
        Sequence of values to check on.
    _print_supported_values : bool, default: True
        Whether to print *_values* when raising ValueError.
    **kwargs : dict
        *key, value* pairs as keyword arguments to find in *_values*.

    Raises
    ------
    ValueError
        If any *value* in *kwargs* is not found in *_values*.

    Examples
    --------
    >>> _api.check_in_iterable(["foo", "bar"], arg=arg, other_arg=other_arg)
    """
    if not kwargs:
        raise TypeError("No argument to check!")
    values = _values
    for key, val in kwargs.items():
        if val not in values:
            msg = f"{val!r} is not a valid value for {key}"
            if _print_supported_values:
                msg += f"; supported values are {', '.join(map(repr, values))}"
            raise ValueError(msg)
