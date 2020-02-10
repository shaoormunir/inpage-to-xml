with open("test-utf.txt", encoding="utf-8") as f:
    data = f.read()

paras = 0
blockquotes = 0
sections = 0
previous_symbol = ""

blockquote = ""

blockquote_running = False

for symbol in data:
    if blockquote_running:
        blockquote+=symbol
    if previous_symbol == ":" and symbol == "\n":
        print("Found a blockquote")
        blockquote_running = True
        blockquotes += 1
    elif symbol == previous_symbol == "\n":
        print("Found a section break")
        sections += 1
    elif symbol == "\n":
        if blockquote_running:
            blockquote_running = False
            print (f"Blockquote: {blockquote}")
            blockquote = ""
        paras += 1
    previous_symbol = symbol
print(f"Total {paras} paras were found")
print(f"Total {sections} sections were found")
print(f"Total {blockquotes} blockquotes were found")
