import numpy as np
import sounddevice as sd
from scipy import signal
import scipy.io.wavfile as wav



def main():
    

    # sine1 = sine_tone(300, 2, 0.6)
    # square_wave1 = square_wave(300, 2, 0.6)
    # sawtooth_wave1 = sawtooth_wave(300, 2, 0.6)

    my_modulator = sawtooth_wave(20,3,)


    my_sound = am_synthesis(500, my_modulator)
    my_sound = fm_synthesis(200, my_sound)
    my_sound = fm_synthesis(100, my_sound)



    my_sound = apply_envelope(my_sound, [1.0, 0.4, 0.7, 1])
    wav.write("audio.wav", 44100, my_sound)



    sd.play(my_sound)
    sd.wait()

def sine_tone(
        frequency: int=440,
        duration: float=1.0,
        amplitude: float=0.5,
        sample_rate: int=44100
    )   -> np.ndarray:
    
        # Calculate the number of samples required
        n_samples = int(duration * sample_rate)

        # Create an array of time points
        time_points = np.linspace(0, duration, n_samples, False)

        # Create the sine wave
        sine = np.sin(2 * np.pi * frequency * time_points)

        # Apply the amplitude and return the tone
        sine *= amplitude
        return sine

def square_wave(
          
    frequency: int=440,
    duration: float=1.0,
    amplitude: float=0.5,
    sample_rate: int=44100
    )   -> np.ndarray:
     
    n_samples = int(duration * sample_rate)

    time_points = np.linspace(0, duration, n_samples, False)

    square_wave = signal.square(2 * np.pi * frequency * time_points)

    square_wave *= amplitude

    return square_wave

def sawtooth_wave(
          
    frequency: int=440,
    duration: float=1.0,
    amplitude: float=0.5,
    sample_rate: int=44100
    )   -> np.ndarray:
     
    n_samples = int(duration * sample_rate)

    time_points = np.linspace(0, duration, n_samples, False)

    sawtooth_wave = signal.sawtooth(2 * np.pi * frequency * time_points)

    sawtooth_wave *= amplitude

    return sawtooth_wave

# def white_noise(
#         duration: float=1.0,
#         amplitude: float=0.5,
#         sample_rate: int=44100
# ) -> np.ndarray:
    
#     n_samples = int(duration * sample_rate)

#     noise = np.random.uniform(-1, 1, n_samples)

#     noise *= amplitude
#     return noise

def apply_envelope(sound: np.array, adsr:list, sample_rate: int=44100) -> np.array:
     
    sound = sound.copy()

    # Calculate the number of samples for each stage 

    attack_samples = int(adsr[0] * sample_rate)
    decay_samples = int(adsr[1] * sample_rate)
    release_samples = int(adsr[3] * sample_rate)
    sustain_samples = len(sound) - (attack_samples + decay_samples + release_samples)

    # Attack

    sound[:attack_samples] *= np.linspace(0, 1, attack_samples)

    # Decay

    sound[attack_samples:attack_samples + decay_samples] *= np.linspace(1, adsr[2], decay_samples)

    # Sustain 

    sound[attack_samples+ decay_samples:attack_samples + decay_samples + sustain_samples] *= adsr[2]

    # Release 

    sound[attack_samples + decay_samples + sustain_samples:] *= np.linspace(adsr[2], 0, release_samples)

    return sound


def am_synthesis(
    carrier_frequency: float,
    modulator_wave: np.array,
    modulation_index: float=0.5,
    amplitude: float=0.5,
    sample_rate: int=44100

    ) -> np.ndarray:

    total_samples = len(modulator_wave)

    time_points = np.arange(total_samples) / sample_rate

    carrier_wave = np.sin(2* np.pi * carrier_frequency * time_points)

    am_wave = (1 + modulation_index * modulator_wave) * carrier_wave

    max_amplitude = np.max(np.abs(am_wave))
    am_wave = amplitude * (am_wave / max_amplitude)

    return am_wave


def fm_synthesis(
          
    carrier_frequency: float,
    modulator_wave: np.array,
    modulation_index: float=3,
    amplitude: float=0.5,
    sample_rate: int=44100    
    
        
    ) -> np.ndarray:
     
    total_samples = len(modulator_wave)

    time_points = np.arange(total_samples) / sample_rate

    fm_wave = np.sin(2* np.pi * carrier_frequency * time_points + modulation_index * modulator_wave)    

    max_amplitude = np.max(np.abs(fm_wave))
    fm_wave = amplitude * (fm_wave / max_amplitude)

    return fm_wave  

if __name__ == "__main__":
    main()

