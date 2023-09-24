from __future__ import annotations

from enum import Enum, auto
from dataclasses import dataclass

from itertools import chain


class _ProxyComponent:

    def __init__(self, identifier: int | list[int], coef: int | list[int]):

        self._components = []
        self._coefficients = []

        def expand(collection, obj):
            if isinstance(obj, int):
                collection.append(obj)
            elif isinstance(obj, list):
                collection.extend(obj)
            else:
                raise RuntimeError("wtf")

        expand(self._components, identifier)
        expand(self._coefficients, coef)

    def __add__(self, other: _ProxyComponent) -> _ProxyComponent:
        comps = list(chain.from_iterable([self._components, other._components]))
        coefs = list(chain.from_iterable([self._coefficients, other._coefficients]))

        return _ProxyComponent(comps, coefs)

    def __mul__(self, other: int):

        coefs = [c*other for c in self._coefficients]
        return _ProxyComponent(self._components, coefs)

    def __rmul__(self, other: int):

        return self*other


class Component(_ProxyComponent):

    def __init__(self, n: int):
        super().__init__(n, 1)
        self._id: int = n

    @staticmethod
    def create(count: int) -> list[_ProxyComponent]:
        return [Component(i) for i in range(count)]

    def __eq__(self, other: Component) -> bool:
        return self._id == other._id


class ReactionType(Enum):

    Irreversible = auto()
    Reversible = auto()


@dataclass
class Reaction:

    lhs: _ProxyComponent
    rhs: _ProxyComponent
    type: ReactionType = ReactionType.Irreversible


class ReactionSystem:

    def __init__(self, reactions: list[Reaction]):

        self._reactions = reactions

    def get_coefficients(self):
        pass


A, B, C, D, E = Component.create(5)

r1 = Reaction(A+2*B, C+D)
r2 = Reaction(A+D, 2*E)

assert len(r1.lhs._components) == 2
assert r1.lhs._components[0] == A._id and r1.lhs._components[1] == B._id
