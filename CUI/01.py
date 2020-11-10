from terminal_layout.extensions.choice import *
from terminal_layout import *
import time
from terminal_layout.extensions.progress import *

c = Choice('Which is the Best Programming Language? (press <esc> to exit) ',
           ['Python', 'C/C++', 'Java', 'PHP', 'Go', 'JS', '...'],
           icon_style=StringStyle(fore=Fore.blue),
           selected_style=StringStyle(fore=Fore.blue))

choice = c.get_choice()
if choice:
    index, value = choice
    print(value, 'is the Best Programming Language')


p = Progress("Initializer", 20)
p.start()
p.set_progress(2)
time.sleep(0.3)
for i in range(10):
    if p.is_finished():
        break
    time.sleep(0.3)
    p.add_progress(i - 1)
p.stop()

print("\033[30m[FindPlugin: 8]\033[0m")

p = Progress("SearchModel", 20)
p.start()
p.set_progress(2)
time.sleep(0.3)
for i in range(10):
    if p.is_finished():
        break
    time.sleep(0.3)
    p.add_progress(i - 1)
p.stop()

print("\033[30m[SearchModel: 8]\033[0m")
