#!/usr/bin/env python3
"""
A simple formatter for making questionaires in PsyToolbox faster by Jakub Jędrusiak.
"""

import sys
import os
from re import match, sub
import tkinter
import customtkinter as CTk
from PIL import ImageTk

CTk.set_appearance_mode("dark")  # Modes: system (default), light, dark

type_group_free = ["radio", "drop"]  # o: free
type_group_requie = ["check"]  # o: requie
type_group_rank = ["rank"]
type_group_info = ["info"]  # o: end


def format_text():
    """
    Main formatting function
    """
    label_text = label_input.get().strip()
    lines = input_text.get("1.0", "end").strip().split("\n")
    output = ""
    count = 1  # for labels

    for line in lines:
        if line in ["----", "page: begin", "page: end"]:
            output += f"{line}\n\n"
            continue
        output += f"l: {label_text}_{count}\nt: {question_type.get()}\n"

        if button_input.get().strip() != "":
            output += f"b: {button_input.get().strip()}\n"

        # check if the question has asterisk at the end
        if line.endswith("*"):
            reversed_scoring = True
            line = line[:-1]
        else:
            reversed_scoring = False

        # Options
        output += print_options()

        # Question
        output += f"q: {line}\n"
        output += print_answers(reversed_scoring)
        count += 1

    output_text.delete("1.0", "end")
    output_text.insert("1.0", output.strip())


def print_options():
    """
    Prints options "o: " in the output
    """
    output = ""
    # Options
    if random.get():
        output += "o: random\n"
    if link.get():
        output += "o: link\n"
    if question_type.get() in type_group_info and end.get():
        output += "o: end\n"
    if question_type.get() in type_group_free and free.get():
        output += "o: free\n"
    if question_type.get() in type_group_requie and requie.get():
        output += "o: requie"
        if min_entry.get() != "":
            output += f" {min_entry.get().strip()}"
            if max_entry.get() != "":
                output += f" {max_entry.get().strip()}"
        output += "\n"
    if sep.get():
        output += "o: sep\n"
    if qf.get():
        output += "o: qf\n"
    if numbers.get():
        output += "o: numbers\n"
    return output


def print_answers(reversed_scoring):
    """
    Prints answers "- " in the output, reverses scoring if reversed_scoring is True
    """
    output = ""
    # Get scores list
    answers = scale_text.get("1.0", "end").strip().split("\n")
    scores = []
    for scale_entry in answers:
        is_scored = match(r"{score=(\d+)}\s*(.*)", scale_entry)
        if is_scored:
            scores.append(int(is_scored.group(1)))
    # Answers
    score_number = 0
    if reversed_scoring:
        current_scores = list(reversed(scores))
    if len(answers) > 1 or answers[0] != "":
        for scale_entry in answers:
            if reversed_scoring:
                is_scored = match(r"{score=\d+}\s*(.*)", scale_entry)
                if is_scored:
                    answer = is_scored.group(1)
                    # inserts next element from scores list
                    score = current_scores[score_number]
                    output += f"- {{score={score}}} {answer}\n"
                    score_number += 1
                else:
                    output += f"- {scale_entry}\n"
            else:
                output += f"- {scale_entry}\n"
    output += "\n"
    return output


def copy_to_clipboard():
    """
    Copy to clipboard function
    """
    formatted_text = output_text.get("1.0", "end").strip()
    if formatted_text:
        root.clipboard_clear()
        root.clipboard_append(formatted_text)


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def select_all(event):
    """
    Selects all text in a text widget
    """
    event.widget.tag_add(tkinter.SEL, "1.0", tkinter.END)
    event.widget.mark_set(tkinter.INSERT, "1.0")
    event.widget.see(tkinter.INSERT)
    return "break"


def bind_all_text_widgets(parent):
    """
    Binds select all shortcut to ctrl+a in all text widgets
    """
    for widget in parent.winfo_children():
        if isinstance(widget, CTk.CTkTextbox):
            widget.bind("<Control-a>", select_all)
        else:
            bind_all_text_widgets(widget)


def clear_text():
    """
    Clears all text widgets
    """
    input_text.delete("1.0", "end")
    output_text.delete("1.0", "end")
    label_input.delete("0", "end")


# root
root = CTk.CTk()
root.title("PsyToolkit Questionnaire Formatter")
photo = ImageTk.PhotoImage(file=resource_path("./images/brain.png"))
root.wm_iconphoto(True, photo)

left_frame = CTk.CTkFrame(root)
right_frame = CTk.CTkFrame(root)
options_frame = CTk.CTkFrame(right_frame)

