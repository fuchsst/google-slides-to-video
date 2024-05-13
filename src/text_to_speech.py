import torch
from TTS.api import TTS
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts
from pathlib import Path

class TTSWrapper:
    def __init__(self, output_folder="../output", model_version: str = "2.0.2", device: str = "cuda") -> None:
        """
        Initialize the TTSWrapper class.

        Args:
            model_version (str): The version of the TTS model to use. Default is "2.0.2".
            device (str): The device to run the TTS model on. Default is "cuda".
        """
        self.model_version: str = model_version
        self.device: str = device
        self.model_loaded: bool = False
        self.model: Xtts = None

    def load_local_model(self, this_dir: Path) -> None:
        """
        Load the local TTS model.

        Args:
            this_dir (Path): The directory path where the TTS model is located.
        """
        config: XttsConfig = XttsConfig()
        model_dir: Path = this_dir / 'models' / self.model_version
        config_path: Path = model_dir / 'config.json'
        speaker_file: Path = model_dir / 'speakers_xtts.pth'

        if not speaker_file.exists():
            raise ValueError("No speaker file found")

        config.load_json(str(config_path))
        self.model = Xtts.init_from_config(config)
        self.model.load_checkpoint(config, speaker_file_path=str(speaker_file), checkpoint_dir=str(model_dir))
        self.model_loaded = True
        self.model.to(self.device)

    def process_tts_to_file(self, this_dir: Path, text: str, language: str, output_file: str) -> str:
        """
        Process text-to-speech and save the output to a file.

        Args:
            this_dir (Path): The directory path where the TTS model is located.
            text (str): The input text to convert to speech.
            language (str): The language of the input text.
            output_file (str): The path of the output file to save the generated speech.

        Returns:
            str: The path of the output file.
        """
        if not self.model_loaded:
            self.load_local_model(this_dir)

        self.model.switch_device(self.device)
        self.model.setup_model()

        out = self.model.generate(text, language)
        torch.save(out["wav"], output_file)

        return output_file
