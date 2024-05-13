import fire
from slides_api import GoogleSlidesAPI
from text_to_speech import TTSWrapper
from translate import TranslationService
from video_editor import create_video

class PresentationProcessor:
    def __init__(self, project_id: str, credentials_file: str = "credentials/google_api_credentials.json",  tts_model_version: str = "2.0.2", tts_device: str = "cuda"):
        """
        Initialize the PresentationProcessor.

        Args:
            project_id (str): The project ID.
            credentials_file (str, optional): The path to the credentials file. Defaults to "credentials/google_api_credentials.json".
            tts_model_version (str, optional): The version of the TTS model. Defaults to "2.0.2".
            tts_device (str, optional): The device to use for TTS. Defaults to "cuda".
        """
        self.slides_api = GoogleSlidesAPI(credentials_file, project_id) 
        self.tts = TTSWrapper(tts_model_version, tts_device)
        self.translator = TranslationService(credentials_file, project_id)

    def run(self, presentation_id: str, target_language: str = "en") -> None:
        """
        Process the entire presentation, translating, generating audio, and compiling a video.

        Args:
            presentation_id (str): The ID of the presentation.
            target_language (str, optional): The target language for translation. Defaults to "en".
        """
        # Extract speaker notes and images
        notes, images = self.slides_api.extract_notes_and_images(presentation_id)

        # Translate notes if target language is not None
        translated_notes = [self.translator.translate_text(note, "en", target_language) for note in notes if note.strip()] if target_language else notes

        # Generate audio from translated notes
        audio_files = [self.tts.process_tts_to_file(note, target_language, f"audio_{i}.wav") for i, note in enumerate(translated_notes) if note.strip()]

        # Create video clips for each slide
        video_files = create_video("video", images, {target_language: audio_files})

        # Output final video paths
        for video_file in video_files:
            print(f"Final video compiled successfully: {video_file}")

if __name__ == '__main__':
    fire.Fire(PresentationProcessor)