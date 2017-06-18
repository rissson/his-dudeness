# -*- coding: utf-8 -*-
import pygame

from graphalama import icons
from graphalama.borg import Borg
import graphalama.fonts as f
from graphalama.rectangle import Rectangle, Area
from graphalama.color import Color
from graphalama.CONSTANTS import *
from graphalama.functions import *

pygame.init()
borg_baby = Borg()


# string functions
def letter_suppress(string, position, size=1):
    return string[:position] + string[position + size:]


def letter_add(string, new_letters, position):
    return string[:position + 1] + new_letters + string[position + 1:]


def split_to_words(text):
    t = []
    w = ''
    for carac in text:
        w += carac
        if carac == ' ':
            t.append(w)
            w = ''
    if w != '':
        t.append(w)
    return t


# classes
class Carac:
    def __init__(self, carac, font=None, color=BLACK, bg_color=TRANSPARENT, underline=False):

        if type(carac) == Carac:  # if we want to re-carac an object
            self.color = carac.color
            self.bg_color = carac.bg_color
            self.carac = carac.carac
            self._font = carac._font
            self.underline = carac.underline
            self.surface = carac.surface
        else:

            self.color = Color(color)
            self.bg_color = Color(bg_color)
            self.carac = carac
            self._font = font if font is not None else f.Font()
            if self._font.size <= 1:
                raise Exception
            self.underline = underline

        self.previous_state = Carac.__state__(self)
        self.previous_state['first'] = None

    def __repr__(self):

        ret = str(self.color) + ' ' + str(self.bg_color) + ' F:' + str(self._font) + ' - ' + self.carac
        return str(ret)

    def __state__(self):
        dic = dict()
        dic['color'] = self.color.RGBA
        dic['bg_color'] = self.bg_color.RGBA
        dic['font'] = self._font
        dic['carac'] = self.carac
        return dic

    # the 4 characteristics of the font
    @property
    def font_class(self):
        return self._font[0]

    @font_class.setter
    def font_class(self, value):
        self._font[0] = value

    @property
    def font_size(self):
        return self._font[1]

    @font_size.setter
    def font_size(self, value):
        self._font[1] = value
        self.previous_state = dict()

    @property
    def bold(self):
        return self._font[2]

    @bold.setter
    def bold(self, value):
        self._font[2] = value

    @property
    def italic(self):
        return self._font[3]

    @italic.setter
    def italic(self, value):
        self._font[3] = value

    # font object itself
    @property
    def font(self):
        """returns the good pygame font object"""

        # The Font Class           # font size   # bools
        return self.font_class.get_font(self.font_size, self.bold, self.italic)

    # useful measurements
    @property
    def size(self):
        """returns the size needed to render the carac"""
        return self.font.size(self.carac)

    @property
    def width(self):
        """Returns the width of the carac"""
        return self.size[0]

    @property
    def height(self):
        """returns the height of the carac"""
        return self.font.get_height()

    @property
    def ascent(self):
        """ Returns the ascent of the carac. The ascent is the number of pixel up to the base line
        We ave height = ascent + descent + 1 """
        return self.font.get_ascent()

    @property
    def descent(self):
        """ Returns the descent of the font/carac. The descent is the number of pixels above th base line.
        We have height = ascent + descent + 1 """
        return self.font.get_descent()

    @only_if_object_changes
    def render(self):
        if self.bg_color.RGBA[3] == 0:  # cause alpha counts for nothing, but it will be transparent if there is no bg
            try:
                self.surface = self.font.render(self.carac, True, self.color.RGBA)  # we re-draw the text surf
            except TypeError:
                print(self.color.RGBA)
        else:
            self.surface = self.font.render(self.carac, True, self.color.RGBA,
                                            self.bg_color.RGBA)  # we re-draw the text surf

        self.surface.convert_alpha()

    def update(self):
        if self.color.is_living:
            self.render()


