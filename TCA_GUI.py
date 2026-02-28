import ast
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox


# ===============================
# COMPLEXITY ANALYZER CLASS
# ===============================
class ComplexityAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.loop_depth = 0
        self.max_loop_depth = 0
        self.recursive_calls = 0
        self.current_function = None
        self.high_complexity_lines = []
        self.space_usage = 0

    # -------------------------
    # LOOP ANALYSIS
    # -------------------------
    def visit_For(self, node):
        self.loop_depth += 1
        self.max_loop_depth = max(self.max_loop_depth, self.loop_depth)

        if self.loop_depth >= 2:
            self.high_complexity_lines.append(
                (node.lineno, f"Nested loop detected (Depth {self.loop_depth})")
            )

        self.generic_visit(node)
        self.loop_depth -= 1

    def visit_While(self, node):
        self.loop_depth += 1
        self.max_loop_depth = max(self.max_loop_depth, self.loop_depth)

        if self.loop_depth >= 2:
            self.high_complexity_lines.append(
                (node.lineno, f"Nested while loop detected (Depth {self.loop_depth})")
            )

        self.generic_visit(node)
        self.loop_depth -= 1

    # -------------------------
    # FUNCTION & RECURSION
    # -------------------------
    def visit_FunctionDef(self, node):
        self.current_function = node.name
        self.generic_visit(node)
        self.current_function = None

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            if node.func.id == self.current_function:
                self.recursive_calls += 1
                self.high_complexity_lines.append(
                    (node.lineno, "Recursive call detected")
                )
        self.generic_visit(node)

    # -------------------------
    # SPACE ANALYSIS
    # -------------------------
    def visit_List(self, node):
        self.space_usage += 1
        self.generic_visit(node)

    def visit_Dict(self, node):
        self.space_usage += 1
        self.generic_visit(node)


# ===============================
# ESTIMATION FUNCTIONS
# ===============================
def estimate_time_complexity(analyzer):
    if analyzer.recursive_calls >= 2:
        return "O(2^n) (Exponential - multiple recursion)"
    elif analyzer.recursive_calls == 1:
        return "O(n) (Linear recursion)"
    elif analyzer.max_loop_depth == 1:
        return "O(n)"
    elif analyzer.max_loop_depth == 2:
        return "O(n^2)"
    elif analyzer.max_loop_depth >= 3:
        return f"O(n^{analyzer.max_loop_depth})"
    else:
        return "O(1)"


def estimate_space_complexity(analyzer):
    if analyzer.space_usage > 0:
        return "O(n)"
    else:
        return "O(1)"


# ===============================
# GUI APPLICATION
# ===============================
class ComplexityApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Time & Space Complexity Analyzer")
        self.root.geometry("800x600")

        self.file_path = None

        # Title
        title_label = tk.Label(root, text="Python Complexity Analyzer", 
                               font=("Arial", 18, "bold"))
        title_label.pack(pady=10)

        # Select file button
        select_btn = tk.Button(root, text="Select Python File", 
                               command=self.select_file, width=20)
        select_btn.pack(pady=5)

        # Analyze button
        analyze_btn = tk.Button(root, text="Analyze Complexity", 
                                command=self.analyze_code, width=20)
        analyze_btn.pack(pady=5)

        # Output area
        self.output_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, 
                                                     width=90, height=25)
        self.output_area.pack(pady=10)

    def select_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Python Files", "*.py")]
        )
        if file_path:
            self.file_path = file_path
            messagebox.showinfo("File Selected", f"Selected:\n{file_path}")

    def analyze_code(self):
        if not self.file_path:
            messagebox.showerror("Error", "Please select a Python file first.")
            return

        try:
            with open(self.file_path, "r") as file:
                code = file.read()

            tree = ast.parse(code)
            analyzer = ComplexityAnalyzer()
            analyzer.visit(tree)

            time_complexity = estimate_time_complexity(analyzer)
            space_complexity = estimate_space_complexity(analyzer)

            self.output_area.delete(1.0, tk.END)
            self.output_area.insert(tk.END, "===== COMPLEXITY REPORT =====\n\n")
            self.output_area.insert(tk.END, f"Estimated Time Complexity:\n{time_complexity}\n\n")
            self.output_area.insert(tk.END, f"Estimated Space Complexity:\n{space_complexity}\n\n")

            self.output_area.insert(tk.END, "High Complexity Areas:\n")
            if analyzer.high_complexity_lines:
                for line, message in analyzer.high_complexity_lines:
                    self.output_area.insert(tk.END, f"Line {line}: {message}\n")
            else:
                self.output_area.insert(tk.END, "No major complexity issues detected.\n")

            self.output_area.insert(tk.END, "\nSuggestions:\n")
            if analyzer.max_loop_depth >= 2:
                self.output_area.insert(tk.END, "- Reduce nested loops using sets or dictionaries.\n")
            if analyzer.recursive_calls >= 1:
                self.output_area.insert(tk.END, "- Use memoization or dynamic programming.\n")
            if analyzer.space_usage > 0:
                self.output_area.insert(tk.END, "- Use generators instead of large lists.\n")
            if analyzer.max_loop_depth == 0 and analyzer.recursive_calls == 0:
                self.output_area.insert(tk.END, "Code is efficiently structured.\n")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to analyze file:\n{e}")


# ===============================
# MAIN
# ===============================
if __name__ == "__main__":
    root = tk.Tk()
    app = ComplexityApp(root)
    root.mainloop()