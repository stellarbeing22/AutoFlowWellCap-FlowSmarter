import tkinter as tk
import tkinter.font as tkFont

# List of font names from your provided list (for demonstration)
font_names = [
    "System", "Terminal", "Fixedsys", "Modern", "Roman", "Script", "Marlett",
    "Arial", "Arabic Transparent", "Arial Baltic", "Arial CE", "Arial CYR", "Arial Greek", "Arial TUR",
    "Arial Black", "Bahnschrift Light", "Bahnschrift SemiLight", "Bahnschrift", "Bahnschrift SemiBold",
    "Bahnschrift Light SemiCondensed", "Bahnschrift SemiLight SemiConde", "Bahnschrift SemiCondensed",
    "Bahnschrift SemiBold SemiConden", "Bahnschrift Light Condensed", "Bahnschrift SemiLight Condensed",
    "Bahnschrift Condensed", "Bahnschrift SemiBold Condensed", "Calibri", "Calibri Light", "Cambria",
    "Cambria Math", "Candara", "Candara Light", "Comic Sans MS", "Consolas", "Constantia", "Corbel",
    "Corbel Light", "Courier New", "Courier New Baltic", "Courier New CE", "Courier New CYR",
    "Courier New Greek", "Courier New TUR", "Ebrima", "Franklin Gothic Medium", "Gabriola", "Gadugi",
    "Georgia", "HoloLens MDL2 Assets", "Impact", "Ink Free", "Javanese Text", "Leelawadee UI",
    "Leelawadee UI Semilight", "Lucida Console", "Lucida Sans Unicode", "Malgun Gothic", "@Malgun Gothic",
    "Malgun Gothic Semilight", "@Malgun Gothic Semilight", "Microsoft Himalaya", "Microsoft JhengHei",
    "@Microsoft JhengHei", "Microsoft JhengHei UI", "@Microsoft JhengHei UI", "Microsoft JhengHei Light",
    "@Microsoft JhengHei Light", "Microsoft JhengHei UI Light", "@Microsoft JhengHei UI Light",
    "Microsoft New Tai Lue", "Microsoft PhagsPa", "Microsoft Sans Serif", "Microsoft Tai Le",
    "Microsoft YaHei", "@Microsoft YaHei", "Microsoft YaHei UI", "@Microsoft YaHei UI", "Microsoft YaHei Light",
    "@Microsoft YaHei Light", "Microsoft YaHei UI Light", "@Microsoft YaHei UI Light", "Microsoft Yi Baiti",
    "MingLiU-ExtB", "@MingLiU-ExtB", "PMingLiU-ExtB", "@PMingLiU-ExtB", "MingLiU_HKSCS-ExtB",
    "@MingLiU_HKSCS-ExtB", "Mongolian Baiti", "MS Gothic", "@MS Gothic", "MS UI Gothic", "@MS UI Gothic",
    "MS PGothic", "@MS PGothic", "MV Boli", "Myanmar Text", "Nirmala UI", "Nirmala UI Semilight", "Palatino Linotype",
    "Sans Serif Collection", "Segoe Fluent Icons", "Segoe MDL2 Assets", "Segoe Print", "Segoe Script",
    "Segoe UI", "Segoe UI Black", "Segoe UI Emoji", "Segoe UI Historic", "Segoe UI Light", "Segoe UI Semibold",
    "Segoe UI Semilight", "Segoe UI Symbol", "Segoe UI Variable Small Light", "Segoe UI Variable Small Semilig",
    "Segoe UI Variable Small", "Segoe UI Variable Small Semibol", "Segoe UI Variable Text Light",
    "Segoe UI Variable Text Semiligh", "Segoe UI Variable Text", "Segoe UI Variable Text Semibold",
    "Segoe UI Variable Display Light", "Segoe UI Variable Display Semil", "Segoe UI Variable Display",
    "Segoe UI Variable Display Semib", "SimSun", "@SimSun", "NSimSun", "@NSimSun", "SimSun-ExtB",
    "@SimSun-ExtB", "Sitka Small", "Sitka Small Semibold", "Sitka Text", "Sitka Text Semibold", "Sitka Subheading",
    "Sitka Subheading Semibold", "Sitka Heading", "Sitka Heading Semibold", "Sitka Display", "Sitka Display Semibold",
    "Sitka Banner", "Sitka Banner Semibold", "Sylfaen", "Symbol", "Tahoma", "Times New Roman",
    "Times New Roman Baltic", "Times New Roman CE", "Times New Roman CYR", "Times New Roman Greek",
    "Times New Roman TUR", "Trebuchet MS", "Verdana", "Webdings", "Wingdings", "Yu Gothic", "@Yu Gothic",
    "Yu Gothic UI", "@Yu Gothic UI", "Yu Gothic UI Semibold", "@Yu Gothic UI Semibold", "Yu Gothic Light",
    "@Yu Gothic Light", "Yu Gothic UI Light", "@Yu Gothic UI Light", "Yu Gothic Medium", "@Yu Gothic Medium",
    "Yu Gothic UI Semilight", "@Yu Gothic UI Semilight", "Agency FB", "Algerian", "Arial Narrow",
    "Arial Rounded MT Bold", "Baskerville Old Face", "Bauhaus 93", "Bell MT", "Berlin Sans FB", "Berlin Sans FB Demi",
    "Bernard MT Condensed", "Blackadder ITC", "Bodoni MT", "Bodoni MT Black", "Bodoni MT Condensed",
    "Bodoni MT Poster Compressed", "Book Antiqua", "Bookman Old Style", "Bookshelf Symbol 7", "Bradley Hand ITC",
    "Britannic Bold", "Broadway", "Brush Script MT", "Californian FB", "Calisto MT", "Castellar", "Centaur", "Century",
    "Century Gothic", "Century Schoolbook", "Chiller", "Colonna MT", "Cooper Black", "Copperplate Gothic Bold",
    "Copperplate Gothic Light", "Curlz MT", "Dubai", "Dubai Light", "Dubai Medium", "Edwardian Script ITC",
    "Elephant", "Engravers MT", "Eras Bold ITC", "Eras Demi ITC", "Eras Light ITC", "Eras Medium ITC", "Felix Titling",
    "Footlight MT Light", "Forte", "Franklin Gothic Book", "Franklin Gothic Demi", "Franklin Gothic Demi Cond",
    "Franklin Gothic Heavy", "Franklin Gothic Medium Cond", "Freestyle Script", "French Script MT", "Garamond",
    "Gigi", "Gill Sans MT", "Gill Sans MT Condensed", "Gill Sans MT Ext Condensed Bold", "Gill Sans Ultra Bold",
    "Gill Sans Ultra Bold Condensed", "Gloucester MT Extra Condensed", "Goudy Old Style", "Goudy Stout",
    "Haettenschweiler", "Harlow Solid Italic", "Harrington", "High Tower Text", "Imprint MT Shadow", "Informal Roman",
    "Jokerman", "Juice ITC", "Kristen ITC", "Kunstler Script", "Lucida Bright", "Lucida Calligraphy", "Lucida Fax",
    "Lucida Handwriting", "Lucida Sans", "Lucida Sans Typewriter", "Magneto", "Maiandra GD", "Matura MT Script Capitals",
    "Mistral", "Modern No. 20", "Monotype Corsiva", "MS Outlook", "MS Reference Sans Serif", "MS Reference Specialty",
    "MT Extra", "Niagara Engraved", "Niagara Solid", "OCR A Extended", "Old English Text MT", "Onyx", "Palace Script MT",
    "Papyrus", "Parchment", "Perpetua", "Perpetua Titling MT", "Playbill", "Poor Richard", "Pristina", "Rage Italic",
    "Ravie", "Rockwell", "Rockwell Condensed", "Rockwell Extra Bold", "Script MT Bold", "Showcard Gothic", "Snap ITC",
    "Stencil", "Tempus Sans ITC", "Tw Cen MT", "Tw Cen MT Condensed", "Tw Cen MT Condensed Extra Bold", "Viner Hand ITC",
    "Vivaldi", "Vladimir Script", "Wide Latin", "Wingdings 2", "Wingdings 3", "DejaVu Sans", "DejaVu Sans Mono",
    "DejaVu Serif", "SimSun-ExtG", "@SimSun-ExtG", "Kruti Dev 011", "Kruti Dev 012", "Kruti Dev 013", "Kruti Dev 014",
    "Kruti Dev 016", "Kruti Dev 021", "Kruti Dev 022", "Kruti Dev 024", "Kruti Dev 100", "Kruti Dev 101",
    "Kruti Dev 102", "Kruti Dev 103", "Kruti Dev 104", "Kruti Dev 105", "Kruti Dev 106", "Kruti Dev 110",
    "Kruti Dev 111", "Kruti Dev 112", "Kruti Dev 114", "Kruti Dev 115", "Kruti Dev 116", "Kruti Dev 120",
    "Kruti Dev 121", "Kruti Dev 122", "Kruti Dev 123", "Kruti Dev 124", "Kruti Dev 125", "Kruti Dev 126",
    "Kruti Dev 130", "Kruti Dev 134", "Kruti Dev 135", "Kruti Dev 136", "Kruti Dev 140", "Kruti Dev 141",
    "Kruti Dev 142", "Kruti Dev 160", "Kruti Dev 010", "Cascadia Code ExtraLight", "Cascadia Code Light",
    "Cascadia Code SemiLight", "Cascadia Code", "Cascadia Code SemiBold", "Cascadia Mono ExtraLight",
    "Cascadia Mono Light", "Cascadia Mono SemiLight", "Cascadia Mono", "Cascadia Mono SemiBold"
]

# Create the main window
root = tk.Tk()
root.title("Font Display")

# Set the window size
root.geometry("600x800")

# Create a Text widget to display the fonts
text_widget = tk.Text(root, height=30, width=100)
text_widget.pack()

# Add each font to the text widget
for font_name in font_names:
    try:
        text_widget.insert(tk.END, f"Font: {font_name}\n", ("font_sample", font_name))
        text_widget.insert(tk.END, "Sample Text\n\n")
    except:
        text_widget.insert(tk.END, f"Font: {font_name} (Not Available)\n", ("font_sample", "Arial"))
        text_widget.insert(tk.END, "Sample Text\n\n")

# Apply tag for fonts
for font_name in font_names:
    text_widget.tag_configure(font_name, font=(font_name, 12))

root.mainloop()
