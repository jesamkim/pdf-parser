"""
Example usage of PDF to Markdown converter
"""
from src.pdf_to_markdown import PDFToMarkdownConverter

def main():
    # Example 1: Basic usage
    print("Example 1: Basic PDF to Markdown conversion")
    converter = PDFToMarkdownConverter()

    # Convert entire PDF
    result = converter.convert_pdf_to_markdown(
        pdf_path="pdf/sample.pdf",
        output_path="output/sample.md"
    )
    print(f"Result: {result}")

    # Example 2: Convert specific pages
    print("\nExample 2: Convert pages 1-5 only")
    result = converter.convert_pdf_to_markdown(
        pdf_path="pdf/sample.pdf",
        output_path="output/sample_pages_1-5.md",
        first_page=1,
        last_page=5
    )
    print(f"Result: {result}")

    # Example 3: Use Haiku model (faster, cheaper)
    print("\nExample 3: Use Haiku model")
    converter_haiku = PDFToMarkdownConverter(
        model_id="global.anthropic.claude-haiku-4-5-20251001-v1:0"
    )
    result = converter_haiku.convert_pdf_to_markdown(
        pdf_path="pdf/sample.pdf",
        output_path="output/sample_haiku.md"
    )
    print(f"Result: {result}")

    # Example 4: High resolution conversion
    print("\nExample 4: High resolution (600 DPI)")
    result = converter.convert_pdf_to_markdown(
        pdf_path="pdf/sample.pdf",
        output_path="output/sample_high_res.md",
        dpi=600
    )
    print(f"Result: {result}")

if __name__ == "__main__":
    main()
