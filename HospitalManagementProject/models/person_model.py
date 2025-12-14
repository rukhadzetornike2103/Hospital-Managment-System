from abc import ABC, abstractmethod


class Person(ABC):

    def __init__(self, full_name, age, gender):
        self._full_name = full_name
        self._age = age
        self._gender = gender

    @abstractmethod
    def display_info(self):
        """Method to display the person's information."""
        pass

    @abstractmethod
    def generate_unique_identifier(self):
        """Generate a unique identifier for the person."""
        pass

    @property
    def full_name(self):
        return self._full_name

    @full_name.setter
    def full_name(self, new_n):
        if isinstance(new_n, str):
            self._full_name = new_n
        else:
            raise TypeError('Name must be a string.')

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, new_a):
        if isinstance(new_a, int) and new_a >= 0:
            self._age = new_a
        else:
            raise ValueError('Age must be a non-negative integer.')

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, new_g):
        if isinstance(new_g, str):
            self._gender = new_g
        else:
            raise TypeError('Gender must be a string.')

