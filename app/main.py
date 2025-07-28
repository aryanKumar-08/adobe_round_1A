import fitz
import json
import os

def extract_headings(pdf_path):
    doc = fitz.open(pdf_path)
    font_sizes = {}
    headings = []
    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        size = span["size"]
                        text = span["text"].strip()
                        if text:
                            font_sizes[size] = font_sizes.get(size, 0) + 1
                            headings.append((size, text, page_num))
    sorted_sizes = sorted(font_sizes.keys(), reverse=True)
    title_size = sorted_sizes[0] if sorted_sizes else 0
    h1_size = sorted_sizes[1] if len(sorted_sizes) > 1 else title_size
    h2_size = sorted_sizes[2] if len(sorted_sizes) > 2 else h1_size
    h3_size = sorted_sizes[3] if len(sorted_sizes) > 3 else h2_size

    output = {"title": "", "outline": []}
    for size, text, page_num in headings:
        if size == title_size and output["title"] == "":
            output["title"] = text
        elif size == h1_size:
            output["outline"].append({"level": "H1", "text": text, "page": page_num})
        elif size == h2_size:
            output["outline"].append({"level": "H2", "text": text, "page": page_num})
        elif size == h3_size:
            output["outline"].append({"level": "H3", "text": text, "page": page_num})
    return output

if __name__ == "__main__":
    input_dir = "/app/input"
    output_dir = "/app/output"
    for file in os.listdir(input_dir):
        if file.endswith(".pdf"):
            pdf_path = os.path.join(input_dir, file)
            result = extract_headings(pdf_path)
            out_file = os.path.join(output_dir, file.replace(".pdf", ".json"))
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