class FlyingText:
    def __init__(self, text, font=None, color=BLACK):
        font = f.Font(size=72) if font is None else font
        self.caracs = []

        if type(text) == str:

            self.font = font  # logical
            self._default_color = Color(color)

            self.add_ddrtf(text, self.font, self.text_color)

        elif isinstance(text, FlyingText):

            self.font = text.font
            self._default_color = text.text_color

            self.caracs = text.caracs

        elif type(text) == list:
            self.font = font
            self.caracs = text  # this is just a list of Carac with lot of functions & methods
            self._default_color = Color(color)

        self.previous_color = Color(self._default_color)
        self.previous_state = 'first'

    def __repr__(self):
        ret = [repr(carac) for carac in self]  # TODO: make sthg shorter
        return str(ret)

    def __state__(self):
        dic = dict()
        for i, carac in enumerate(self.caracs):
            dic[i] = carac.__state__()
        dic['width'] = self.width

        return dic

    # Some list-like functions
    def __delitem__(self, key):
        self.caracs.__delitem__(key)

    def __getitem__(self, item):
        try:
            if type(item) == slice:
                start = 0 if item.start is None else item.start
                stop = len(self) if item.stop is None else item.stop
                step = 1 if item.step is None else item.step

                caracs = [self.caracs[i] for i in range(start, stop, step)]
                return FlyingText(caracs)

            elif type(item) == int:
                return self.caracs.__getitem__(item)

        except IndexError:
            print(('Item: ', item, 'self:', self))
            raise

    def __setitem__(self, key, value):
        if type(key) == int:
            if type(value) == str:
                # here I select the Carac who'll give the font/size... to the nex carac
                if key == 0:
                    model = self[1]  # maybe a little bit ugly :P # TODO : Can I to better ?
                else:
                    model = self[key - 1]
                for carac in value:
                    self.caracs[key] = Carac(model)  # we double the model Carac
                    self[key].carac = carac  # Then we just change the char itself

    def __delslice__(self, i, j):
        if i == 0 and j == len(self):
            del self
        else:
            for pos in range(i, j).__reversed__():
                self.__delitem__(pos)

    def __add__(self, letters):
        new_word = FlyingText(self)
        new_word.insert(len(self), letters)

        return new_word

    def __iadd__(self, letters):
        return self + letters

    # TODO: __radd__

    def __len__(self):
        return len(self.caracs)

    def __iter__(self):
        for carac in self.caracs:
            yield carac

    def insert(self, position, letters):
        """
        This will insert 'letters' at 'position'
        The font and size will be the the same as the carac before.
        :type position: int
        :type carac: str
        :type color: Color
        """
        if type(letters) == str:
            if position == 0:
                self.insert_ddrtf(position, letters, self.font, self._default_color)
            else:
                self.insert_ddrtf(position, letters,
                                  self[position - 1]._font, self[position - 1].color, self[position - 1].bg_color)

        elif type(letters) == Text:
            for p, carac in enumerate(letters):
                self.caracs.insert(position + p, carac)

        elif type(letters) == Carac:
            self.caracs.insert(position, letters)

    def append(self, letters):
        self.insert(len(self), letters)

    def insert_ddrtf(self, position, text, font=None, color=None, bg_color=None):
        pos = 0
        number_of_caracs_added = 0
        # done
        bold = False if font is None else font.bold
        italic = False if font is None else font.italic
        underline = False

        font = self.font if font is None else font

        color = Color(color) if color is not None else self._default_color
        bg_color = TRANSPARENT

        while pos < len(text):
            if text[pos] == "¤":
                pos += 1
                if text[pos] == '¤':  # it's \ who needs to be rendered
                    self.caracs.insert(position + number_of_caracs_added,
                                Carac('¤', f.Font(font[0], font[1], bold, italic), color, bg_color, underline))
                    pos += 1
                else:  # it's not a visible \ : it's a tag start
                    tag = ''
                    while text[pos] != ' ':
                        tag += text[pos]
                        pos += 1
                    pos += 1  # the last space
                    if tag == 'bold':  # bold, underline, italic
                        bold = not bold
                    elif tag == 'italic':
                        italic = not italic
                    elif tag == underline:
                        underline = not underline
                        # tags[tag] = False
                        # elif tag in ['bold0', 'italic0', 'underline0']:  # not bold, not underline, not italic
                        #     tags[tag[:-1]] = False  # the last char is '0'. In the dict, tags aren'T with the '0'
            else:
                # we add the char at the end of the text already added
                self.caracs.insert(position + number_of_caracs_added,
                            Carac(text[pos], f.Font(font[0], font[1], bold, italic), color, bg_color, underline))
                pos += 1  # run furet !

            number_of_caracs_added += 1

    def add_ddrtf(self, text, font=None, color=None, bg_color=None):
        self.insert_ddrtf(len(self), text, font, color, bg_color)

    # TODO : def to_ddrtf(self, text)

    # The text itself
    @property
    def text(self):
        return ''.join([carac.carac for carac in self])

    @text.setter
    def text(self, text):
        """
        :type text: str
        """
        if type(text) == str:
            self.caracs = []
            self.add_ddrtf(text)

        elif isinstance(text, FlyingText) or type(text) == list:
            raise NotImplementedError

    # Bold, italic and underline
    @property
    def bold(self):
        """ Returns the Proportion of bold Carac in self"""
        return sum([carac.bold for carac in self]) / len(self)

    @bold.setter
    def bold(self, args):
        """set the bold (or not) for the word."""

        for carac in self:
            carac.bold = args

    @property
    def italic(self):
        """ Returns the Proportion of italic Carac in self"""
        return sum([carac.italic for carac in self]) / len(self)

    @italic.setter
    def italic(self, args):
        for carac in self:
            carac.italic = args

    @property
    def underline(self):
        """ Returns the Proportion of underline Carac in self"""
        return sum([carac.underline for carac in self]) / len(self)

    @underline.setter
    def underline(self, args):
        for carac in self:
            carac.underline = args

    @property
    def font(self):
        return self._default_font

    @font.setter
    def font(self, font):
        """ Sets the font for the whole text. Do Text[start:end] to set it for a part of the text """
        for carac in self:
            carac.font_class = font.clas
            carac.font_size = font.size
            carac.bold = font.bold
            carac.italic = font.italic

        self._default_font = font

    @property
    def font_size(self):
        raise NotImplementedError

    @font_size.setter
    def font_size(self, size):
        """size can be between 0 and 1 (proportional) or any other positive integer"""

        for carac in self:
            carac.font_size = size  # the args is the boolean of bold
            print('.', end='')

    def increment_font_size(self, value):
        """increment the font of each carac by the value given. value is an INTEGER positive or negative"""
        for carac in self:
            carac.font_size = carac.font_size + value

    @property
    def height(self):
        """
        return the height needed to render the text. It's the sum of the lines' height
        :return: int
        """

        if len(self) > 0:
            return max([carac.height for carac in self])
        else:
            return 0

    @property
    def ascent(self):
        if len(self) > 0:
            return max([carac.ascent for carac in self])
        else:
            return 0

    @property
    def descent(self):
        if len(self) > 0:
            return max([carac.descent for carac in self])
        else:
            return 0

    @property
    def width(self):
        """ Returns the total width need to render the caracs if they were in one single line."""
        if len(self) > 0:
            return sum([carac.width for carac in self])
        else:
            return 0

    @property
    def color_is_living(self):
        for carac in self:
            if carac.color.is_living:
                return True
        return False

    # the Back/foreground color

    @property
    def text_color(self):
        return self._default_color

    @text_color.setter
    def text_color(self, value):
        for carac in self:
            carac.color = Color(value)

    @property
    def bg_color(self):
        return None

    @bg_color.setter
    def bg_color(self, value):
        for carac in self:
            carac.bg_color = Color(value)

    def update(self):
        if self.previous_color.RGBA != self.text_color.RGBA:  # color has changed (but only the mode)
            self.text_color = self.text_color
            self.previous_color = Color(self.text_color)

        for carac in self:
            carac.update()


