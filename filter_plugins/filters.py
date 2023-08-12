#!/usr/bin/env python3
import collections.abc
__metaclass__ = type


class FilterModule():
    def filters(self):
        return {
            'expand_ranges': self.expand_ranges,
        }

    def expand_ranges(self, value):
        """Expand a number range at the beginning of value or each element of value.

        Generate a list of all numbers in the range (inclusive), append a :-separated suffix (if
        any) and return them as a list.

        Args:
            value: A value or sequene of values to be expanded. Each value may be of any of the
            following forms:
                1
                1:t
                1-3
                1-3:t

        Returns:
            A list of all numbers in the range(s) with the suffix appended to each number.

        """
        result = []
        if isinstance(value, str) or not isinstance(value, collections.abc.Sequence):
            value = [value]
        for v in value:
            v = str(v)
            if '-' not in v:
                result.append(v)
                continue
            suffix = ''
            if ':' in v:
                suffix = ':' + v.split(':')[1]
            numbers = v.split(':', maxsplit=1)[0]
            start = int(numbers.split('-', maxsplit=1)[0])
            end = int(numbers.split('-', maxsplit=1)[1])
            result.extend([f"{n}{suffix}" for n in range(start, end + 1)])
        return result