left_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nesw")
right_frame.grid(row=2, column=1, padx=10, pady=10, sticky="new")
options_frame.pack(padx=10, ipadx=5, pady=10,
                   anchor="nw", side="bottom", fill="x")

root.rowconfigure(2, weight=1)
root.columnconfigure(0, weight=2)
root.columnconfigure(1, weight=1)

# Options checkboxes
random = tkinter.BooleanVar()
end = tkinter.BooleanVar()
link = tkinter.BooleanVar()
free = tkinter.BooleanVar()
requie = tkinter.BooleanVar()
sep = tkinter.BooleanVar()
qf = tkinter.BooleanVar()
numbers = tkinter.BooleanVar()
checkboxes_vars = [random, end, link, free, requie, sep, qf, numbers]

random_button = CTk.CTkCheckBox(
    options_frame, text="Show items in a random order", variable=random
)
end_button = CTk.CTkCheckBox(
    options_frame, text="End questionnaire after this question", variable=end
)
link_button = CTk.CTkCheckBox(
    options_frame,
    text="Link to previous question (typically not necessary)",
    variable=link,
)
free_button = CTk.CTkCheckBox(
    options_frame, text="Do not require participant to select any item", variable=free
)
requie_button = CTk.CTkCheckBox(
    options_frame, text="Require participant to select any item", variable=requie
)
sep_button = CTk.CTkCheckBox(
    options_frame, text="Save data anonymously", variable=sep)
qf_button = CTk.CTkCheckBox(
    options_frame, text="Show question text above image/video (if any)", variable=qf
)
numbers_button = CTk.CTkCheckBox(
    options_frame, text="Show numbers in front of items", variable=numbers
)

options_buttons = [
    "random_button",
    "end_button",
    "link_button",
    "numbers_button",
    "free_button",
    "requie_button",
    "sep_button",
    "qf_button",
]


def clear_options():
    """
    clears options checkboxes
    """
    for widget in options_buttons:
        globals()[widget].deselect()
        globals()[widget].pack_forget()


def show_options(question_type_selected):
    """
    shows options checkboxes based on question type
    """
    clear_options()
    for widget in options_buttons:
        globals()[widget].pack(pady=5, anchor="w")
    if question_type_selected in type_group_free:
        end_button.pack_forget()
        requie_button.pack_forget()
        numbers_button.pack_forget()
    elif question_type_selected in type_group_requie:
        end_button.pack_forget()
        free_button.pack_forget()
        requie_button.configure(command=requie_borders)
        numbers_button.pack_forget()
    elif question_type_selected in type_group_rank:
        end_button.pack_forget()
        free_button.pack_forget()
        requie_button.pack_forget()
    elif question_type_selected in type_group_info:
        random_button.pack_forget()
        free_button.pack_forget()
        requie_button.pack_forget()
        sep_button.pack_forget()
        numbers_button.pack_forget()


min_label = CTk.CTkLabel(options_frame, text="Minimum requied:")
max_label = CTk.CTkLabel(options_frame, text="Maximum requied:")
max_entry = CTk.CTkEntry(options_frame, width=300)
min_entry = CTk.CTkEntry(options_frame, width=300)


def requie_borders():
    """
    minimum and maximum textboxes for o: requie
    """
    if question_type.get() in type_group_requie and requie.get():
        min_label.pack()
        min_entry.pack()
        max_label.pack()
        max_entry.pack()
    else:
        min_label.pack_forget()
        min_entry.pack_forget()
        max_label.pack_forget()
        max_entry.pack_forget()


# Dropdown menu for selecting type of input
question_type = CTk.StringVar(value="radio")
input_label = CTk.CTkLabel(root, text="Question type:")
input_menu = CTk.CTkOptionMenu(
    root,
    values=type_group_free + type_group_requie + type_group_rank + type_group_info,
    variable=question_type,
    command=show_options,
)
input_label.grid(row=0, column=0, pady=(5, 0), padx=10, sticky="w")
input_menu.grid(row=1, column=0, padx=10, columnspan=2, sticky="ew")

# Left frame
input_label = CTk.CTkLabel(left_frame, text="Enter text:")
input_text = CTk.CTkTextbox(left_frame, width=600)
label_label = CTk.CTkLabel(left_frame, text="Enter label:")
label_input = CTk.CTkEntry(left_frame, width=300)
format_button = CTk.CTkButton(left_frame, text="Format", command=format_text)
output_label = CTk.CTkLabel(left_frame, text="Formatted text:")
output_text = CTk.CTkTextbox(left_frame, width=600)
copy_button = CTk.CTkButton(
    left_frame, text="Copy to Clipboard", command=copy_to_clipboard
)
clear_button = CTk.CTkButton(left_frame, text="Clear", command=clear_text)