class Text(FlyingText, Rectangle):
    def __init__(self, text, rect_args=None, font=None, color=BLACK, anchor=None, options=NO):
        """ :param text:        is a DDRTF string
:param rect_args:   will be passed in args to the rect around the text. It must be a tuple/list
:param font:        a graphalama.fonts.Font object
:param color:
:param anchor:      look like this : ('bl', 0.1, 7). The first two caracs are the position of the text (see below)
    and the second and third item are the offset, it can be, like the font size between 0 and 1 (so
    proportionally) or any integer (nbr of pxl).
        possible anchors:   tl tc tr
                            cl cc cr
                            bl bc br
:param options:     can be ONELINE if u want a text who must always be contained in one line

/!\\ For the addition, the order matters !!!! This is only the rect of the first Text who'll be kept !
"""

        self.end_of_lines = []
        self.default_font = f.Font()

        if type(text) == str:

            self.options = options

            if font is None:
                font = f.Font()

            self.anchor = ('tl', 0, 0) if anchor is None else anchor

            Rectangle.__init__(self, *rect_args)
            fake_font = f.Font(*font)
            fake_font.size = to_pixels(font[1], self.real_h)  # we scale if needed (if 0 < font <= 1) the font size
            FlyingText.__init__(self, text, fake_font, color)
            self.font = font

            self.split_to_lines()

        elif type(text) == Text:

            Rectangle.__init__(self, *text.rect_as_tuple)
            FlyingText.__init__(self, [Carac(carac) for carac in text],
                                f.Font(*text._default_font), Color(self._default_color))

            self.anchor = text._anchor
            self.options = text.options
            self.split_to_lines()

        else:
            raise NotImplementedError

        self.previous_state = Text.__state__(self)
        self.previous_state['first'] = None

    def __repr__(self):
        return 'Text' + FlyingText.__repr__(self) + '\n -->:' + Rectangle.__repr__(self) + \
               '\n Anchor' + str(self.relative_anchor)

    def __state__(self):
        state = dict()
        state.update(FlyingText.__state__(self))
        state.update(Rectangle.__state__(self))
        state['anchor'] = self.real_anchor
        state['options'] = self.options
        return state

    # Some list-like functions
    def __add__(self, letters):
        new_word = Text(self)
        new_word.insert(len(self), letters)

        return new_word

    @property
    def font_size(self):
        return to_pixels(self.font.size, self.real_h)

    @font_size.setter
    def font_size(self, size):
        """size can be between 0 and 1 (proportional) or any other positive integer"""
        for carac in self:
            carac.font_size = to_pixels(size, self.height)
        self.default_font.size = size

    @property
    def font(self):
        fo = self.default_font
        return f.Font(fo.clas, to_pixels(fo.size, self.real_h), fo.bold, fo.italic)

    @font.setter
    def font(self, font):
        for carac in self:
            carac.font_class = font.clas
            carac.font_size = to_pixels(font.size, self.real_h)
            carac.bold = font.bold
            carac.italic = font.italic
        self.default_font = font
    # anchor

    @property
    def relative_anchor(self):
        return [self.anchor[0], to_prop(self.anchor[1], self.real_w), to_prop(self.anchor[2], self.real_h)]

    @property
    def real_anchor(self):
        return self.anchor[0], to_pixels(self.anchor[1], self.real_w), to_pixels(self.anchor[2], self.real_h)

    @property
    def rendered_height(self):
        """ Returns the total height of the rendered text, without the extra bg size
        !! This functions calls split_to_lines.
        !! This does not include the margin : add 2 * self.real_anchor[2] to get the very real height"""
        h = 0
        beg = 0
        self.split_to_lines()
        for end in self.end_of_lines:
            h += self[beg: end].height
            beg = end
        return h

    def split_to_lines(self):

        if ONELINE in self.options:
            self.end_of_lines = [len(self)]
        else:
            words = split_to_words(self.text)
            treated_text = [('', 0, 0)]
            for word in words:
                start_pos = treated_text[-1][1] + len(treated_text[-1][0])
                w = self[start_pos: start_pos + len(word)].width
                treated_text.append((word, start_pos, w))
            del treated_text[0]

            max_w = self.real_w - 2 * (self.real_anchor[1] + self.real_circle_radius)
            space_left = max_w
            endl = []
            pos = 0
            for word in treated_text:
                if word[2] > max_w:
                    endl.append(pos)
                    space_left = max_w
                    for i in range(word[1], word[1] + len(word[0])):
                        if self[i].width > space_left:
                            endl.append(pos)
                            space_left = max_w - self[i].width
                        else:
                            space_left -= self[i].width
                        pos += 1
                else:
                    if word[2] > space_left:
                        endl.append(pos)
                        space_left = max_w - word[2]
                    else:
                        space_left -= word[2]
                    pos += len(word[0])

            endl.append(len(self))
            self.end_of_lines = endl

    def split_to_lines2(self):

        if ONELINE in self.options:
            self.end_of_lines = [len(self)]

        else:
            self.end_of_lines = [0]
            # the width of each line. We subtract the margin
            max_width = self.real_w - 2 * (self.real_anchor[1] + self.real_circle_radius)

            line_w = 0
            for i, carac in enumerate(self):
                line_w += carac.width
                if line_w >= max_width:
                    j = i
                    while self[j].carac != ' ' and j > self.end_of_lines[-1]:
                        j -= 1
                    if j == self.end_of_lines[-1]:  # 2nd condition of the while loop
                        self.end_of_lines.append(i)
                    else:
                        self.end_of_lines.append(j+1)  # j is the space, he on the line

                    line_w = 0
                    for k in range(j, i):
                        line_w += self[k].width
                    line_w = carac.width

            self.end_of_lines.append(len(self))
            self.end_of_lines = self.end_of_lines[1:]  # we remove the first 0 whose not an and of line

    @only_if_object_changes
    def render(self):
        if ADAPT_L in self.options:
            self.w = self.width + 2 * self.real_anchor[1]

        size_of_rect_changed = Rectangle.render(self)

        if size_of_rect_changed is not None:  # if the rectangle size has changed
            self.font = self.font  # actualisation of the font size
            self.split_to_lines()
        elif self.previous_state['width'] != self.width:
            self.split_to_lines()

        offset_x = self.real_anchor[1] + self.real_circle_radius
        offset_y = self.real_anchor[2]

        if ONELINE in self.options:
            # we do a di(ego)chotomy
            borne_a = 0
            borne_b = self.font_size

            while self.font_size != borne_a:

                w = self.width + 2 * offset_x
                h = self.height + 2 * offset_y

                if w < self.real_w and h < self.real_h:  # the text can grow up
                    borne_a = self.font_size
                    self.font_size = int((borne_a + borne_b)/2)

                else:  # w > self.real_w or h > self.real_h:  # something is too big
                    borne_b = self.font_size
                    size = int((borne_a + borne_b) / 2)
                    self.font_size = size

        elif FILL_SPACE in self.options:

            while self.rendered_height + 2 * offset_y <= self.real_h:
                self.increment_font_size(1)
            while self.rendered_height + 2 * offset_y > self.real_h:
                self.increment_font_size(-1)

        # we find the right y position to start rendering the lines
        if self.relative_anchor[0][0] == 't':  # align to the top
            y = offset_y

        elif self.relative_anchor[0][0] == 'c':  # centred
            total_height = 0
            a = 0
            for end_line in self.end_of_lines:  # end_line is an int
                total_height += self[a: end_line].height
                a = end_line
            y = (self.real_h - total_height) / 2

        elif self.relative_anchor[0][0] == 'b':  # align to the bottom
            total_height = 0
            a = 0
            for end_line in self.end_of_lines:  # end_line is an int
                total_height += self[a: end_line].height
                a = end_line
            y = self.real_h - total_height - offset_y
        else:
            y = 1 / 0

        a = 0
        for end_line in self.end_of_lines:  # end_line is an int
            delta_x = 0
            global_ascent = self[a: end_line].ascent

            # find the x position for the line who'll be rendered
            if self.relative_anchor[0][1] == 'l':  # align left
                x = offset_x
            elif self.relative_anchor[0][1] == 'c':  # centered horizontally
                x = (self.real_w - self[a: end_line].width) / 2
            elif self.relative_anchor[0][1] == 'r':  # align right
                x = self.real_w - offset_x - self[a: end_line].width
            else:
                raise Exception

            for carac in self[a:end_line]:

                carac.render()
                self.blit(carac.surface, (x + delta_x, y + global_ascent - carac.ascent))
                delta_x += carac.width

            y += self[a: end_line].height
            a = end_line

        self.convert_alpha()

    def update(self):
        FlyingText.update(self)
        Rectangle.update(self)


