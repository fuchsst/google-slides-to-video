from typing import Dict, List
from moviepy.editor import CompositeAudioClip, ImageClip, concatenate_videoclips, AudioFileClip

def create_video(output_filename: str, slides: List[str], lang_to_wav: Dict[str, List[str]], pause_in_seconds: int = 1) -> str:
    """
    Create a video by combining slides and corresponding audio files.

    Args:
        file_prefix (str): Prefix for the output video file names.
        slides (List[str]): List of paths to slide images.
        lang_to_wav (Dict[str, List[str]]): Dictionary mapping language codes to lists of audio files.
        pause_in_seconds (int, optional): Duration of pause between each slide. Defaults to 1.

    Returns:
        str: Path to the created video file.
    """
    if not lang_to_wav:
        raise ValueError("No languages provided.")
    
    # Create a list to hold all the audio clips for each language
    audio_clips = []
    for _, wav_files in lang_to_wav.items():
        if len(slides) != len(wav_files):
            raise ValueError("Number of slides and wav files should be the same.")
        
        clips = []
        for slide, wav_file in zip(slides, wav_files):
            slide_image = ImageClip(slide)
            audio_clip = AudioFileClip(wav_file)
            video_clip = slide_image.set_audio(audio_clip).set_duration(audio_clip.duration + pause_in_seconds)
            clips.append(video_clip)

        # Concatenate all video clips into one video
        final_clip = concatenate_videoclips(clips)

        # Add the audio of the final clip to the list of audio clips
        audio_clips.append(final_clip.audio)

    # Create a composite audio clip from all the audio clips
    composite_audio = CompositeAudioClip(audio_clips)

    # Set the audio of the first final clip to the composite audio
    final_clip.audio = composite_audio

    # Export the video clip as mp4
    video_file = f"{output_filename}" + (".mp4" if not output_filename.endswith(".mp4") else "")
    final_clip.write_videofile(video_file, codec="libx264")

    return video_file