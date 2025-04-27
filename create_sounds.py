import numpy as np
import os
from scipy.io import wavfile

# Create sounds directory if it doesn't exist
if not os.path.exists('sounds'):
    os.makedirs('sounds')

def generate_sound(frequency, duration, volume, fade_out=0):
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = np.sin(2 * np.pi * frequency * t) * volume
    # Convert to stereo
    stereo_wave = np.column_stack((wave, wave))
    if fade_out > 0:
        fade_samples = int(fade_out * sample_rate)
        fade = np.linspace(1.0, 0.0, fade_samples)
        stereo_wave[-fade_samples:] *= fade[:, np.newaxis]
    # Convert to 16-bit integer after all processing
    stereo_wave = (stereo_wave * 32767).astype(np.int16)
    return stereo_wave, sample_rate

def generate_level_up():
    sample_rate = 44100
    duration = 0.5
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    # Generate ascending pitch
    frequencies = np.linspace(440, 880, len(t))
    wave = np.sin(2 * np.pi * frequencies * t) * 0.3
    # Convert to stereo
    stereo_wave = np.column_stack((wave, wave))
    # Convert to 16-bit integer after all processing
    stereo_wave = (stereo_wave * 32767).astype(np.int16)
    return stereo_wave, sample_rate

# Generate sounds
brick_hit, rate = generate_sound(880, 0.1, 0.3)
paddle_hit, rate = generate_sound(440, 0.1, 0.3)
game_over, rate = generate_sound(220, 0.5, 0.4, 0.2)
level_up, rate = generate_level_up()

# Save sounds
wavfile.write('sounds/brick_hit.wav', rate, brick_hit)
wavfile.write('sounds/paddle_hit.wav', rate, paddle_hit)
wavfile.write('sounds/game_over.wav', rate, game_over)
wavfile.write('sounds/level_up.wav', rate, level_up)

print("Sound files generated successfully!") 