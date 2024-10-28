import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox, StringVar
from tokenizer import tokenize, TokenType
import os, platform, subprocess, random
import arabic_reshaper
from bidi.algorithm import get_display
import ttkbootstrap as tb
from tkinter.font import Font
import tempfile

# Configure Persian text processing
def process_text(input_text):
    if any('\u0600' <= char <= '\u06FF' for char in input_text):
        reshaped_text = arabic_reshaper.reshape(input_text)  
        bidi_text = get_display(reshaped_text)
        return bidi_text
    return input_text

# Main GUI Class
class BashCommandParserApp:
    def __init__(self, master):
        self.master = master
        self.master.title(process_text("تحلیلگر دستورات بش"))

        # Force window size and position
        self.master.geometry("1425x760+200+100")  # Set size and force open at specific screen location
        self.master.update_idletasks()  # Ensure geometry settings take effect
        self.master.resizable(False, False)  # Disable resizing for both width and height

        # Set font style and theme
        self.font = ("B Nazanin", 12, "bold")
        self.setup_ui()
        self.output_console.config(bg='#191212', fg='white')  # Black background for output console
        self.master.geometry("1425x760+200+100")  # Set size and force open at specific screen location
        self.master.update_idletasks()  # Ensure geometry settings take effect

    def setup_ui(self):
        # Top frame for buttons and theme selector
        top_frame = tb.Frame(self.master)
        top_frame.pack(side=tk.TOP, pady=10, fill=tk.X)

        # Buttons
        button_frame = tb.Frame(top_frame)
        button_frame.pack(side=tk.RIGHT, padx=5)

        self.create_button(button_frame, "تحلیل کد", self.process_code, "primary")
        self.create_button(button_frame, "پاک‌سازی خروجی", self.clear_output, "danger")
        self.create_button(button_frame, "پاک‌سازی کد", self.clear_code, "info")
        self.create_button(button_frame, "ذخیره کد", self.save_code, "success")
        self.create_button(button_frame, "بارگذاری کد", self.load_code, "warning")
        self.create_button(button_frame, "مستندات", self.open_docs, "light")
        self.create_button(button_frame, "بستن", self.exit_app, "dark")
        self.create_button(button_frame, "بزرگنمایی", self.zoom_in, "info")
        self.create_button(button_frame, "کوچکنمایی", self.zoom_out, "info")

        # Theme Selector
        theme_frame = tb.Frame(top_frame)
        theme_frame.pack(side=tk.LEFT, padx=5)
        tb.Label(theme_frame, text=process_text("انتخاب تم:"), bootstyle="info").pack(side=tk.RIGHT)

        self.theme_var = StringVar(value="solar")  # Default theme
        themes = ["darkly", "solar", "superhero", "cyborg", "vapor", "litera", "cosmo", "flatly", "journal", "minty"]
        theme_selector = tb.Combobox(theme_frame, textvariable=self.theme_var, values=themes, state="readonly", width=10)
        theme_selector.pack(side=tk.LEFT)
        theme_selector.bind("<<ComboboxSelected>>", self.change_theme)

        # Frames for code and output sections
        main_frame = tk.Frame(self.master)
        main_frame.pack(side=tk.TOP, padx=10, pady=10, fill=tk.BOTH, expand=True)

        left_frame = tb.Frame(main_frame, bootstyle="primary")
        left_frame.pack(side=tk.LEFT, fill=tk.Y)
        right_frame = tb.Frame(main_frame, bootstyle="secondary")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Line numbers and code input area
        self.line_numbers = tk.Text(left_frame, width=5, bg='lightgrey', fg='black', state='disabled')
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        self.code_input = scrolledtext.ScrolledText(left_frame, wrap=tk.WORD, width=60, height=40, bg='khaki', fg='black', font=("Courier New", 10))
        self.code_input.pack(side=tk.LEFT, fill=tk.Y, expand=True)
        self.code_input.bind("<KeyRelease>", lambda e: self.update_line_numbers())

        # Output console
        self.output_console = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD, width=110, height=40, bg='black', fg='white', font=("Courier New", 10))
        self.output_console.pack(fill=tk.BOTH, expand=True)

        # Display user information at the bottom
        text_frame = tb.Frame(self.master)
        text_frame.pack(side=tk.BOTTOM, anchor=tk.SE, pady=10, padx=10)
        tb.Label(text_frame, text=process_text("برنامه شبیه سازی کامپایلر | تولید شده توسط رضا خدارحیمی | 2024"), bootstyle="info").pack(side=tk.RIGHT)

        # Unicode Info Icon ℹ️
        info_icon = tk.Label(text_frame, text="♨", font=("Arial", 16), fg="blue", cursor="hand2")
        info_icon.pack(side=tk.RIGHT, padx=5)
        info_icon.bind("<Button-1>", self.open_readme)

        # Initialize line numbers
        self.update_line_numbers()

    def open_readme(self, event=None):
        # Path to the README.md file
        readme_path = os.path.join(os.getcwd(), 'README.md')

        if os.path.exists(readme_path):
            if platform.system() == "Windows":
                os.startfile(readme_path)  # Open with the default application on Windows
            elif platform.system() == "Linux":
                subprocess.Popen(['xdg-open', readme_path])  # Open with the default application on Linux
            elif platform.system() == "Darwin":  # macOS
                subprocess.Popen(['open', readme_path])  # Open with the default application on macOS
            else:
                print(f"Unsupported OS: {platform.system()}")
        else:
            messagebox.showerror("Error", "README.md file not found!")

    def create_button(self, parent, text, command, style):
        button = tb.Button(parent, text=process_text(text), bootstyle=style, command=command)
        button.pack(side=tk.LEFT, padx=5)

    # Process Code Function
    def process_code(self):
        code = self.code_input.get("1.0", tk.END)

        # Write the code to a temporary file to pass it to the LEX tokenizer
        with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.txt') as temp_code_file:
            temp_code_file.write(code)
            temp_code_file_path = temp_code_file.name

        # Run the LEX tokenizer using the temporary file
        tokens, total_tokens, token_count, error_percentage, whitespace_count, comment_count = tokenize(temp_code_file_path, verbose=True)

        self.output_console.delete("1.0", tk.END)

        # Insert header with proper tags
        self.output_console.insert(tk.END, "#!/bin/python3\n", "header_yellow")
        self.output_console.insert(tk.END, "##############################\n", "header_white")
        self.output_console.insert(tk.END, "# @ St.Id  : 4000711328                      #\n", "header_white")
        self.output_console.insert(tk.END, "#  Develop: Reza Khodarahimi        #\n", "header_white")
        self.output_console.insert(tk.END, "# 﫥 Copyright 2024                             #\n", "header_white")
        self.output_console.insert(tk.END, "##############################\n", "header_white")
        self.output_console.insert(tk.END, "-------------------------------------------------------------------------------\n", "header")
        self.output_console.insert(tk.END, " *** Bash Command Parser - Tokens Breakdown ***\n", "header")
        self.output_console.insert(tk.END, "-------------------------------------------------------------------------------\n\n", "header")

        line_number = 1
        for line in code.splitlines():
            self.output_console.insert(tk.END, f"Line {line_number}: ", "line_red")
            self.output_console.insert(tk.END, f"{line}\n", "line_cyan")
            self.output_console.insert(tk.END, "--------------------------------------------------------------------------------\n", "border")
            self.output_console.insert(tk.END, "| Line | Col | Token Type      | Value           | Description                          |\n", "border")
            self.output_console.insert(tk.END, "|------|-----|-----------------|-----------------|--------------------------------------|\n", "border")
            
            # Process tokens for the line
            line_tokens = [token for token in tokens if token.line == line_number]
            for token in line_tokens:
                desc = self.get_token_description(token)
                token_value = f"{token.value:<17}"

                # Map token types to their corresponding tags
                token_tag_map = {
                    TokenType.KEYWORD: "keyword",
                    TokenType.COMMAND: "command",
                    TokenType.OPERATOR: "operator",
                    TokenType.DELIMITER: "delimiter",
                    TokenType.IDENTIFIER: "identifier",
                    TokenType.NUMBER: "number",
                    TokenType.STRING_LITERAL: "string_literal",
                    TokenType.OPTION: "option",
                    TokenType.ARGUMENT: "argument",
                    TokenType.ERROR: "error",
                    TokenType.WHITESPACE: "whitespace",
                    TokenType.NEWLINE: "newline",
                    TokenType.COMMENT: "comment",
                    TokenType.AND: "operator",
                    TokenType.OR: "operator",
                    TokenType.EQUALS: "operator",
                    TokenType.NOT_EQUALS: "operator",
                    TokenType.LESS_OR_EQUAL: "operator",
                    TokenType.GREATER_OR_EQUAL: "operator",
                    TokenType.PLUS: "operator",
                    TokenType.MINUS: "operator",
                    TokenType.MULTIPLY: "operator",
                    TokenType.DIVIDE: "operator",
                    TokenType.ASSIGN: "operator",
                    TokenType.LESS_THAN: "operator",
                    TokenType.GREATER_THAN: "operator",
                    TokenType.NOT: "operator",
                    TokenType.COLON: "delimiter",
                    TokenType.SEPARATOR: "delimiter",
                    TokenType.PIPE: "operator",
                    TokenType.APPEND_REDIRECT: "operator",
                    TokenType.VARIABLE: "identifier"
                }

                tag = token_tag_map.get(token.token_type, "default")

                self.output_console.insert(tk.END, f"| {token.line:<4} | {token.column:<3} | {token.token_type:<15} | ", tag)
                self.output_console.insert(tk.END, token_value, tag)
                self.output_console.insert(tk.END, f"| {desc:<36} |\n", "line")

            self.output_console.insert(tk.END, "-------------------------------------------------------------------------------\n\n", "border")
            line_number += 1

        self.output_console.insert(tk.END, "-------------------------------------------------------------------------------\n", "summary")
        self.output_console.insert(tk.END, "Token Analysis Summary\n", "summary")
        self.output_console.insert(tk.END, "-------------------------------------------------------------------------------\n", "summary")
        self.output_console.insert(tk.END, f"Total Tokens: {total_tokens}\n", "header")

        # Display token counts
        for token_type, count in token_count.items():
            tag = "line"
            if token_type == TokenType.ERROR:
                tag = "error"
            elif token_type in token_tag_map:
                tag = token_tag_map[token_type]

            self.output_console.insert(tk.END, f"- {token_type} ", tag)
            self.output_console.insert(tk.END, f"(Count: {count})\n", "line")

        self.output_console.insert(tk.END, f"Error Percentage: {error_percentage:.2f}%\n", "error")
        self.output_console.insert(tk.END, "-------------------------------------------------------------------------------\n", "recommendations")
        self.output_console.insert(tk.END, "Recommendations for Fixes:\n", "recommendations")
        
        # Add recommendations based on common errors
        self.output_console.insert(tk.END, "1. Check for unrecognized characters or typos.\n", "recommendations")
        self.output_console.insert(tk.END, "2. Ensure all commands and keywords are correctly spelled.\n", "recommendations")
        self.output_console.insert(tk.END, "3. Verify the use of operators and delimiters.\n", "recommendations")

        # Summary of common errors
        self.output_console.insert(tk.END, "-------------------------------------------------------------------------------\n", "recommendations")
        self.output_console.insert(tk.END, "Error Summary:\n", "recommendations")
        self.output_console.insert(tk.END, "- Unrecognized characters may indicate typos or unsupported symbols.\n", "recommendations")

        self.output_console.insert(tk.END, "-------------------------------------------------------------------------------\n", "visualization")
        self.output_console.insert(tk.END, "Visualization:\n", "visualization")
        self.output_console.insert(tk.END, "Review the highlighted tokens to identify any issues in the script.\n", "visualization")

        # Clean up the temporary file
        os.remove(temp_code_file_path)

        # Configure tags for colors
        self.configure_output_tags()

    def get_token_description(self, token):
        """Get the description for the token."""
        descriptions = {
            TokenType.KEYWORD: "Shell Keyword",
            TokenType.COMMAND: "Shell Command",
            TokenType.OPERATOR: "Operator",
            TokenType.DELIMITER: "Delimiter",
            TokenType.IDENTIFIER: "Identifier (Variable)",
            TokenType.NUMBER: "Numeric Value",
            TokenType.STRING_LITERAL: "String Literal",
            TokenType.OPTION: "Command Option",
            TokenType.ARGUMENT: "Argument or File",
            TokenType.ERROR: "Unrecognized Character",
            TokenType.WHITESPACE: "Whitespace",
            TokenType.NEWLINE: "Newline",
            TokenType.COMMENT: "Comment",
            TokenType.AND: "Logical AND Operator",
            TokenType.OR: "Logical OR Operator",
            TokenType.EQUALS: "Equality Operator",
            TokenType.NOT_EQUALS: "Inequality Operator",
            TokenType.LESS_OR_EQUAL: "Less Than or Equal Operator",
            TokenType.GREATER_OR_EQUAL: "Greater Than or Equal Operator",
            TokenType.PLUS: "Addition Operator",
            TokenType.MINUS: "Subtraction Operator",
            TokenType.MULTIPLY: "Multiplication Operator",
            TokenType.DIVIDE: "Division Operator",
            TokenType.ASSIGN: "Assignment Operator",
            TokenType.LESS_THAN: "Less Than Operator",
            TokenType.GREATER_THAN: "Greater Than Operator",
            TokenType.NOT: "Logical NOT Operator",
            TokenType.COLON: "Colon Delimiter",
            TokenType.SEPARATOR: "Command Separator",
            TokenType.PIPE: "Pipeline Operator",
            TokenType.APPEND_REDIRECT: "Append Redirection Operator",
            TokenType.VARIABLE: "Shell Variable"
        }
        return descriptions.get(token.token_type, "Unknown token type")

    def configure_output_tags(self):
        """Configure text tags for colored output."""
        self.output_console.tag_configure("header", foreground="blue", font=("Helvetica", 12, "bold"))
        self.output_console.tag_configure("header_white", foreground="white", font=("Helvetica", 12, "bold"))
        self.output_console.tag_configure("header_yellow", foreground="yellow", font=("Helvetica", 12, "bold"))
        self.output_console.tag_configure("border", foreground="yellow")
        self.output_console.tag_configure("line", foreground="white")
        self.output_console.tag_configure("line_red", foreground="red")
        self.output_console.tag_configure("line_cyan", foreground="cyan")
        self.output_console.tag_configure("summary", foreground="darkgreen")
        self.output_console.tag_configure("recommendations", foreground="darkorange")
        self.output_console.tag_configure("visualization", foreground="purple")
        
        # Enhanced coloring for tokens
        self.output_console.tag_configure("keyword", foreground="blue")
        self.output_console.tag_configure("command", foreground="green")
        self.output_console.tag_configure("operator", foreground="orange")
        self.output_console.tag_configure("delimiter", foreground="cyan")
        self.output_console.tag_configure("identifier", foreground="purple")
        self.output_console.tag_configure("number", foreground="darkgreen")
        self.output_console.tag_configure("string_literal", foreground="magenta")
        self.output_console.tag_configure("option", foreground="brown")
        self.output_console.tag_configure("argument", foreground="darkblue")
        self.output_console.tag_configure("error", foreground="red", font=("Helvetica", 10, "bold"))
        self.output_console.tag_configure("whitespace", foreground="lightgrey")
        self.output_console.tag_configure("newline", foreground="grey")
        self.output_console.tag_configure("comment", foreground="grey", font=("Helvetica", 10, "italic"))
        
        # Default tag
        self.output_console.tag_configure("default", foreground="white")
    def clear_code(self):
        self.code_input.delete("1.0", tk.END)
        self.output_console.delete("1.0", tk.END)
        self.update_line_numbers()

    def clear_output(self):
        self.output_console.delete("1.0", tk.END)

    def load_code(self):
        file_path = filedialog.askopenfilename(filetypes=[("Shell Script files", "*.sh"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'r') as file:
                self.code_input.delete("1.0", tk.END)
                self.code_input.insert(tk.END, file.read())
            self.update_line_numbers()

    def save_code(self):
        code = self.code_input.get("1.0", tk.END)
        file_path = filedialog.asksaveasfilename(defaultextension=".sh", filetypes=[("Shell Script files", "*.sh"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(code)

    def open_docs(self):
        pdf_path = os.path.join(os.getcwd(), 'documentation.pdf')
        if os.path.exists(pdf_path):
            if platform.system() == "Windows":
                os.startfile(pdf_path)
            elif platform.system() == "Linux":
                subprocess.Popen(['xdg-open', pdf_path])
            else:
                print(f"Unsupported OS: {platform.system()}")
        else:
            print("Documentation file not found!")

    def zoom_in(self):
        current_font = Font(font=self.output_console.cget("font"))
        new_size = current_font.actual()["size"] + 2
        current_font.config(size=new_size)
        self.output_console.configure(font=current_font)

    def zoom_out(self):
        current_font = Font(font=self.output_console.cget("font"))
        new_size = max(current_font.actual()["size"] - 2, 8)
        current_font.config(size=new_size)
        self.output_console.configure(font=current_font)

    def exit_app(self):
        exit_message = process_text("آیا مطمئن هستید که می‌خواهید خارج شوید؟")
        exit_title = process_text("خروج")
        if messagebox.askokcancel(exit_title, exit_message):
            self.master.destroy()

    def update_line_numbers(self):
        self.line_numbers.config(state='normal')
        self.line_numbers.delete('1.0', tk.END)
        line_count = int(self.code_input.index('end-1c').split('.')[0])
        line_numbers = '\n'.join(f"{i:4d}" for i in range(1, line_count + 1))
        self.line_numbers.insert(tk.END, line_numbers)
        self.line_numbers.config(state='disabled')
        self.line_numbers.see(self.code_input.index(tk.INSERT))

    def change_theme(self, event):
        selected_theme = self.theme_var.get()
        self.master.style.theme_use(selected_theme)

        # Explicitly reset background colors to maintain consistency
        # self.code_input.config(bg='khaki', fg='black')  # Khaki background for code input
        self.output_console.config(bg='#191212', fg='white')  # Black background for output console
