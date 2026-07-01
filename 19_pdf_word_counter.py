import collections
import os
import re
from pypdf import PdfReader

def analyze_pdf(pdf_path):
    """
    Reads a PDF file, extracts the text, cleans it, 
    and returns total words and a frequency distribution.
    """
    if not os.path.exists(pdf_path):
        return f"❌ Error: The file '{pdf_path}' was not found.", None

    try:
        print("📖 Opening PDF file stream and parsing text blocks...")
        reader = PdfReader(pdf_path)
        combined_text = ""

        # Loop through every page and extract text blocks
        for page in reader.pages:
            text = page.extract_text()
            if text:
                combined_text += text + " "

        if not combined_text.strip():
            return "⚠️ Warning: The PDF seems to be empty or contains scanned images instead of text.", None

        # Clean string: convert to lower case and isolate alphanumeric strings using regex
        words = re.findall(r'\b[a-z0-9\-]+\b', combined_text.lower())
        
        total_word_count = len(words)
        
        # Filter out extremely common structural words (stop-words) to show real meaning
        stop_words = {'the', 'a', 'and', 'of', 'to', 'in', 'is', 'for', 'that', 'on', 'with', 'as', 'it', 'at', 'by', 'an', 'this', 'you', 'your', 'from'}
        filtered_words = [word for word in words if word not in stop_words and len(word) > 2]

        # Use Counter to calculate most frequent terms
        word_frequencies = collections.Counter(filtered_words)
        
        return total_word_count, word_frequencies.most_common(5)

    except Exception as e:
        return f"❌ System failed to parse PDF document: {e}", None

if __name__ == "__main__":
    print("📊 Welcome to the PDF Diagnostic Text Analyzer 📊")
    print("-" * 50)

    # Automatically creates a dummy PDF for immediate testing if you don't have one handy
    test_pdf = "sample_document.pdf"
    
    if not os.path.exists(test_pdf):
        print("Creating a temporary sample text PDF file for your execution verification...")
        try:
            # We use pypdf to dynamically write out a test document
            from pypdf import PdfWriter
            writer = PdfWriter()
            page = writer.add_blank_page(width=612, height=792)
            # Add some test strings into the metadata stream for scanning
            writer.add_metadata({
                "/Title": "Test System, Automation Analysis Data Engineering Skillset Data Python Python Core"
            })
            with open(test_pdf, "wb") as f:
                writer.write(f)
            print(f"📦 Test target '{test_pdf}' successfully built.\n")
        except Exception:
            pass

    # Prompt user for path or fallback to test sample
    user_input = input("Enter path to a PDF file (or press Enter to use the generated sample):\n➔ ").strip()
    target_path = user_input if user_input else test_pdf

    print("-" * 50)
    total_words, top_keywords = analyze_pdf(target_path)

    if isinstance(total_words, int):
        print(f"✅ Analysis Completed Successfully for: {target_path}")
        print(f"📈 Total Alphanumeric Words Extracted: {total_words}")
        print("\n🔍 Most Common Informative Keywords Found:")
        for rank, (word, count) in enumerate(top_keywords, 1):
            print(f"   {rank}. [{word}] appeared -> {count} times")
    else:
        # Prints out the error message string instead
        print(total_words)
        
    print("-" * 50)
