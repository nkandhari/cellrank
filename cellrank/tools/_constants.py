# -*- coding: utf-8 -*-
"""Module containing CellRank contants."""

from enum import Enum, EnumMeta
from typing import Any, Union, Callable
from functools import wraps


class PrettyEnum(Enum):
    """Enum wit a pretty __str__ and __repr__."""

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.value)

    @property
    def v(self) -> Any:
        """Return the value."""
        return self.value

    @property
    def s(self) -> str:
        """Return the value as string."""
        return str(self)

    @property
    def fmt(self) -> Callable:
        """Return the formatting function given by the string value."""
        return self.s.format


class Lin(PrettyEnum):
    """Lineage aggregation type."""

    REST = "rest"
    OTHERS = "others"


class Direction(PrettyEnum):
    """Direction of the process."""

    FORWARD = "fwd"
    BACKWARD = "bwd"


class DirectionPlot(PrettyEnum):
    """Pretty direction names for plotting."""

    FORWARD = "forward"
    BACKWARD = "backward"


class FinalStatesKey(PrettyEnum):
    """State key in `adata.obs`."""

    FORWARD = "final_states"
    BACKWARD = "root_states"


class FinalStatesPlot(PrettyEnum):
    """Pretty state names for plotting."""

    FORWARD = "final states"
    BACKWARD = "root states"


# FinalStatesKey and AbsProbKey must have the same suffix `_..._states` because of model.prepare
class AbsProbKey(PrettyEnum):
    """Lineage key in `adata.obsm`."""

    FORWARD = "to_final_states"
    BACKWARD = "from_root_states"


class MetaKey(PrettyEnum):
    """Metastable state key in `adata.obs`."""

    FORWARD = "metastable_states_fwd"
    BACKWARD = "metastable_states_bwd"


class DirPrefix(PrettyEnum):
    """Direction prefix."""

    FORWARD = "to"
    BACKWARD = "from"


def _transition(d: Union[str, Direction]) -> str:
    return f"T_{d}"


def _lin_names(k: Union[str, AbsProbKey]) -> str:
    return f"{k}_names"


def _colors(k: Union[str, AbsProbKey, FinalStatesKey]) -> str:
    return f"{k}_colors"


def _probs(k: Union[str, FinalStatesKey]) -> str:
    return f"{k}_probs"


def _dp(k: Union[str, AbsProbKey]) -> str:
    return f"{k}_dp"


class PrettyEnumMeta(EnumMeta):
    """Metaclass for Enums which shows values when invalid is specified."""

    def __new__(cls, clsname, superclasses, attributedict):  # noqa
        res = super().__new__(cls, clsname, superclasses, attributedict)
        res.__new__ = _pretty_raise_enum(
            res.__new__, [m.value for m in res.__members__.values()]
        )
        return res


def _pretty_raise_enum(fun, values):
    @wraps(fun)
    def wrapper(*args, **kwargs):
        try:
            return fun(*args, **kwargs)
        except ValueError as e:
            value = args[1]
            e.args = (f"Invalid option `{value}`. Valid options are: `{values}`.",)
            raise e

    return wrapper
