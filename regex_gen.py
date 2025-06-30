import re

def generate_regex_pattern(text, target):
    index = text.find(target)
    if index == -1:
        print("❌ Target value not found in the text.")
        return None

    # Extract context around the target
    pre_context = text[max(0, index - 25):index]
    post_context = text[index + len(target):index + len(target) + 25]

    # Clean up whitespace
    pre_context = pre_context.strip()
    post_context = post_context.strip()

    # Escape regex special chars
    pre_escaped = re.escape(pre_context)
    post_escaped = re.escape(post_context)

    # Replace common delimiters/spaces with flexible matchers
    pre_pattern = re.sub(r"\\s+", r"\\s*", pre_escaped)
    post_pattern = re.sub(r"\\s+", r"\\s*", post_escaped)

    # Try smart guess on value type
    if target.isdigit():
        capture_group = r"(\d+)"
    elif re.fullmatch(r"[A-Z]+\d+", target, re.I):
        capture_group = r"([A-Z]+\d+)"
    else:
        capture_group = r"(.+?)"

    pattern = f"{pre_pattern}\\s*{capture_group}\\s*{post_pattern}"

    return pattern

def main():
    print("🔧 Auto Regex Pattern Generator")
    full_text = input("\n📄 Enter full text (e.g., OCR output):\n").strip()
    target_value = input("\n🎯 Enter the exact value to extract:\n").strip()

    pattern = generate_regex_pattern(full_text, target_value)
    if pattern:
        print("\n✅ Generated Regex Pattern:")
        print(pattern)

        # Test it
        match = re.search(pattern, full_text)
        if match:
            print(f"\n🎉 Match found: {match.group(1)}")
        else:
            print("⚠️  Pattern did not match the text.")

if __name__ == "__main__":
    main()
