# -*- coding: utf-8 -*-

import math


class Printer:

    def __init__(self):
        pass

    @staticmethod
    def print_border_top():
        print '╔════════════════════════════════════════════════════════════════════════════════════════════════════' \
              '══════════════════╗'

        Printer.print_empty()

    @staticmethod
    def print_border_bottom():
        Printer.print_empty()

        print '╚════════════════════════════════════════════════════════════════════════════════════════════════════' \
              '══════════════════╝'

        Printer.print_newline()

    @staticmethod
    def print_border_middle():
        Printer.print_empty()

        print '╠═══════════════════════════════════════════════════════════════════════════════════════════════════' \
              '═══════════════════╣'

        Printer.print_empty()

    @staticmethod
    def print_empty():
        print '║                                                                                                   ' \
              '                   ║'

    @staticmethod
    def print_content(content, align='center'):
        if align == 'center':
            print '║' + (' ' * int(math.floor(59 - (len(content) / 2)))) + content \
                + (' ' * int(math.ceil(59 - (len(content) / 2)))) + '║'
        else:
            print '║ ' + content + (' ' * (118 - len(content) - 1)) + '║'

    @staticmethod
    def print_newline():
        print ''
