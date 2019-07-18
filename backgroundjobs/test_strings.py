import unittest

from strings import *


class TestString(unittest.TestCase):

    def test_last_3_characters(self):
        inputs_and_outputs = [
            ('abcd', 'bcd'),
            ('a', 'a'),
            ('', ''),
            ('hello world', 'rld'),
        ]
        for inp, expected_output in inputs_and_outputs:
            output = last_3_characters(inp)
            self.assertEqual(output, expected_output)

    def test_first_10_characters(self):
        inputs_and_outputs = [
            ('abcd', 'abcd'),
            ('a', 'a'),
            ('', ''),
            ('hello world', 'hello worl'),
        ]
        for inp, expected_output in inputs_and_outputs:
            output = first_10_characters(inp)
            self.assertEqual(output, expected_output)

    def test_chars_4_through_10(self):
        inputs_and_outputs = [
            ('abcd', ''),
            ('a', ''),
            ('', ''),
            ('hello world', 'o world'),
            ('simple is better than complex', 'le is b'),
        ]
        for inp, expected_output in inputs_and_outputs:
            output = chars_4_through_10(inp)
            self.assertEqual(output, expected_output)

    def test_str_length(self):
        inputs_and_outputs = [
            ('abcd', 4),
            ('a', 1),
            ('', 0),
            ('hello world', 11),
            ('simple is better than complex', 29),
        ]
        for inp, expected_output in inputs_and_outputs:
            output = str_length(inp)
            self.assertEqual(output, expected_output)

    def test_words(self):
        inputs_and_outputs = [
            ('', ''),
            ('hello', 'hello'),
            ('simple is better than complex', ['simple', 'is', 'better', 'than', 'complex']),
            ('Explicit is better than implicit', ['Explicit', 'is', 'better', 'than', 'implicit']),
        ]

    def test_capitalize(self):
        inputs_and_outputs = [
            ('abcd', 'Abcd'),
            ('a', 'A'),
            ('', ''),
            ('hello world', 'Hello world'),
            ('simple is better than complex', 'Simple is better than complex'),
        ]
        for inp, expected_output in inputs_and_outputs:
            output = capitalize(inp)
            self.assertEqual(output, expected_output)

    def test_to_uppercase(self):
        inputs_and_outputs = [
            ('abcd', 'ABCD'),
            ('a', 'A'),
            ('', ''),
            ('hello world 1234', 'HELLO WORLD 1234'),
        ]
        for inp, expected_output in inputs_and_outputs:
            output = to_uppercase(inp)
            self.assertEqual(output, expected_output)


if __name__ == '__main__':
    unittest.main()
