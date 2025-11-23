# **TODO**

### **Core UI & Layout**

* [x] Finalize card header with custom maximize button
* [x] Add optional toolbox above the maximize button
* [x] Finalize preview component and move it to `main.py`
* [x] Improve `CustomItemWidget` design (timestamp, preview, action buttons)
* [x] Run `text_component_widgets`
* [x] Finalize list component and move it to `main.py`
* [x] Improve background styling and finalize overall design
* [x] Create `ClipboardList` that accepts a list of `CustomItemWidget` instances and displays them
* [x] Add palette selector in settings (dark mode / light mode / default)

### **Clipboard Behavior (MVP)**

* [x] Add simple/MVP-level clipboard behavior; update `CustomItemWidget` with basic item operations:

  * [x] `delete_all` + verify clipboard resets properly
  * [x] Per-item delete
  * [x] On list item click → update system clipboard + update preview context
  * [x] Fix preview styling
  * [x] Handle URLs / file content — show title or reference only
  * [x] Make simple search work
  * [x] Change cursor on buttons (matching color_chooser cursor style)
  * [x] Add preview tools: capitalize / lowercase / uppercase
  * [x] Style confirmation buttons & unify theme between menus
  * [x] Fix status messages

### **Refactoring & Architecture**

* [x] Quick refactor (variables, comments, cleanups)
* [x] Make app cross-platform and one-click installable

### **Bug Fixes**

* [x] Fix bug where images disappear after deleting search text (remove Enter handler, simplify logic)
* [x] Add system tray integration

### **Persistence**

* [-] Database? Currently data resets on each restart (in-memory only)

### **Settings & Integrations**

* [ ] Add Settings buttingd:
  * [ ] API inputs for OCR
  * [ ] Vision/understanding model (“summarize what this image represents”)
  * [ ] Topic modeling for text
  * [ ] Saved secrets that persist in settings & does not show on clipboard list
