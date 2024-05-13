from google.cloud import translate_v2 as translate

class TranslationService:
    def __init__(self, credentials_file, project_id: str) -> None:
        """
        Initializes a TranslationService instance.

        Args:
            project_id (str): The ID of the Google Cloud project.
        """
        self.client: translate.TranslationServiceClient = translate.TranslationServiceClient()
        self.parent: str = self.client.location_path(project_id, "global")

    def translate_text(self, input_text: str, input_lang: str, output_lang: str) -> str:
        """
        Translates the input text from the source language to the target language.

        Args:
            input_text (str): The text to be translated.
            input_lang (str): The language code of the input text.
            output_lang (str): The language code of the desired translation.

        Returns:
            str: The translated text.
        """
        response = self.client.translate_text(
            parent=self.parent,
            contents=[input_text],
            mime_type="text/plain",
            source_language_code=input_lang,
            target_language_code=output_lang,
        )
        return response.translations[0].translated_text
