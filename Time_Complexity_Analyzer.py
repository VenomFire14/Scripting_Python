import ast
import sys

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


def analyze_file(filepath):
    with open(filepath, "r") as file:
        code = file.read()

    tree = ast.parse(code)
    analyzer = ComplexityAnalyzer()
    analyzer.visit(tree)

    print("\n===== COMPLEXITY REPORT =====\n")

    print("Estimated Time Complexity:")
    print(estimate_time_complexity(analyzer))

    print("\nEstimated Space Complexity:")
    print(estimate_space_complexity(analyzer))

    print("\nHigh Complexity Areas:")
    if analyzer.high_complexity_lines:
        for line, message in analyzer.high_complexity_lines:
            print(f"Line {line}: {message}")
    else:
        print("No major complexity issues detected.")

    print("\nSuggestions:")
    if analyzer.max_loop_depth >= 2:
        print("- Try reducing nested loops using hashing or sets.")
    if analyzer.recursive_calls >= 1:
        print("- Consider memoization or dynamic programming.")
    if analyzer.space_usage > 0:
        print("- Use generators instead of large lists if possible.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python complexity_analyzer.py <python_file.py>")
    else:
        analyze_file(sys.argv[1])