from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload
import io
import logging
from typing import List, Tuple

class GoogleSlidesAPI:
    def __init__(self, credentials_file: str, project_id: str):
        self.credentials_file = credentials_file
        self.scopes = ['https://www.googleapis.com/auth/presentations.readonly',
                       'https://www.googleapis.com/auth/drive.readonly']
        self.creds = self.get_credentials()
        self.slides_service = build('slides', 'v1', credentials=self.creds)
        self.drive_service = build('drive', 'v3', credentials=self.creds)

    def get_credentials(self) -> service_account.Credentials:
        """Fetch the credentials from the service account file."""
        return service_account.Credentials.from_service_account_file(
            self.credentials_file,
            scopes=self.scopes
        )

    def fetch_presentation(self, presentation_id: str) -> dict:
        """Fetch the presentation from Google Slides API using the presentation ID.

        Args:
            presentation_id (str): The ID of the Google Slides presentation.

        Returns:
            dict: The presentation data as a dictionary.
        """
        logging.info("Fetching presentation...")
        presentation = self.slides_service.presentations().get(presentationId=presentation_id).execute()
        logging.info("Presentation fetched successfully.")
        return presentation

    def extract_notes(self, slide: dict) -> str:
        """Extract speaker notes from a slide.

        Args:
            slide (dict): The slide data as a dictionary.

        Returns:
            str: The extracted speaker notes.
        """
        logging.info("Extracting notes...")
        slide_notes = ""
        if 'notesPage' in slide:
            notes_elements = slide['notesPage']['pageElements']
            for element in notes_elements:
                if 'shape' in element and 'text' in element['shape']:
                    text_elements = element['shape']['text']['textElements']
                    for text_element in text_elements:
                        if 'textRun' in text_element:
                            slide_notes += text_element['textRun']['content']
        logging.info("Notes extracted successfully.")
        return slide_notes

    def download_slide_as_image(self, presentation_id: str, slide_number: int) -> str:
        """Download a slide as an image.

        Args:
            presentation_id (str): The ID of the Google Slides presentation.
            slide_number (int): The number of the slide to download.

        Returns:
            str: The file name of the downloaded slide image.
        """
        slide_image_file_name = f"slide_{slide_number}.png"
        logging.info(f"Downloading slide {slide_number} as image...")
        request = self.drive_service.files().export_media(fileId=presentation_id, mimeType='image/png')
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
        fh.seek(0)
        with open(slide_image_file_name, 'wb') as f:
            f.write(fh.read())
        logging.info("Slide downloaded as image successfully.")
        return slide_image_file_name

    def extract_notes_and_images(self, presentation_id: str) -> Tuple[List[str], List[str]]:
        """Extract speaker notes and download each slide as an image from the presentation.

        Args:
            presentation_id (str): The ID of the Google Slides presentation.

        Returns:
            Tuple[List[str], List[str]]: A tuple containing the extracted speaker notes and the file names of the downloaded slide images.
        """
        logging.info("Extracting notes and images...")
        presentation = self.fetch_presentation(presentation_id)
        notes = []
        images = []

        for i, slide in enumerate(presentation.get('slides', []), start=1):
            notes.append(self.extract_notes(slide))
            images.append(self.download_slide_as_image(presentation_id, i))

        logging.info("Notes and images extracted successfully.")
        return notes, images
