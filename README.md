# GoogleSlidesToVideo

GoogleSlidesToVideo is a Python project that converts Google Slides speaker notes into video presentations. It uses various services such as Google Slides API, Google Translate API, and Text-to-Speech (TTS) to generate a video presentation from your Google Slides.

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/GoogleSlidesToVideo.git
    ```

2. Navigate to the project directory:

    ```sh
    cd GoogleSlidesToVideo
    ```

3. Install the required Python packages:

    ```sh
    pip install -r requirements.txt
    ```

4. Install the project:

    ```sh
    python setup.py install
    ```

## Usage

The main entry point of the application is the [`main.py`](main.py) script. You can run it as follows:

```sh
python src/main.py
```

The [`main.py`](main.py) script uses the `fire` library to expose the `PresentationProcessor` class as a command-line interface. You can use it to process a Google Slides presentation into a video.

For example, to process a presentation, you can use the [`process_presentation`](main.py) method:

```sh
python main.py run --project_id=YOUR_PROJECT_ID process_presentation --presentation_id=YOUR_PRESENTATION_ID --target_language=YOUR_TARGET_LANGUAGE
```

Replace `YOUR_PRESENTATION_ID` with the ID of your Google Slides presentation.

Please note that you need to set up your Google API credentials and other environment variables as per your requirements. Refer to the [`app.py`](app.py) script for more details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the terms of the MIT license.