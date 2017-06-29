#!/usr/bin/python3

import subprocess
import shlex
import sys
import curses
import curses.panel
import configparser


class Interface:
    def __init__(self, y, x, w, h, title_color, regular_text_color, title=''):
        curses.init_pair(80, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.panel_id = None
        self.win_id = None
        self.title = title
        self.title_color = title_color
        self.local_func = None
        self.value = None
        self.master = False
        self.regular_text_color = regular_text_color
        self.win_id = curses.newwin(self.h, self.w, self.y, self.x)
        self.shadow = curses.newwin(self.h, self.w, self.y + 1, self.x + 1)
        self.shadow.bkgd(' ', curses.color_pair(80))
        self.shadow.refresh()
        self.panel_id = curses.panel.new_panel(self.win_id)
        self.win_id.bkgd(' ', self.regular_text_color)
        self.win_id.clear()
        self.win_id.box()
        self.win_id.keypad(1)
        self.win_id.immedok(True)
        self.print_title()

    def call(self):
        self.local_func(*self.args)

    def print_title(self):
        self.win_id.addstr(0, 2, '%s' % self.title, self.title_color | curses.A_BOLD)

    def action(self, common_key):
        if common_key == 9:
            return False


class EditBar(Interface):
    def __init__(self, x, y, w, h, title_color, regular_text_color, title='',
                 default_value='', numeric=True):
        super(EditBar, self).__init__(x, y, w, h, title_color, regular_text_color, title)
        self.value = list(default_value)
        self.numeric = numeric
        self.cursor_position_x = len(self.value) + 1
        self.win_id.move(1, self.cursor_position_x)
        self.win_id.addstr(1, 1, default_value, regular_text_color)

    @staticmethod
    def focus():
        curses.curs_set(1)

    def update(self):
        self.cursor_position_x = len(self.value) + 1
        self.win_id.addstr(1, 1, ' ' * (self.w - 2))
        self.win_id.addstr(1, 1, ''.join(self.value), self.regular_text_color)

    def action(self, special_key):
        self.focus()
        if special_key == 263:
            if self.cursor_position_x > 1:
                self.value.pop(self.cursor_position_x - 2)
                self.cursor_position_x = self.cursor_position_x - 1 if self.cursor_position_x > 1 else 0
                self.win_id.addstr(1, self.cursor_position_x, '%s  ' % ''.join(self.value[self.cursor_position_x - 1:]))

        if special_key == 260:
            self.cursor_position_x = self.cursor_position_x - 1 if self.cursor_position_x > 1 else 1

        if special_key == 261:
            self.cursor_position_x = self.cursor_position_x + 1 if len(self.value) > self.cursor_position_x - 1 else \
                self.cursor_position_x

        if special_key == 262:
            self.cursor_position_x = 1

        if special_key == 360:
            self.cursor_position_x = len(self.value) + 1

        if (len(self.value) < self.w - 3 and ((48 <= special_key <= 57) or
                                              (65 <= special_key <= 90) or
                                              (97 <= special_key <= 122) or
                                              special_key in (45, 95, 58, 47, 44, 46, 64, 32))):
            if self.numeric and not chr(special_key).isdigit():
                return
            self.value.insert(self.cursor_position_x - 1, chr(special_key))
            self.cursor_position_x += 1
            self.win_id.addstr(1, self.cursor_position_x - 1, ''.join(self.value[self.cursor_position_x - 2:]))
        self.win_id.move(1, self.cursor_position_x)
        super(EditBar, self).action(special_key)


class List(Interface):
    def __init__(self, x, y, w, h, title_color, regular_text_color, rlist, title=''):
        super(List, self).__init__(x, y, w, h, title_color, regular_text_color, title)
        self.rlist = rlist
        self.y_max = h - 2
        self.page = 0
        self.pages = round(len(self.rlist) / self.y_max) - 1
        self.cursor_pos = 1
        self.value = 0
        self.print_rlist()
        self.win_id.move(1, 1)

    @staticmethod
    def focus():
        curses.curs_set(0)

    def _find_position(self):
        self.page = int(self.value / self.y_max)
        if self.value > len(self.rlist) - 1:
            self.value = 0
        self.cursor_pos = self.value - (self.page * self.y_max) + 1

    def update(self):
        self._find_position()
        self.print_rlist()

    def print_rlist(self, check=''):
        for pos, fu in enumerate(self.rlist[self.page * self.y_max:(self.page * self.y_max) + self.y_max]):
            self.win_id.move(1 + pos if pos < self.y_max else self.y_max, 1)
            self.win_id.clrtobot()
            self.win_id.addstr(1 + pos if pos < self.y_max else self.y_max, 1, '%s%s' % (check, fu))
        self.win_id.box()
        self.print_title()

    def action(self, special_key):
        super(List, self).action(special_key)

        def scroll_progress():
            if len(self.rlist) > self.y_max:
                self.win_id.addstr(0, self.w - 7, ' %-3s%s ' % (
                    round((100 * (self.page * self.y_max + self.cursor_pos) / len(self.rlist))), '%'))

        self.focus()
        if special_key == 262:
            self.value = 0
            self._find_position()
            self.print_rlist()

        if special_key == 360:
            self.value = len(self.rlist) - 1
            self._find_position()
            self.print_rlist()

        if special_key == 338:
            if self.pages > self.page:
                self.value = (self.page + 1) * self.y_max
                self._find_position()
                self.print_rlist()

        if special_key == 339:
            if self.page > 0:
                self.value = (self.page - 1) * self.y_max
                self._find_position()
                self.print_rlist()

        if special_key == 258:
            temp_page = self.page
            if self.value < len(self.rlist) - 1:
                self.value += 1
            self._find_position()
            if temp_page != self.page:
                self.print_rlist()
            scroll_progress()

        if special_key == 259:
            temp_page = self.page
            if self.value > 0:
                self.value -= 1
            self._find_position()
            if temp_page != self.page:
                self.print_rlist()
            scroll_progress()


class MenuList(List):
    def __init__(self, x, y, w, h, title_color, regular_text_color, rlist, title=''):
        super(MenuList, self).__init__(x, y, w, h, title_color, regular_text_color, rlist, title)
        self.print_rlist()

    def print_rlist(self, check=''):
        super(MenuList, self).print_rlist()

    def update(self):
        super(MenuList, self).update()
        self.action(0)
        self.win_id.refresh()

    def action(self, special_key):
        if len(self.rlist):
            self.win_id.chgat(self.cursor_pos, 1, self.w - 2, self.regular_text_color)
            super(MenuList, self).action(special_key)
            self.win_id.chgat(self.cursor_pos, 1, self.w - 2, curses.A_REVERSE)

    @staticmethod
    def focus():
        curses.curs_set(1)


class Button(Interface):
    def __init__(self, x, y, w, h, title_color, regular_text_color, title, value):
        super(Button, self).__init__(x, y, w, h, title_color, regular_text_color)
        self.title = title
        self.checked = 0
        self.win_id.addstr(1, int((self.w / 2) - (len(title) / 2)), '[%s]' % self.title, regular_text_color)

    def action(self, special_key):
        super(Button, self).action(special_key)
        if special_key == 10 or special_key == 32:
            self.checked = 1

    @staticmethod
    def focus():
        curses.curs_set(1)


class Dialog:
    def __init__(self, *elist):
        self.elist = elist
        self.cur_elmt = 0
        self.elist[self.cur_elmt].win_id.refresh()
        self.elist[self.cur_elmt].focus()

    def keyboard(self):
        get_key = 0
        while True:
            if get_key == 27 or \
                    (type(self.elist[self.cur_elmt]) is Button and self.elist[self.cur_elmt].checked == 1):
                break
            get_key = self.elist[self.cur_elmt].win_id.getch()
            if get_key == 10 and type(self.elist[self.cur_elmt]) is not Button:
                for button in list(filter((lambda o: type(o) is Button), self.elist)):
                    button.checked = 1
                break
            if get_key == 9:
                self.cur_elmt = self.cur_elmt + 1 if len(self.elist) - 1 > self.cur_elmt else 0
                self.elist[self.cur_elmt].win_id.refresh()
            self.elist[self.cur_elmt].action(get_key)
            curses.endwin()
            for obj in self.elist:
                obj.args = [obj]
                if obj.local_func:
                    obj.call()
            self.elist[self.cur_elmt].win_id.refresh()


def init_curses():
    screen_id = curses.initscr()
    curses.cbreak()
    curses.noecho()
    screen_id.keypad(1)
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_CYAN)
    return screen_id


