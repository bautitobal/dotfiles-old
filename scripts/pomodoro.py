#!/usr/bin/env python3
import subprocess
import time
import sys
import os
import select

SOUND = os.path.expanduser("~/dotfiles/sfx/ding.mp3")
TERMINAL = "kitty"  # Cambiar si usás foot, alacritty, etc.

# Función para mostrar menú con Rofi
def rofi_prompt(prompt, options):
    rofi_cmd = ["rofi", "-dmenu", "-p", prompt]
    proc = subprocess.Popen(rofi_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    stdout, _ = proc.communicate("\n".join(options))
    return stdout.strip()

# Función para pedir entradas individuales
def rofi_input(prompt):
    return rofi_prompt(prompt, [""])

# Elección de modo
choice = rofi_prompt("🍅 Elegí un modo", [
    "🍅 Pomodoro (25/5)",
    "⏳ Largo (50/10)",
    "⚙️ Personalizado",
    "❌ Cancelar"
])
if choice in ["Cancelar", ""]:
    sys.exit(0)

# Parámetros por defecto o personalizados
if choice == "🍅 Pomodoro (25/5)":
    work = 25
    rest = 5
elif choice == "⏳ Largo (50/10)":
    work = 50
    rest = 10
elif choice == "⚙️ Personalizado":
    try:
        work = int(rofi_input("Minutos de trabajo"))
        rest = int(rofi_input("Minutos de descanso"))
    except ValueError:
        sys.exit(1)
else:
    sys.exit(1)

# Pedir nombre de la actividad y cantidad de pomodoros
activity = rofi_input("¿Qué vas a hacer?")
if activity.strip() == "":
    activity = "Actividad sin nombre"

try:
    rounds = int(rofi_input("¿Cuántos pomodoros?"))
except ValueError:
    sys.exit(1)

# Script que se ejecutará dentro de la terminal
inner_script = f"""\
#!/usr/bin/env python3
import time, sys, os, select, subprocess

SOUND = "{SOUND}"

def countdown(minutes, label):
    total_seconds = minutes * 60
    paused = False
    print(f"\\033[1;32m🍅 {{label}} iniciado: {{minutes}} minutos\\033[0m")

    while total_seconds > 0:
        if not paused:
            mins, secs = divmod(total_seconds, 60)
            print(f"\\r\\033[1;34m[{{label}}]\\033[0m Tiempo restante: {{mins:02}}:{{secs:02}} (p: pausar, s: saltar, q: salir): ", end="")
            total_seconds -= 1
        else:
            print(f"\\r⏸️  Pausado. Presioná 'p' para continuar, 's' para saltar, o 'q' para salir: ", end="")

        start_time = time.time()
        while time.time() - start_time < 1:
            if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                key = sys.stdin.read(1)
                if key == 'p':
                    paused = not paused
                    print()
                elif key == 's':
                    print("\\n⏩ Fase saltada por el usuario.")
                    return
                elif key == 'q':
                    print("\\n❌ Cancelado por el usuario.")
                    sys.exit(0)
            time.sleep(0.1)

    print(f"\\n🔔 Finalizó {{label}}.")
    subprocess.run(["paplay", SOUND])
    print("Presioná Enter o 'c' para continuar...", end="", flush=True)
    
    # Esperar confirmación para continuar
    while True:
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            key = sys.stdin.read(1)
            if key in ['\\n', 'c']:
                break
        time.sleep(0.1)

print(f"\\n📌 Actividad: {activity}")
print(f"🎯 Total de pomodoros: {rounds}\\n")

for i in range(1, {rounds + 1}):
    print(f"\\n👉 Pomodoro {{i}} de {rounds}")
    countdown({work}, "Trabajo")
    if i != {rounds}:
        countdown({rest}, "Descanso")

print("\\n✅ ¡Pomodoros completados!")
input("Presioná Enter para salir...")
"""

# Guardar y ejecutar el script en la terminal
with open("/tmp/pomodoro_inner.py", "w") as f:
    f.write(inner_script)

subprocess.Popen([TERMINAL, "--class", "Pomodoro", "-e", "python3", "/tmp/pomodoro_inner.py"])
