import argparse
import whisper
from transformers import pipeline
import json
import datetime
import torch

def process_audio(audio_path):
    """
    Transcribes audio using Whisper and summarizes the transcription using Hugging Face.

    Args:
        audio_path (str): Path to the input WAV audio file.

    Returns:
        dict: A dictionary containing the timestamp and the summary.
    """
    print(f"Loading Whisper model...")
    # Use "cuda" if available, otherwise "cpu"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")
    # Load the base model. Other options: "tiny", "small", "medium", "large"
    model = whisper.load_model("base", device=device)
    print("Whisper model loaded.")

    print(f"Transcribing audio file: {audio_path}...")
    # Transcribe the audio file
    result = model.transcribe(audio_path)
    transcription = result["text"]
    print("Transcription complete.")
    # print(f"Transcription: {transcription}") # Optional: print full transcription

    print("Loading summarization pipeline...")
    # Load a summarization pipeline from Hugging Face Transformers
    # You can specify a model like "facebook/bart-large-cnn" or use the default
    summarizer = pipeline("summarization", device=0 if device == "cuda" else -1) # device=0 for GPU, -1 for CPU
    print("Summarization pipeline loaded.")

    print("Summarizing transcription...")
    # Summarize the transcription
    # Adjust max_length and min_length as needed
    # Handle potentially long transcriptions by chunking or truncating if necessary
    # For simplicity, we'll summarize the whole text here.
    # Note: Default models might have input length limits.
    max_chunk_length = 1024 # Example max length for BART default model
    if len(transcription) > max_chunk_length:
         print(f"Warning: Transcription length ({len(transcription)}) exceeds model's typical max length ({max_chunk_length}). Summarizing truncated text.")
         # Simple truncation - more sophisticated chunking might be needed for very long audio
         transcription_to_summarize = transcription[:max_chunk_length]
    else:
         transcription_to_summarize = transcription

    summary_result = summarizer(transcription_to_summarize, max_length=150, min_length=30, do_sample=False)
    summary = summary_result[0]['summary_text']
    print("Summarization complete.")

    # Get current timestamp
    timestamp = datetime.datetime.now().isoformat()

    # Prepare JSON output
    output_data = {
        "timestamp": timestamp,
        "summary": summary
    }

    return output_data

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transcribe and summarize an audio file.")
    parser.add_argument("audio_file", help="../Recording0002.wav")

    args = parser.parse_args()

    # Check if the file exists (basic check)
    try:
        with open(args.audio_file, 'rb') as f:
            pass # File exists and is readable
    except FileNotFoundError:
        print(f"Error: Input file not found at {args.audio_file}")
        exit(1)
    except IOError:
        print(f"Error: Could not read file at {args.audio_file}")
        exit(1)


    # Process the audio and get the result
    result_json = process_audio(args.audio_file)
    # Print the JSON output
    print("--- Output JSON ---")
    print(json.dumps(result_json, indent=4))