import pygame
import colorsys
import math
import numpy as np
import wave
import struct
import os
import time

# -------------------------------------------------------------
# 1️⃣ CONFIGURACIÓN GENERAL
# -------------------------------------------------------------
pygame.init()
WIDTH, HEIGHT = 1400, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🎹 Piano Visual Natural - HSL System")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Segoe UI", 22, bold=True)

SAMPLE_RATE = 44100
DURATION = 0.8  # segundos por nota
VOLUME = 0.6

notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
A4_FREQ = 440.0  # Hz

S_min = 40
s_min = S_min / 100
D = 20
alpha = (1 / 4) * math.log2(100 / S_min)

# -------------------------------------------------------------
# 2️⃣ FUNCIONES DE COLOR
# -------------------------------------------------------------
def saturation(delta_o):
    return 100 * (2 ** (-alpha * abs(delta_o)))

def delta_L(S):
    s = S / 100
    return D * (math.log2(1/s) / math.log2(1/s_min))

def HSL_to_RGB(H, S, L):
    r, g, b = colorsys.hls_to_rgb(H / 360, L / 100, S / 100)
    return int(r * 255), int(g * 255), int(b * 255)

def color_for(note_index, octave):
    H = (note_index * 30) % 360
    delta_o = octave - 4
    S = saturation(delta_o)
    L = 50 + delta_L(S) if delta_o < 0 else 50 - delta_L(S)
    return H, S, L, HSL_to_RGB(H, S, L)

# -------------------------------------------------------------
# 3️⃣ SÍNTESIS DE SONIDO "PIANO-LIKE"
# -------------------------------------------------------------
def note_frequency(note_index, octave):
    semitones_from_A4 = (octave - 4) * 12 + (note_index - 9)
    freq = A4_FREQ * (2 ** (semitones_from_A4 / 12))
    return round(freq, 2)

def adsr_envelope(t, attack=0.02, decay=0.1, sustain=0.7, release=0.1, total_duration=0.8):
    env = np.zeros_like(t)
    for i, ti in enumerate(t):
        if ti < attack:
            env[i] = ti / attack
        elif ti < attack + decay:
            env[i] = 1 - (1 - sustain) * ((ti - attack) / decay)
        elif ti < total_duration - release:
            env[i] = sustain
        else:
            env[i] = sustain * (1 - (ti - (total_duration - release)) / release)
    return env

def create_piano_wave(freq):
    t = np.linspace(0, DURATION, int(SAMPLE_RATE * DURATION), endpoint=False)
    wave_data = (np.sin(2*np.pi*freq*t) +
                 0.5*np.sin(2*np.pi*freq*2*t) +
                 0.25*np.sin(2*np.pi*freq*3*t) +
                 0.1*np.sin(2*np.pi*freq*4*t))
    wave_data *= adsr_envelope(t)
    wave_data /= np.max(np.abs(wave_data))
    return (wave_data * 32767).astype(np.int16)

