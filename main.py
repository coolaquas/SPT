import librosa
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import savemat
import os

# Define input and output paths
audio_dir = './sample'
output_dir = './converted'
os.makedirs(output_dir, exist_ok=True)

def extract_features(audio_path):
    y, sr = librosa.load(audio_path)
    duration = librosa.get_duration(y=y, sr=sr)
    # Features like spectral centroid and rolloff as basis for pitch and irregularity
    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
    return spectral_centroid, sr, duration

def map_features_to_haptic(centroid, sr, duration, resolution=19200, length_mm=101.76):
    # Normalize and map features to specified pitch and irregularity ranges
    norm_centroid = (centroid - np.min(centroid)) / (np.max(centroid) - np.min(centroid))
    pitch = 0.01 + norm_centroid * (94 - 0.01)  # Mapping to 0.01 to 94 cycles/mm
    irregularity = 0.001 + norm_centroid * (3.16 - 0.001)  # Mapping to 0.001 to 3.16 cycles/mm

    # Interpolate to match the resolution of the TPad
    time = np.linspace(0, duration, len(centroid))
    interp_time = np.linspace(0, duration, resolution)
    interp_pitch = np.interp(interp_time, time, pitch)

    return interp_pitch, irregularity

def save_haptic_data(output_path, pitch_data, irregularity_data):
    # Save data to TXT and MAT files for use with MATLAB and TPad
    savemat(output_path + '.mat', {'pitch': pitch_data, 'irregularity': irregularity_data})
    np.savetxt(output_path + '.txt', pitch_data, fmt='%f')

    # Plotting the haptic data
    plt.figure(figsize=(10, 4))
    plt.plot(pitch_data, label='Pitch')
    plt.plot(irregularity_data, label='Irregularity')
    plt.title('Haptic Data Visualization')
    plt.xlabel('Samples')
    plt.ylabel('Pitch (cycles/mm)')
    plt.legend()
    plt.savefig(output_path + '.png')
    plt.close()

# Process each audio file
for filename in os.listdir(audio_dir):
    if filename.endswith('.wav'):
        audio_path = os.path.join(audio_dir, filename)
        output_path = os.path.join(output_dir, filename.replace('.wav', '_haptic'))
        
        centroid, sr, duration = extract_features(audio_path)
        pitch_data, irregularity_data = map_features_to_haptic(centroid, sr, duration)
        save_haptic_data(output_path, pitch_data, irregularity_data)

print("Haptic data processing is complete.")
