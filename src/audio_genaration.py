
from gtts import gTTS
import os
import cv2
import pytesseract
from PyPDF2 import PdfReader
from docx import Document
import io
import base64
import langid
from pydub import AudioSegment

from io import BytesIO

class audioprocess:

    @staticmethod
    def extract_text_from_image(scanned_image):
        gray_image = cv2.cvtColor(scanned_image, cv2.COLOR_RGB2GRAY)
        text = pytesseract.image_to_string(gray_image)
        print("Extracted Text from Image:")
        return text

    @staticmethod
    def extract_text_from_pdf(pdf_path):
        with open(pdf_path, 'rb') as file:
            pdf_reader = PdfReader(file)
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
            return text

    @staticmethod
    def extract_text_from_text_file(text_file_path):
        with open(text_file_path, 'r') as file:
            text = file.read()
            print("Text from Text File:")
            return text

    @staticmethod
    def extract_text_from_word_document(docx_path):
        doc = Document(docx_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + '\n'
        print("Text from Word Document:")
        return text

    @staticmethod
    def text_to_speech(text, language):
        tts = gTTS(text=text, lang=language, slow=False)
        audio_buffer = BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_data = AudioSegment.from_mp3(audio_buffer)
        return audio_data

    @staticmethod
    def detect_language(text):
        try:
            lang, _ = langid.classify(text)
            return lang
        except Exception as e:
            # Handle exceptions, e.g., if langid cannot process the input
            print(f"Error during language detection: {e}")
            return None

    @staticmethod
    def process_file(file_path):
        file_extension = os.path.splitext(file_path)[-1].lower()

        if file_extension == '.pdf':
            text = audioprocess.extract_text_from_pdf(file_path)
        elif file_extension == '.txt':
            text = audioprocess.extract_text_from_text_file(file_path)
        elif file_extension == '.docx':
            text = audioprocess.extract_text_from_word_document(file_path)
        elif file_extension in ['.png', '.jpg', '.jpeg', '.bmp']:
            scanned_image = cv2.imread(file_path)
            scanned_image = cv2.cvtColor(scanned_image, cv2.COLOR_BGR2RGB)
            text = audioprocess.extract_text_from_image(scanned_image)
        else:
            print(f"Unsupported file format: {file_extension} for file {file_path}")
            return None

     # Remove the temporary file
        return text


def main():
    file_path = "312079761-Telugu-Kavithalu.pdf"
    text = audioprocess.process_file(file_path)

    if text:
        target_language =audioprocess.detect_language(text)
        print(target_language)
        audio_data = audioprocess.text_to_speech(text, target_language)

        # Save the audio file temporarily
        


        return "Audio is playing."
    else:
        return "Error processing file."

if __name__ == '__main__':
    main()


        