class SText(Text):
    def __init__(self, text, rect_args=None, font=None, color=BLACK, anchor=None, options=NO):
        """ Params are exactly same as a Text object """
        self._cursor_position = 0
        self.focus = False
        self.cursor_time = 0

        Text.__init__(self, text, rect_args, font, color, anchor, options)

    def __repr__(self):
        return super(SText, self).__repr__() + ' \nCursor: ' + str((self.focus, self.cursor_position, self.cursor_time < 65))

    def __state__(self):
        dic = dict()
        dic.update(Text.__state__(self))
        dic['focus'] = self.focus
        dic['cursor_time'] = self.cursor_time < 65
        dic['cursor_position'] = self.cursor_position
        return dic

    @property
    def cursor_position(self):
        return self._cursor_position

    @cursor_position.setter
    def cursor_position(self, value):
        if value < 0:
            value = 0
        elif value > len(self):
            value = len(self)

        self._cursor_position = value

    def set_cursor_pos_from_mouse(self, inputs):
        x = self.real_x + self.real_anchor[1] + self.real_circle_radius
        y = self.real_y + self.real_anchor[2]
        goal_x = inputs['mouse']['real x']
        goal_y = inputs['mouse']['real y']

        if goal_y <= y:
            i_line = 0

            beg_of_the_line = 0

        elif goal_y >= self.rendered_height:
            i_line = len(self.end_of_lines) - 1

            if len(self.end_of_lines) == 1:
                beg_of_the_line = 0
            else:
                beg_of_the_line = self.end_of_lines[-2]

        else:
            current_h = y
            beg_of_line = 0
            i_line = 0

            while goal_y >= current_h:
                current_h += self[beg_of_line: self.end_of_lines[i_line]].height
                beg_of_line = self.end_of_lines[i_line]
                i_line += 1

            beg_of_the_line = beg_of_line

        if goal_x <= x:
            if i_line == 0:
                self.cursor_position = 0
            else:
                self.cursor_position = self.end_of_lines[i_line - 1]
        else:
            current_x = x
            self.cursor_position = beg_of_the_line
            while current_x < goal_x and self.cursor_position < len(self) - 1:  # -1 because we add 1 in the next line
                self.cursor_position += 1
                current_x += self[self.cursor_position].width

    @property
    def real_cursor_position(self):
        """
        Returns the point right after the carac number. The point y is on the top of the line.
        The coordinates are depending on the top left corner of the text. NOT THE TOPLEFT OF THE SCREEN !
        """

        num_carac = self.cursor_position
        if num_carac != 0:
            num_line = 0

            # getting the num of the line
            for end_of_line in self.end_of_lines:
                if end_of_line < num_carac:
                    num_line += 1

            # get the height of those lines
            pos_y = 0
            beginning_of_line = 0
            for end_of_line in self.end_of_lines[0:num_line]:
                # I'm ONLY getting the height of the line
                pos_y += self[beginning_of_line: end_of_line].height
                beginning_of_line = end_of_line

            # now we have the y position of the cursor_position
            # getting the x positon
            pos_x = self[beginning_of_line: num_carac].width
            # add the margin
            pos_x += self.real_anchor[1] + self.real_circle_radius
            pos_y += 3

            # height depends on the carac before the cursor_position --> self.cursor_position - 1
            return (pos_x, pos_y), (pos_x, pos_y + self[self.cursor_position - 1].height - 5)
        else:
            pos_x = self.real_anchor[1] + self.real_circle_radius
            return (pos_x, 2), (pos_x, self.font_size - 3)

    def update(self):
        Text.update(self)

        if self.mouse_click_area(1):
            self.focus = True
            self.set_cursor_pos_from_mouse(borg_baby.inputs)
        elif borg_baby.inputs.mouse_click:  # outside the text
            self.focus = False

        if self.focus:
            self.cursor_time += 1
            self.cursor_time %= 80

    @only_if_object_changes
    def render(self):
        Text.render(self)

        if self.cursor_time < 65 and self.focus:  # the cursor_position tic tac && the box must be clicked
            pos = self.real_cursor_position  # If needed
            pygame.draw.line(self, GREY_75, pos[0], pos[1])  # we draw the cursor_position

        self.convert_alpha()


