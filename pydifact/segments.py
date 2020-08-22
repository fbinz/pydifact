# Pydifact - a python edifact library
#
# Copyright (c) 2019 Christian González
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
from typing import Union, List

from pydifact.control import Characters
from pydifact.syntax import EDISyntaxError


class Segment:
    """Represents a low-level segment of an EDI interchange."""

    def __init__(self, tag: str, *elements: Union[str, List[str]]):
        """Create a new Segment instance.

        :param str tag: The code/tag of the segment. Must not be empty.
        :param list elements: The data elements for this segment, as (possibly empty) list.

        The Segment can assure that the given parameters are correct.
        """
        assert tag
        self.tag = tag

        # The data elements for this segment.
        # this is converted to a list (due to the fact that python creates a tuple
        # when passing a variable arguments list to a method)
        self.elements = list(elements)

    def __str__(self) -> str:
        """Returns the Segment in Python list printout"""
        return "'{tag}' EDI segment: {elements}".format(
            tag=self.tag, elements=str(self.elements)
        )

    def __repr__(self) -> str:
        return f"{self.tag} segment: {str(self.elements)}"

    def __eq__(self, other) -> bool:
        # FIXME the other way round too? isinstance(other, type(self))?
        return isinstance(self, type(other)) and list(self.elements) == list(
            other.elements
        )


class SegmentFactory:
    """Factory for producing segments."""

    characters = None

    @staticmethod
    def create_segment(name: str, *elements: Union[str, List[str]]) -> Segment:
        """Create a new instance of the relevant class type.

        :param name: The name of the segment
        :param elements: The data elements for this segment
        """
        if not SegmentFactory.characters:
            SegmentFactory.characters = Characters()

        # Basic segment type validation is done here.
        # The proper validation must be done in the corresponding Segment

        if not name:
            raise EDISyntaxError("The tag of a segment must not be empty.")

        if type(name) != str:
            raise EDISyntaxError(
                f"The tag name of a segment must be a str, but is a {type(name)}: {name}"
            )

        if not name.isalnum():
            raise EDISyntaxError(
                f"Tag '{name}': A tag name must only contain alphanumeric characters."
            )

        # FIXME: characters is not used!
        return Segment(name, *elements)
