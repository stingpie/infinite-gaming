import toolcalls
import os

os.system("bash reset.bash")

print(toolcalls.createfile({"name":"test.txt"}))
print(toolcalls.readfile({"name":"test.txt","firstline":0, "lastline":100}))
print(toolcalls.insertlines({"name":"test.txt","firstline":0,"text":"yaba daba \n doooooo\n\n\n\nyah"}))
#print(toolcalls.readfile({"name":"test.txt", "firstline":0, "lastline":2}))
print(toolcalls.replaceline({"name":"test.txt", 'line':3, "text":"Qouth the Raven, 'Nevermore.'"}))
#print(toolcalls.readfile({'name':'test.txt', 'firstline':0, 'lastline':6}))
print(toolcalls.removelines({"name":'test.txt', 'firstline':0, 'lastline':2}))
#print(toolcalls.readfile({'name':'test.txt', 'firstline':0, 'lastline':100}))

print(toolcalls.insertlines({'name':'test.txt', 'firstline':4,'text':'Once upon a midnight dreary,\nwhilst I pondered weak and weary,\nover many a volume of forgotten lore,\nthere came a knocking, rapping, nearly tapping,\ntapping on my chamber\'s door.'}))

print(toolcalls.readfile({'name':'test.txt', 'firstline':0, 'lastline':100}))



