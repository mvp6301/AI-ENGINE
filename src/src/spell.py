
# Import necessary libraries
from spellchecker import SpellChecker
from language_tool_python import LanguageTool
from PyPDF2 import PdfReader
import cv2
import pytesseract
from docx import Document

# Define a class for grammar checking
class Grammar_checker:
    @staticmethod
    def extract_text_from_image(scanned_image):
        # Convert the scanned image to grayscale
        gray_image = cv2.cvtColor(scanned_image, cv2.COLOR_RGB2GRAY)
        # Use pytesseract to extract text from the grayscale image
        text = pytesseract.image_to_string(gray_image)
        print("Extracted Text from Image:")
        print(text)
        return text

    @staticmethod
    def extract_text_from_pdf(pdf_path):
        # Open the PDF file in binary mode
        with open(pdf_path, 'rb') as file:
            # Create a PdfReader object to read the PDF file
            pdf_reader = PdfReader(file)
            text = ""
            # Iterate through each page of the PDF and extract text
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
            print("Extracted Text from PDF:")
            print(text)
            return text

    @staticmethod
    def extract_text_from_text_file(text_file_path):
        # Open the text file and read its contents
        with open(text_file_path, 'r') as file:
            text = file.read()
            print("Text from Text File:")
            print(text)
            return text

    @staticmethod
    def extract_text_from_word_document(docx_path):
        # Use the python-docx library to read text from a Word document
        doc = Document(docx_path)
        text = ""
        # Iterate through each paragraph in the document and extract text
        for paragraph in doc.paragraphs:
            text += paragraph.text + '\n'
        print("Text from Word Document:")
        print(text)
        return text

    @staticmethod
    def correct_spelling_and_grammar(text):
        # Create instances for SpellChecker and LanguageTool
        spell = SpellChecker()
        tool = LanguageTool('en-US')

        # Correct spelling
        words = text.split()
        corrected_words = [spell.correction(word) for word in words if spell.correction(word) is not None]
        corrected_text = ' '.join(corrected_words)

        # Grammar check
        matches = tool.check(corrected_text)
        if matches:
            for match in matches:
                suggested_word = match.replacements[0] if match.replacements else "<no suggestions>"
                start = match.offset
                end = match.offset + match.errorLength
                corrected_text = corrected_text[:start] + suggested_word + corrected_text[end:]

        return corrected_text

if __name__ == "__main__":
    # Create an instance of the Grammar_checker class
    grammar_checker = Grammar_checker()

    # Specify the text source (PDF in this case)
    text = "summarized_text.pdf"

    # Extract text from the PDF
    extracted_text = grammar_checker.extract_text_from_pdf(text)

    # Display a separator

    # Correct spelling and grammar in the extracted text
    corrected_text = grammar_checker.correct_spelling_and_grammar(extracted_text)

    # Display the corrected text
    print(corrected_text)

