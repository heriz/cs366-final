import urwid
import sys, os
wd = os.getcwd()
sys.path.insert(0, wd+"/scripts")
import markov
import naive_tags
import jumble

def menu_button(caption, callback):
    button = urwid.Button(caption)
    urwid.connect_signal(button, 'click', callback)
    return urwid.AttrMap(button, None, focus_map='reversed')

def sub_menu(caption, choices):
    contents = menu(caption, choices)
    def open_menu(button):
        return top.open_box(contents)
    return menu_button([caption, u'...'], open_menu)

def menu(title, choices):
    body = [urwid.Text(title), urwid.Divider()]
    body.extend(choices)
    return urwid.ListBox(urwid.SimpleFocusListWalker(body))

def item_chosen(button):
    response = urwid.Text([u'You chose ', button.label, u': check gen.txt for output!\n'])
    handle_choices(button.label)
    done = menu_button(u'OK', exit_program)
    top.open_box(urwid.Filler(urwid.Pile([response, done])))

def exit_program(button):
    raise urwid.ExitMainLoop()

menu_top = menu(u'Style of Message', [
    sub_menu(u'Formal', [
        menu_button(u'Formal Markov Chain', item_chosen),
        menu_button(u'Formal Naive', item_chosen),
        menu_button(u'Formal Word Replacement', item_chosen),
    ]),
    sub_menu(u'Medium Formal', [
        menu_button(u'Medium Formal Markov Chain', item_chosen),
        menu_button(u'Medium Formal Naive', item_chosen),
        menu_button(u'Medium Formal Word Replacement', item_chosen),
    ]),

    sub_menu(u'Informal', [
        menu_button(u'Informal Markov Chain', item_chosen),
        menu_button(u'Informal Naive', item_chosen),
        menu_button(u'Informal Word Replacement', item_chosen),
    ]),
])

def handle_choices(choice):
  if (choice == 'Formal Markov Chain'):
    markov.generate_email("greeting","body","closing","gen.txt")
  elif (choice == 'Formal Naive'):
    naive_tags.replace_and_output("data/naive/cappy.outline", 
        "gen.txt","data/naive/cappy.yaml")
  elif (choice == 'Formal Word Replacement'):
    markov.generate_email("greeting","body","closing","gen.txt", True)
  elif (choice == 'Medium Formal Markov Chain'):
    markov.generate_email("greeting","body","closing","gen.txt")
  elif (choice == 'Medium Formal Naive'):
    naive_tags.replace_and_output("data/naive/wordsmiths.outline",
        "gen.txt", "data/naive/wordsmiths.yaml")
  elif (choice == 'Medium Formal Word Replacement'):
    markov.generate_email("greeting","body","closing", "gen.txt", True)
  elif (choice == 'Informal Markov Chain'):
    markov.generate_email("greeting","body","closing","gen.txt")
  elif (choice == 'Informal Naive'):
    naive_tags.replace_and_output("data/naive/outings.outline",
        "gen.txt", "data/naive/outings.yaml")
  else:
    markov.generate_email("greeting","body","closing","gen.txt", True)
  
class CascadingBoxes(urwid.WidgetPlaceholder):
    max_box_levels = 4

    def __init__(self, box):
        super(CascadingBoxes, self).__init__(urwid.SolidFill(u'/'))
        self.box_level = 0
        self.open_box(box)

    def open_box(self, box):
        self.original_widget = urwid.Overlay(urwid.LineBox(box),
            self.original_widget,
            align='center', width=('relative', 80),
            valign='middle', height=('relative', 80),
            min_width=24, min_height=8,
            left=self.box_level * 3,
            right=(self.max_box_levels - self.box_level - 1) * 3,
            top=self.box_level * 2,
            bottom=(self.max_box_levels - self.box_level - 1) * 2)
        self.box_level += 1

    def keypress(self, size, key):
        if key == 'esc' and self.box_level > 1:
            self.original_widget = self.original_widget[0]
            self.box_level -= 1
        else:
            return super(CascadingBoxes, self).keypress(size, key)

if __name__ == "__main__":
  top = CascadingBoxes(menu_top)
  urwid.MainLoop(top, palette=[('reversed', 'standout', '')]).run()