class TextBox(SText):
    def __init__(self, default_text, rect_args, font=None, color=BLACK, anchor=None, options=NO):

        super().__init__('', rect_args, font, color, anchor, options)

        def_font = f.Font(*self.default_font)
        def_font.italic = True
        self.default_text = Text(default_text, rect_args, def_font, GREY_50, anchor)
        self.last_entered_text = ''

    def __repr__(self):
        return "TextBox :" + self.last_entered_text + SText.__repr__(self)

    def __state__(self):
        state = dict()
        state.update(SText.__state__(self))
        state['last_entered_text'] = self.last_entered_text
        return state

    def update(self):
        """
        Changes the text depending on the inputs
        If the text changes, this update the surface too by calling render_self()
        """

        super(TextBox, self).update()

        if self.focus:

            for event in Borg().inputs.list_events:
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_BACKSPACE:  # if we want to delete a carac :
                        if self.cursor_position > 0:  # we can not suppress the -1th letter
                            del self[self.cursor_position - 1]  # we suppress the letter at the cursor_position
                            self.cursor_position -= 1

                    # enter press
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        self.last_entered_text = self.text
                        self.text = ''  # we reset the text
                        self.cursor_position = 0

                    elif event.key == pygame.K_DELETE:
                        if self.cursor_position < len(self):
                            del self[self.cursor_position]

                    # if any arrow is pressed
                    if event.key == pygame.K_RIGHT:
                        self.cursor_position += 1
                        if self.cursor_position > len(self):
                            self.cursor_position = len(self)

                    elif event.key == pygame.K_LEFT:
                        self.cursor_position -= 1
                        if self.cursor_position < 0:
                            self.cursor_position = 0

                    elif event.dict['unicode'].isprintable() and len(event.dict['unicode']) == 1:
                        carac = event.dict['unicode']  # we get the pressed touch by his unicode
                        # we add a letter at the cursor_position poss
                        self.insert(self.cursor_position, carac)
                        self.cursor_position += 1

    @only_if_object_changes
    def render(self):
        if self.text == '' and not self.focus or (NO_CURSOR in self.options and self.text == ''):
            self.fill(TRANSPARENT)
            self.default_text.render()
            self.blit(self.default_text, (0, 0))
        else:
            if NO_CURSOR in self.options:
                Text.render(self)
            else:
                SText.render(self)

        self.convert_alpha()


