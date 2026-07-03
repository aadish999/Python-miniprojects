import os
import re

def parse_markdown_to_html(md_text):
    """
    Parses structural markdown string data into standard HTML elements.
    """
    html_lines = []
    in_list = False

    # Split document by line breaks
    lines = md_text.split('\n')

    for line in lines:
        # 1. Handle Unordered Lists (- or *)
        list_match = re.match(r'^[-\*]\s+(.*)', line)
        if list_match:
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
            content = list_match.group(1)
            # Inline parsing for list items
            content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
            html_lines.append(f"  <li>{content}</li>")
            continue
        else:
            if in_list:
                html_lines.append("</ul>")
                in_list = False

        # Skip blank lines
        if not line.strip():
            continue

        # 2. Handle Headings (### down to #)
        if line.startswith("### "):
            html_lines.append(f"<h3>{line[4:]}</h3>")
            continue
        elif line.startswith("## "):
            html_lines.append(f"<h2>{line[3:]}</h2>")
            continue
        elif line.startswith("# "):
            html_lines.append(f"<h1>{line[2:]}</h1>")
            continue

        # 3. Inline Elements for Paragraphs: Bold (**text**)
        processed_line = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line)

        # Wrap standard remaining text blocks inside paragraph tags
        html_lines.append(f"<p>{processed_line}</p>")

    # Close trailing open list tags if the file ended unexpectedly
    if in_list:
        html_lines.append("</ul>")

    return "\n".join(html_lines)

def convert_file(input_filename, output_filename):
    """
    Orchestrates file reading, compilation, and file output creation.
    """
    if not os.path.exists(input_filename):
        print(f"Error: The input file '{input_filename}' was not found.")
        return

    try:
        with open(input_filename, "r", encoding="utf-8") as f:
            md_content = f.read()

        html_content = parse_markdown_to_html(md_content)

        # Wrap in full HTML document boilerplate structure
        full_html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Compiled Document</title>
    <style>
        body {{ font-family: sans-serif; line-height: 1.6; padding: 20px; max-width: 800px; margin: 0 auto; }}
        h1 {{ border-bottom: 1px solid #ccc; padding-bottom: 10px; }}
        strong {{ color: #d32f2f; }}
    </style>
</head>
<body>
{html_content}
</body>
</html>"""

        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(full_html)

        print(f"Success: Compiled '{input_filename}' into '{output_filename}'")

    except Exception as e:
        print(f"System failed during document conversion: {e}")

if __name__ == "__main__":
    print("Document Compiler: Markdown to HTML Converter")
    print("-" * 50)

    # Automatically set up a sample input markdown file for testing
    sample_md = "test_document.md"
    output_html = "compiled_output.html"

    if not os.path.exists(sample_md):
        print("Creating a temporary sample markdown file...")
        with open(sample_md, "w", encoding="utf-8") as f:
            f.write("# Project Update Report\n\n")
            f.write("## Current Milestones\n")
            f.write("This file was compiled natively from regular text string data.\n\n")
            f.write("### Deliverables Completed:\n")
            f.write("- Developed the underlying **regular expression** compilation engine.\n")
            f.write("- Formatted output streams inside strict structural tags.\n")
            f.write("- Validated line matrix processing routines.\n")
        print(f"Saved: {sample_md}\n")

    # Run the utility process
    convert_file(sample_md, output_html)
    print("-" * 50)
