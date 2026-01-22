import os
from markitdown import MarkItDown

RAW_DOCS_DIR = "data/raw"
MD_DOCS_DIR = "data/md_docs"

os.makedirs(MD_DOCS_DIR, exist_ok=True)

md = MarkItDown()

def convert_all():
    for file in os.listdir(RAW_DOCS_DIR):
        if file.lower().endswith((".pdf", ".docx", ".pptx", ".html")):
            input_path = os.path.join(RAW_DOCS_DIR, file)
            output_file = file.rsplit(".", 1)[0] + ".md"
            output_path = os.path.join(MD_DOCS_DIR, output_file)

            print(f"Converting: {file}")

            result = md.convert(input_path)

            # ✅ safest way (works even if attributes change)
            markdown_text = str(result)

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(markdown_text)

            print(f"Saved: {output_path}")

if __name__ == "__main__":
    convert_all()
