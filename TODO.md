# Todo

- [x] Finalize card top with custom button (maximaze)
- [x] maybe on top of maximaze, add a toolbox so that we can
- [x] Finalize preview and move it to main.py
- [x] improve CustomItemWidget design with timestamp, previe, action button,
- [x] run text_component_widgets
- [x] Finalize list and move it to main.py
- [x] Improve background and finalize all the design
- [x] Create a clipboardList that take a list of CustomItemWidget and show them,
- [x] Palletes button in settings to change color, dark mode, light mode, default
- [-] Add simple/MVP-level clipboard behavior and behavior , Update CustomItemWidget with function add_item, remove_item, delete_all, get_item, etc.
  - [x] delete all & copy again to test that it is really deleted
  - [x] delete per item
  - [x] On list_item_clik - update clipboard + update preview context
  - [x] Fix preview stylings
  - [x] Handle urls/read file contetent just keep title? or just the references? Bugs
  - [x] make simple search works
  - [x] Change cursor on button just like the color_chooser btn
  - [x] Prebiewbutton tools -  capitalize, lower, uppcase
  - [x] Style confirmation buttons & mske menu consistent in theme
  - [x] Fix status messages
- [ ] Refactor  add variable, comments etc.
- [ ] Makeit cross-platform installable with one-click
- [ ] settings button  (api for ocr + vision understand model("summarize what this image represents"), topic modeling text ), saved secrets in settings allways there
- [ ] Create a tree of all the software and the widgets dependency graph


pyside6==6.10.0 pyside6-addons==6.10.0 pyside6-essentials==6.10.0

[[source]]
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"

[packages]
pyside6 = "==6.10.0"
pyside6-addons = "==6.10.0"
pyside6-essentials = "==6.10.0"
pynput = "==1.8.1"
keyboard = "==0.13.5"
pyautogui = "==0.9.54"
pillow = "==12.0.0"
pyperclip = "==1.11.0"
pytesseract = "==0.3.13"
mss = "==10.1.0"
paddleocr = "*"
easyocr = "*"

[dev-packages]

[requires]
python_version = "3.13"