input_label.pack()
input_text.pack(fill="both", expand=True)
label_label.pack()
label_input.pack()
format_button.pack(pady=10)
output_label.pack()
output_text.pack(fill="both", expand=True)
clear_button.pack(side="bottom", pady=5)
copy_button.pack(side="bottom", pady=5)

# Right frame
# Scale
scale_label = CTk.CTkLabel(right_frame, text="Enter scale values:")
scale_text = CTk.CTkTextbox(right_frame)

scale_label.pack()
scale_text.pack(fill="x", expand=True)

# Scores
scoring_scheme = CTk.StringVar(value="incremental")
default_score = CTk.StringVar(value="1")
preserve_scores = CTk.BooleanVar()


def add_scores():
    """
    Adds scores to scales, incremental by default, preserves existing.
    """
    if not preserve_scores.get():
        remove_scores()
    text = scale_text.get("1.0", "end").strip()
    lines = text.split("\n")
    output = ""
    count = int(default_score.get()) - 1
    if scoring_scheme.get() == "decremental":
        count += len(lines) + 1
    for line in lines:
        if scoring_scheme.get() == "incremental":
            count += 1
        elif scoring_scheme.get() == "decremental":
            count -= 1
        if match(r"^{score *= *\d+} *", line):  # preserve existing
            output += f"{line}\n"
        else:
            output += f"{{score={count}}} {line}\n"
    scale_text.delete("1.0", "end")
    scale_text.insert("1.0", output.strip())


def remove_scores():
    """
    Removes scores from scale.
    """
    text = scale_text.get("1.0", "end").strip()
    lines = text.split("\n")
    output = ""
    for line in lines:
        output += sub(r"^\s*{score *= *\d+} *", "", line)
        output += "\n"
    scale_text.delete("1.0", "end")
    scale_text.insert("1.0", output.strip())


def score_options():
    """
    Opens Score Options window to change defaults
    """
    score_options_window = CTk.CTkToplevel(root)
    score_options_window.title("Score Options")
    score_options_window.geometry("300x210")
    score_options_window.resizable(False, False)

    scoring_scheme_label = CTk.CTkLabel(
        score_options_window, text="Scoring scheme:")
    scoring_scheme_dropdown = CTk.CTkOptionMenu(
        score_options_window,
        values=["incremental", "decremental", "fixed"],
        variable=scoring_scheme,
    )
    default_score_label = CTk.CTkLabel(
        score_options_window, text="Deafult score (to start from or end on):"
    )
    default_score_entery = CTk.CTkEntry(
        score_options_window, textvariable=default_score
    )
    preserve_scores_checkbox = CTk.CTkCheckBox(
        score_options_window,
        text="Preserve existing scores when adding",
        variable=preserve_scores,
    )
    scoring_note = CTk.CTkLabel(
        score_options_window,
        text="Note: add an asterisk * at the end\nof an item to invert scoring for the item.",
    )

    scoring_scheme_label.pack()
    scoring_scheme_dropdown.pack(pady=(0, 10))
    default_score_label.pack()
    default_score_entery.pack(pady=(0, 10))
    preserve_scores_checkbox.pack(pady=(0, 10))
    scoring_note.pack()


score_frame = CTk.CTkFrame(right_frame)
remove_scores_button = CTk.CTkButton(
    score_frame, text="Remove scores", command=remove_scores
)
score_options_button = CTk.CTkButton(
    score_frame, text="Score options", command=score_options
)
add_scores_button = CTk.CTkButton(
    score_frame, text="Add scores", command=add_scores)

score_frame.pack(pady=10)
remove_scores_button.pack(side=tkinter.LEFT)
score_options_button.pack(side=tkinter.LEFT, padx=(5, 5))
add_scores_button.pack(side=tkinter.LEFT)

# Non-standard continue button
button_label = CTk.CTkLabel(
    right_frame, text="Non-standard continue button text:")
button_input = CTk.CTkEntry(right_frame, width=300)

button_label.pack()
button_input.pack()

# Clear scores button


def clear_right_frame():
    """
    Restores right frame to default.
    """
    show_options(question_type.get())
    requie_borders()
    scale_text.delete("1.0", "end")
    button_input.delete(0, "end")


clear_scores_button = CTk.CTkButton(
    right_frame, text="Clear scores and options", command=clear_right_frame
)

clear_scores_button.pack(pady=10, side="bottom")

# Main window
show_options(question_type.get())  # show options for given question type

bind_all_text_widgets(root)  # apply ctrl+a to all text widgets

root.minsize(root.winfo_width() + 15, root.winfo_height())

root.mainloop()
