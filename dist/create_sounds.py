import numpy as np
from scipy.io import wavfile

def create_beep(freq, duration, volume=0.5, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration))
    wave = np.sin(2 * np.pi * freq * t) * volume
    return (wave * 32767).astype(np.int16)

# 다양한 효과음 생성
sounds = {
    'paddle_hit.wav': (400, 0.1),  # 낮은 주파수, 짧은 지속시간
    'brick_hit.wav': (800, 0.1),   # 중간 주파수, 짧은 지속시간
    'powerup.wav': (1200, 0.2),    # 높은 주파수, 중간 지속시간
    'game_over.wav': (200, 0.5),   # 매우 낮은 주파수, 긴 지속시간
    'level_up.wav': (600, 0.3),    # 중간 주파수, 중간 지속시간
}

# 사운드 파일 생성
for filename, (freq, duration) in sounds.items():
    wave = create_beep(freq, duration)
    wavfile.write(f'sounds/{filename}', 44100, wave) 