def shutdown_curses(scr_id):
    curses.nocbreak()
    curses.echo()
    scr_id.keypad(0)
    curses.curs_set(1)
    curses.endwin()


def match_nodes(nodes, filter_string):
    tmp_nodes = nodes
    for word in filter_string.split(' '):
        tmp_nodes = list(filter(lambda e: word in e['words'], tmp_nodes))
    return tmp_nodes


def keyboard_shortcuts(scr_id):
    def hosts_to_display(this, *args):
        found_nodes = match_nodes(i.nodes_list, ''.join(keywords.value).rstrip(' '))
        this.rlist = [n['host'] for n in found_nodes]
        this.update()

    size_y, size_x = scr_id.getmaxyx()

    i = plugin_sd.Inventory()
    found_nodes = match_nodes(i.nodes_list, '')
    keywords = EditBar(5, int(size_x / 2) - 27, 50, 3, curses.color_pair(1),
                       curses.color_pair(1), ' Keywords ', '', False)
    filtred_hosts = MenuList(8, int(size_x / 2) - 27, 50, 35, curses.color_pair(1),
                             curses.color_pair(1), [n['host'] for n in found_nodes], ' Nodes list ')
    bOK = Button(43, int(size_x / 2) - 27, 25, 3, curses.color_pair(1), curses.color_pair(1), 'OK', 1)
    bCancel = Button(43, int((size_x / 2) - 27 + 25), 25, 3, curses.color_pair(1),
                        curses.color_pair(1), 'Cancel', 0)
    keywords.master = True
    filtred_hosts.local_func = hosts_to_display
    start_dialog = Dialog(keywords, filtred_hosts, bOK, bCancel)
    start_dialog.keyboard()
    if bOK.checked:
        return filtred_hosts.rlist
    else:
        return []

if __name__ == "__main__":
    ready_list = []
    plugin_sd = None
    config = configparser.ConfigParser()
    consumed_files = config.read('mt.conf')
    if consumed_files:
        if config['DEFAULT']['plugin'] == 'consul':
            import plugins.consul.consul as plugin_sd
        if plugin_sd:
            main_scr = init_curses()
            try:
                ready_list = keyboard_shortcuts(main_scr)
            except plugin_sd.PluginConfigNotFound as pcm:
                shutdown_curses(main_scr)
                print('ERROR: %s' % pcm.args)
            finally:
                shutdown_curses(main_scr)
            for ssh in ready_list:
                subprocess.Popen(shlex.split('%s%s' % (config['DEFAULT']['cmd'], ssh)))
        else:
            print('No such plugin.')
    else:
        print('ERROR: main config mt.conf file is missing.')
    sys.exit(0)

