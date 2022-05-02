def character_remover(character, string):
    """Removes any number of consecutive <character>s from the beginning of <string>"""
    while True:
        if string[0] == character:
            string = string[1:]
        else:
            break

    return string


class RegexEngine:
    def __init__(self):
        self.regex = ''
        self.string = ''
        self.flags = {
            '^': False,
            '$': False,
            '?': False,
            '.': False,
            '*': False,
            '+': False,
            '\\': False,
        }

    def main(self):
        self._set_comparison()
        print(self._reg_checker_depth1(self.regex, self.string))

    def _set_comparison(self):
        """Reads the comparison from input and sets the regex and string attributes."""
        comparison = input().split('|')
        self.regex = comparison[0]
        self.string = comparison[1]
        return

    def _reg_checker_depth1(self, regex, string):
        """Determines if the regex attribute is contained within <string>."""

        if regex.startswith('^') and regex.endswith('$') and regex[-2:] != r'/$':
            return self._reg_checker_depth1(regex[1:], string) and self._reg_checker_depth1(regex[:-1], string)

        if regex.startswith('^'):
            return self._reg_checker_depth2(regex[1:], string)

        if self._reg_checker_depth2(regex, string):
            return True

        if string == '':
            return False

        return self._reg_checker_depth1(regex, string[1:])

    def _reg_checker_depth2(self, regex, string):
        """Checks if string is equal to regex."""
        self._reset_flags()
        self._set_flags(regex)

        if regex == '':
            return True
        if regex == '$' and string == '':
            return True
        if regex == '$' and string != '':
            return False
        if string == '':
            return False

        if len(regex) >= 2 and regex[1] in ['?', '*', '+']:
            return self._handle_repetition_operators(regex, string)

        if regex[:2] in ['\\.', '\\\\']:
            return self._reg_checker_depth2(regex[1:], string)

        if regex[0] == string[0] or regex[0] == '.':
            return self._reg_checker_depth2(regex[1:], string[1:])

        if regex[0] != string[0] and regex.endswith('$'):
            return self._reg_checker_depth2(regex, string[1:])

        return False  # If the first character of regex doesn't match the first character of string

    def _reset_flags(self):
        for flag in self.flags:
            self.flags[flag] = False
        return

    def _set_flags(self, regex):
        if len(regex) >= 2 and regex[0] == '\\':
            self.flags[regex[1]] = True
        return

    def _handle_repetition_operators(self, regex, string):
        if regex[1] == '?' and not self.flags['?']:
            return self._handle_question_mark(regex, string)
        if regex[1] == '*' and not self.flags['*']:
            return self._handle_asterisk(regex, string)
        if regex[1] == '+' and not self.flags['+']:
            return self._handle_plus_sign(regex, string)

        return self._reg_checker_depth2(regex[1:], string)

    def _handle_question_mark(self, regex, string):
        if regex[0] == string[0]:
            return self._reg_checker_depth2(regex[2:], string[1:])
        else:
            return self._reg_checker_depth2(regex[2:], string)

    def _handle_asterisk(self, regex, string):
        if regex[0] == string[0]:
            return self._reg_checker_depth2(regex, string[1:])
        else:
            return self._reg_checker_depth2(regex[2:], string)

    def _handle_plus_sign(self, regex, string):
        if regex[0] == '.' and regex[2:] != '':
            next_character = regex[2]
            string_character_index = string.index(next_character)
            return self._reg_checker_depth2(regex[2:], string[string_character_index:])
        if regex[0] == '.' and regex[2:] == '':
            return True
        if regex[0] != string[0]:
            return False
        if regex[0] == string[0]:
            character = string[0]
            string = character_remover(character, string)
            return self._reg_checker_depth2(regex[2:], string)
        else:
            return self._reg_checker_depth2(regex, string[1:])


engine = RegexEngine()
engine.main()
