from abc import ABC, abstractmethod


class Serializable(ABC):
    """
    Serializable is an abstract class that defines the `serialize` and `deserialize`
    methods. You do not have to inherit from this class, but it is recommended
    to do so. This allows you to create custom objects that support serialization, deltas and crossair support.
    """

    @abstractmethod
    def serialize(self):
        raise NotImplemented()

    @classmethod
    @abstractmethod
    def deserialize(cls, data):
        return cls(**data)