def generate_sound(note, octave):
    freq = note_frequency(notes.index(note), octave)
    data = create_piano_wave(freq)
    filename = f"sounds/octave_{octave}/{note}.wav"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with wave.open(filename, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(struct.pack('<' + 'h' * len(data), *data))

# -------------------------------------------------------------
# 4️⃣ EFECTO DE LUZ
# -------------------------------------------------------------
class Glow:
    def __init__(self):
        self.active = False
        self.color = (255, 255, 255)
        self.radius = 0
        self.alpha = 0
        self.pos = (WIDTH // 2 - 100, HEIGHT // 2 - 100)

    def trigger(self, color, position):
        self.active = True
        self.color = color
        self.pos = position
        self.radius = 0
        self.alpha = 255

    def update(self):
        if not self.active:
            return
        self.radius += 35
        self.alpha -= 10
        if self.alpha <= 0:
            self.active = False

    def draw(self):
        if not self.active:
            return
        surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.circle(surface, (*self.color, max(self.alpha, 0)), self.pos, self.radius)
        screen.blit(surface, (0, 0))

def draw_HSL_panel(H, S, L, color):
    panel = pygame.Rect(WIDTH - 260, 0, 260, HEIGHT)
    pygame.draw.rect(screen, (30, 30, 40), panel)
    pygame.draw.rect(screen, (80, 80, 90), panel, 3)
    title = font.render("HSL Monitor", True, (255, 255, 255))
    screen.blit(title, (WIDTH - 230, 30))
    labels = [
        f"Hue: {H:.1f}°",
        f"Saturation: {S:.1f}%",
        f"Lightness: {L:.1f}%",
    ]
    for i, txt in enumerate(labels):
        t = font.render(txt, True, (200, 200, 200))
        screen.blit(t, (WIDTH - 230, 80 + i * 40))
    pygame.draw.rect(screen, color, (WIDTH - 220, 250, 200, 120), border_radius=8)
    ctext = font.render("Color Actual", True, (20, 20, 20))
    screen.blit(ctext, (WIDTH - 210, 380))

# -------------------------------------------------------------
# 5️⃣ PIANO Y MELODÍA
# -------------------------------------------------------------
key_width = 80
def draw_piano(octave):
    for i, note in enumerate(notes):
        x = 80 + i * key_width
        is_black = "#" in note
        rect = pygame.Rect(x, 400, key_width, 250 if not is_black else 150)
        color = (250, 250, 250) if not is_black else (30, 30, 30)
        pygame.draw.rect(screen, color, rect, border_radius=6)
        pygame.draw.rect(screen, (0, 0, 0), rect, 2, border_radius=6)
        if not is_black:
            label = font.render(f"{note}{octave}", True, (0, 0, 0))
            screen.blit(label, (x + 20, 630))

# “Twinkle Twinkle Little Star”
melody_pattern = [
    "C","C","G","G","A","A","G",
    "F","F","E","E","D","D","C"
]

def play_melody(glow, current_octave):
    for note in melody_pattern:
        generate_sound(note, current_octave)
        sound = pygame.mixer.Sound(f"sounds/octave_{current_octave}/{note}.wav")
        H, S, L, rgb = color_for(notes.index(note), current_octave)
        glow.trigger(rgb, (120 + notes.index(note)*key_width, 400))
        sound.play()
        draw_HSL_panel(H, S, L, rgb)
        pygame.display.flip()
        time.sleep(0.6)

# -------------------------------------------------------------
# 6️⃣ LOOP PRINCIPAL
# -------------------------------------------------------------
pygame.mixer.init()
glow = Glow()
current_octave = 4
background_color = (10, 10, 20)
active_color = (0, 0, 0)
H = S = L = 0
running = True

while running:
    screen.fill(background_color)
    glow.draw()
    draw_piano(current_octave)
    draw_HSL_panel(H, S, L, active_color)

    text = font.render(f"Octava actual: {current_octave}", True, (255, 255, 255))
    screen.blit(text, (20, 20))
    info = font.render("⬆⬇ Cambiar octava | M: Reproducir melodía | ESC: salir", True, (180, 180, 180))
    screen.blit(info, (20, 60))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_UP and current_octave < 8:
                current_octave += 1
            elif event.key == pygame.K_DOWN and current_octave > 1:
                current_octave -= 1
            elif event.key == pygame.K_m:
                play_melody(glow, current_octave)
            else:
                key_map = {
                    pygame.K_a: 0, pygame.K_w: 1, pygame.K_s: 2, pygame.K_e: 3,
                    pygame.K_d: 4, pygame.K_f: 5, pygame.K_t: 6, pygame.K_g: 7,
                    pygame.K_y: 8, pygame.K_h: 9, pygame.K_u: 10, pygame.K_j: 11
                }
                if event.key in key_map:
                    note_index = key_map[event.key]
                    note_name = notes[note_index]
                    generate_sound(note_name, current_octave)
                    sound = pygame.mixer.Sound(f"sounds/octave_{current_octave}/{note_name}.wav")
                    H, S, L, rgb = color_for(note_index, current_octave)
                    glow.trigger(rgb, (120 + note_index*key_width, 400))
                    active_color = rgb
                    sound.play()
                    print(f"{note_name}{current_octave}: H={H:.1f}, S={S:.1f}, L={L:.1f}, RGB={rgb}")

    glow.update()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
