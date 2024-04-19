import os
import numpy as np
import soundfile as sf  # Use soundfile for saving audio to WAV format

def haptic_to_audio(texture_map, original_sr, duration):
    # This function attempts to reverse the process to synthesize audio from the haptic texture map
    t = np.linspace(0, duration, int(original_sr * duration))
    # Synthesize tone based on the average of the texture map treated as a frequency
    synthesized_audio = 0.5 * np.sin(2 * np.pi * texture_map.mean() * t)
    return synthesized_audio

# Function to save audio to WAV file
def save_audio_wav(audio, sr, output_path):
    sf.write(output_path, audio, sr)

# Load an example texture map
try:
    haptic_dir = "./converted"
    for filename in os.listdir(haptic_dir):
        if filename.endswith('.txt'):
            haptic_path = os.path.join(haptic_dir, filename)
            output_path = os.path.join(haptic_dir, filename.replace('_haptic.txt', '.wav'))
            example_texture_map = np.loadtxt(haptic_path, delimiter=',')
            # Assuming the original sampling rate and duration are known
            original_sr = 22050  # Example, this should be the sampling rate of the original audio
            duration = 5  # seconds, this should match or approximate the duration of the original audio
            synthesized_audio = haptic_to_audio(example_texture_map, original_sr, duration)
            print(f"Saving synthesized audio to {filename}...")
            save_audio_wav(synthesized_audio, original_sr, output_path)
            print("Audio saved successfully.")
except Exception as e:
    print(f"An error occurred: {e}")
