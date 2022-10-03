#import
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import*
import json

#window
app = QApplication([])
main_win = QWidget()
main_win.resize(800,600)
main_win.setWindowTitle("Clever Notes")

#widgets
main_text = QTextEdit()

l1 = QLabel("Note List")
note_list = QListWidget()
btn1 = QPushButton("create note")
btn2 = QPushButton("delete note")
btn3 = QPushButton("save note")

l2 = QLabel("Tag List")
tag_list = QListWidget()
tag_name = QLineEdit()
btn4 = QPushButton("add to note")
btn5 = QPushButton("delete from note")
btn6 = QPushButton("search note")

#layout
main_h1 = QHBoxLayout()
v1 = QVBoxLayout()
v2 = QVBoxLayout()
v1.addWidget(main_text)
v2.addWidget(l1)
v2.addWidget(note_list)
h2 = QHBoxLayout()
h3 = QHBoxLayout()
h2.addWidget(btn1)
h2.addWidget(btn2)
h3.addWidget(btn3)
v2.addLayout(h2)
v2.addLayout(h3)

v2.addWidget(l2)
v2.addWidget(tag_list)
h4 = QHBoxLayout()
h5 = QHBoxLayout()
h4.addWidget(btn4)
h4.addWidget(btn5)
h5.addWidget(btn6)
v2.addWidget(tag_name)
v2.addLayout(h4)
v2.addLayout(h5)

main_h1.addLayout(v1)
main_h1.addLayout(v2)
main_win.setLayout(main_h1)

#...
notes = {
"О планетах" : 
     	{
        		"текст" : "Что если вода на Марсе это признак жизни?",
        		"теги" : ["Марс", "гипотезы"]
    		},
"О чёрных дырах" : 
     	{
        		"текст" : "Сингулярность на горизонте событий отсутствует",
        		"теги" : ["чёрные дыры", "факты"]
    		}
}

with open ("data.json", "r") as file:
    notes = json.load(file)
    #json.dump(notes, file)

note_list.addItems(notes)

#note methods
def show_note():
    name = note_list.selectedItems()[0].text()
    main_text.setText(notes[name]["текст"])
    tag_list.clear()
    tag_list.addItems(notes[name]["теги"])

note_list.clicked.connect(show_note)

def add_note():
    name, ok = QInputDialog.getText(main_win, "add text", "note name")
    
    if ok and name != "":
        notes[name] = {
            "текст" : "", "теги" : []
        }
        note_list.addItem(name)

btn1.clicked.connect(add_note)

def save_note():
    if note_list.selectedItems:
        name = note_list.selectedItems()[0].text()
    
    if name != "":
        notes[name]["текст"] = main_text.toPlainText()
        with open ("data.json", "w") as file:
            json.dump(notes, file)

btn3.clicked.connect(save_note)

#tag methods
def add_tag():
    if note_list.selectedItems:
        name = note_list.selectedItems()[0].text()  
    
        if tag_name.text() != "" and tag_name.text() not in notes[name]["теги"]:
            notes[name]["теги"].append(tag_name.text())
            tag_list.addItem(tag_name.text())
            tag_name.clear()
            with open ("data.json", "w") as file:
                json.dump(notes, file)

btn4.clicked.connect(add_tag)                

def search_note():
    tag = tag_name.text()
    if btn6.text() == "search note":
        notes2 = {}
        for name in notes:
            if tag in notes[name]["теги"]:
                notes2[name] = notes[name]
        note_list.clear()
        note_list.addItems(notes2)
        btn6.setText("end search")
    else:
        note_list.clear()
        note_list.addItems(notes)
        btn6.setText("search note")
        tag_name.clear()

btn6.clicked.connect(search_note)

#show
main_win.show()
app.exec()