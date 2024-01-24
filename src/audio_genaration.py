
from gtts import gTTS
import fitz
import os
import cv2
import pytesseract
from PyPDF2 import PdfReader
from docx import Document
from playsound import playsound 
import langid
from pydub import AudioSegment
from pydub import AudioSegment

# Specify the path to the ffmpeg executable
ffmpeg_path = '\config\ffmpeg'

# Set the ffmpeg path
AudioSegment.converter = ffmpeg_path



class audioprocess:

    @staticmethod
    def extract_text_from_image(scanned_image):
        gray_image = cv2.cvtColor(scanned_image, cv2.COLOR_RGB2GRAY)
        text = pytesseract.image_to_string(gray_image)
        print("Extracted Text from Image:")
        return text

    @staticmethod
    def extract_text_from_pdf(pdf_path):
        text = ""
        try:
            pdf_document = fitz.open(pdf_path)
            for page_num in range(pdf_document.page_count):
                page = pdf_document[page_num]
                text += page.get_text()
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
        finally:
            if pdf_document:
                pdf_document.close()
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
        try:
            # Create a gTTS object
            tts = gTTS(text=text, lang=language, slow=False)

            # Save the audio file
            audio_file_path = "output_audio.mp3"
            tts.save(audio_file_path)

            # Play the generated audio
            playsound(audio_file_path)

        except Exception as e:
            print(f"Error during text-to-speech conversion: {e}")

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
    file_path = "documents\\test_documents\\A 25.pdf"
    text = audioprocess.process_file(file_path)
   

    if text:
        target_language =audioprocess.detect_language(text)
        print(target_language)
        audioprocess.text_to_speech(text, target_language)

        # Save the audio file temporarily
        


        return "Audio is playing."
    else:
        return "Error processing file."

if __name__ == '__main__':
    main()


        