class PasswordBox(TextBox):
    def __init__(self, default_text, rect_args, font=None, options=NO):
        super(PasswordBox, self).__init__(default_text, rect_args, font, options=options)
        self.hash_pass = ''
        fo = f.Font(*self.default_font)
        fo.italic = True
        self.false_text = Text('', self.rect_as_tuple, fo, self.default_text.text_color, self.anchor, self.options)

        x = lambda pswbx: pswbx.relative_x + pswbx.relative_w - pswbx.relative_h

        self.show_real_area = Area(lambda: x(self), self._y, self._h, self._h)
        self.showing = False

        self.previous_state = self.__state__()
        self.previous_state['f'] = 1

    def __state__(self):
        s = dict()
        s.update(super(PasswordBox, self).__state__())
        s['hash pass'] = self.hash_pass
        s['showing'] = self.showing
        return s

    def update(self):
        super(PasswordBox, self).update()
        self.hash_pass = hash(self.text)
        if self.show_real_area.mouse_click_area(1):
            self.showing = True
        elif self.show_real_area.mouse_click_area(1, option=IS_PRESSED):
            # we do not need to change anything
            pass
        else:
            self.showing = False

    @only_if_object_changes
    def render(self):
        self.fill(TRANSPARENT)

        if self.text == '' and not self.focus or (NO_CURSOR in self.options and self.text == ''):  # noting in the box
            self.fill(TRANSPARENT)  # so we blit the
            self.default_text.render()  # default text
            self.blit(self.default_text, (0, 0))
        else:
            if self.hash_pass != self.previous_state['hash pass']:  # the password changes
                self.false_text.text = random_string(len(self))  # we make a new false text
                self.false_text.render()
            if self.showing:
                print(yayy)
                if NO_CURSOR in self.options:
                    Text.render(self)
                else:
                    SText.render(self)
            else:
                self.blit(self.false_text, (0, 0))
            self.blit(icons.eye_icon.get(self.show_real_area.real_h),
                      self.show_real_area.real_topleft - self.real_topleft)

        self.convert_alpha()

__all__ = ['Carac', 'FlyingText', 'Text', 'SText', 'TextBox', 'PasswordBox']
