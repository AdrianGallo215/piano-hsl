# 🎹 Piano Visual Interactivo - Sistema HSL

## 🌈 Descripción

Este proyecto combina **música, color y visualización** en una experiencia interactiva donde **cada nota del piano** genera tanto un **sonido natural tipo piano acústico** como un **destello de color** correspondiente a su **Hue (matiz)**, **Saturación (S)** y **Luminosidad (L)**, basándose en el modelo de correlación HSL diseñado teóricamente.

Además, incluye un **visualizador automático** que interpreta melodías simples (como *Twinkle Twinkle Little Star*) adaptando el color y brillo según la **octava activa** del piano.

---

## 🧠 Fundamento teórico

Cada nota musical se asocia a un **ángulo del círculo cromático (Hue)**, dividiendo los 360° entre las 12 notas de la escala temperada:

```math
H(\text{nota}) = (H_0 + 30° \times \text{índice}(\text{nota})) \mod 360°
```

La **Saturación (S)** y la **Luminosidad (L)** varían según la octava, siguiendo las funciones:

```math
S(\Delta o) = 100 \cdot 2^{-\alpha |\Delta o|}, \quad \alpha = \frac{1}{4}\log_2\left(\frac{100}{S_{\min}}\right)
```

```math
\Delta L(s) = D \cdot \frac{\log_2(1/s)}{\log_2(1/s_{\min})}, \quad s = S/100
```

Parámetros empleados:

```math
S_{\min} = 40, \quad s_{\min} = 0.4, \quad D = 20
```

De esta forma:
- **Octavas graves** → menor saturación, mayor luminosidad.  
- **Octavas agudas** → mayor saturación, menor luminosidad.  

El resultado es una representación visual coherente con la percepción auditiva del sonido.

---

## 🎧 Características

- 🎵 **Sonido realista tipo piano acústico**, generado por síntesis aditiva con envolvente ADSR.  
- 🌈 **Destellos de color dinámicos** que reflejan los valores HSL de cada nota.  
- 🎼 **Melodía automática** (*Twinkle Twinkle Little Star*) que se adapta a la octava activa.  
- 🖱️ **Interfaz gráfica elegante** desarrollada con Pygame.  
- 🧩 **Generación automática** de los archivos `.wav` (no se requieren samples externos).  
- ⚙️ Código limpio, auto-contenido y fácil de modificar.

---

## 🖥️ Requisitos

- Python **3.9 o superior**
- Librerías necesarias:

```bash
pip install pygame numpy
```

---

## 🚀 Ejecución

1. Clona este repositorio o descarga los archivos:
   ```bash
   git clone https://github.com/tuusuario/piano-visual-hsl.git
   cd piano-visual-hsl
   ```
2. Ejecuta el programa:
   ```bash
   python piano_hsl_acoustic.py
   ```

3. ¡Disfruta el show visual y musical! 🌟

---

## 🎹 Controles

| Tecla | Acción |
|-------|--------|
| `A W S E D F T G Y H U J` | Tocar notas (C a B) |
| `⬆️ / ⬇️` | Cambiar octava |
| `M` | Reproducir melodía *Twinkle Twinkle Little Star* |
| `ESC` | Salir |

---

## 🪄 Visualizador automático

Cada nota genera:
- Un **destello radial** del color correspondiente (RGB derivado del HSL).  
- Una actualización del panel lateral con sus valores:
  - 🎨 Hue (°)
  - 💧 Saturación (%)
  - ☀️ Luminosidad (%)

---

## 📦 Estructura del proyecto

```
piano-visual-hsl/
│
├── piano_hsl_acoustic.py      # Código principal del piano visual
├── sounds/                    # Carpeta generada automáticamente con .wav
│   ├── octave_1/
│   ├── octave_2/
│   └── ...
└── README.md
```

---

## 🎨 Ejemplo visual

Al tocar una nota **C4**:
- Se genera un sonido con frecuencia ≈ 261.63 Hz  
- Se ilumina un destello rojo puro `(H=0°, S=100%, L=50%)`  
- En octavas inferiores, la luminosidad aumenta; en superiores, disminuye.

---

## 🔬 Autoría y créditos

Proyecto desarrollado por **Adrián Gallo Mosqueira**,  
como parte del estudio sobre **correlación estructural entre sonido y color** en el modelo HSL.  

Inspirado en la **sinestesia musical** y la teoría perceptual de **Wassily Kandinsky**.

---

## 🧩 Próximas mejoras (roadmap)

- 🎼 Soporte para múltiples melodías (ej. *Für Elise*, *Canon in D*).  
- 🔊 Control de tempo y dinámica.  
- 💡 Integración MIDI real con luces físicas (IoT / RGB LEDs).  
- 🎨 Exportación de visualizaciones en video.  

---

⭐ Si te gustó el proyecto, ¡dale una estrella en GitHub!  
Tu apoyo ayuda a seguir creando más herramientas visual-musicales.
