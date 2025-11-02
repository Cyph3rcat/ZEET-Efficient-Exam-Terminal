# Typewriter effect with spinning ball animation
import sys
import time
import threading
import os
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn
import math
import time
import sys
import itertools

# Initialize a Rich console for use in animation functions
console = Console()

zeetASCII = r"""
  ______     ______     ______     ______   
/\___  \   /\  ___\   /\  ___\   /\__  _\ 
\/_/  /__  \ \  __\   \ \  __\   \/_/\ \/ 
  /\_____\  \ \_____\  \ \_____\    \ \_\ 
 \/_____/   \/_____/   \/_____/     \/_/ 
 -----------------------------------------
    ...             /////////////////////////////                          
  
"""
CYAN = "\033[96m"  # Light cyan/teal
RESET = "\033[0m"
ORANGE = "\033[38;5;208m"

# Boot animation using Rich 
def boot_sequence(duration, user):
    console.clear()
    console.rule("[bold cyan]BOOTING ZEET")
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TimeElapsedColumn(),
        transient=True,
        console=console,
    ) as prog:
        task = prog.add_task("[green]Initializing modules...", total=100)
        t0 = time.time()
        while not prog.finished:
            prog.advance(task, 6)
            time.sleep(0.06)
            if time.time() - t0 > duration:
                prog.update(task, completed=100)
                break
    console.print(f"[bold green]ZEET acessed. Welcome, {user}. ")
    time.sleep(1)
    console.clear()

def splash_screen(type_text,
                  wave_amplitude=3, wave_speed=3, wave_delay=0.05,
                  type_delay=0.04, spinner_delay=0.08):
    """
    Runs an animated splash: wave_ascii above, typewriter+spinner below,
    and a 'Press [ENTER] to start' prompt. Stops when Enter is pressed.
    """
    # Shared state
    state = {
        "typed": [],            # list of chars typed so far
        "spinner": " ",         # current spinner char
        "typing_done": False
    }
    lock = threading.Lock()
    stop_event = threading.Event()

    ascii_lines = zeetASCII.strip("\n").splitlines()

    # Typewriter thread: gradually append chars to state['typed']
    def typewriter_thread_fn():
        try:
            for ch in type_text:
                with lock:
                    state["typed"].append(ch)
                time.sleep(type_delay)
        finally:
            with lock:
                state["typing_done"] = True

    # Spinner thread: updates spinner char independently
    spinner_chars = ['⠋','⠙','⠹','⠸','⠼','⠴','⠦','⠧','⠇','⠏']
    def spinner_thread_fn():
        for ch in itertools.cycle(spinner_chars):
            if stop_event.is_set():
                break
            with lock:
                state["spinner"] = ch
            time.sleep(spinner_delay)
        # clear spinner on exit
        with lock:
            state["spinner"] = " "

    # Render thread: draw full frame (wave + typed line + prompt)
    def render_thread_fn():
        # initial full clear
        sys.stdout.write("\033[2J")  # clear entire screen
        sys.stdout.flush()
        t0 = time.perf_counter()
        frame = 0
        last_fps_t = t0
        frame_count = 0
        show_fps = False  # flip to True to debug framerate

        while not stop_event.is_set():
            # home cursor
            sys.stdout.write("\033[H")
            now = time.perf_counter() - t0

            # draw wave ascii
            cols = 80
            try:
                cols = os.get_terminal_size().columns
            except Exception:
                pass

            # We'll compute a float-phase and convert to an integer column offset.
            # Using sin(...) * amplitude gives -amplitude..+amplitude, so we add a baseline.
            for i, line in enumerate(ascii_lines):
                phase = wave_speed * now + i * 0.6
                # continuous offset (can be negative); then shift so we don't go left of column 0
                float_offset = math.sin(phase) * wave_amplitude
                offset = int(round(float_offset + wave_amplitude))  # map to 0..(2*amplitude)
                # clip to terminal width (avoid overflow)
                max_offset = max(0, cols - len(line) - 1)
                offset = max(0, min(offset, max_offset))
                sys.stdout.write(CYAN + " " * offset + line + RESET + "\n")

            # spacer
            sys.stdout.write("\n")

            # typed line + spinner (read under lock)
            with lock:
                current = "".join(state["typed"])
                spinner_ch = state["spinner"]

            line_to_print = f"{ORANGE}{current}{RESET} {CYAN}{spinner_ch}{RESET}"
            padding = max(0, cols - len(current) - 3)
            sys.stdout.write(line_to_print + " " * padding + "\n")

            # prompt line
            prompt = "[ENTER] to start"
            sys.stdout.write(f"\n{prompt}\n")

            # optional tiny FPS debug
            frame_count += 1
            if show_fps:
                now_t = time.perf_counter()
                if now_t - last_fps_t >= 0.5:
                    fps = frame_count / (now_t - last_fps_t)
                    sys.stdout.write(f"FPS: {fps:.1f}\n")
                    last_fps_t = now_t
                    frame_count = 0
                else:
                    sys.stdout.write("\n")

            sys.stdout.flush()
            # Respect the desired frame delay (sleep)
            time.sleep(max(0, wave_delay))
            frame += 1

    # start threads
    t_type = threading.Thread(target=typewriter_thread_fn, daemon=True)
    t_spin = threading.Thread(target=spinner_thread_fn, daemon=True)
    t_render = threading.Thread(target=render_thread_fn, daemon=True)

    t_type.start()
    t_spin.start()
    t_render.start()

    # block until Enter pressed; while blocking, animation continues in threads
    try:
        input()  # "Press Enter" - the prompt is already printed by render loop
    except KeyboardInterrupt:
        pass
    # signal threads to stop and join
    stop_event.set()
    t_type.join(timeout=0.5)
    t_spin.join(timeout=0.5)
    t_render.join(timeout=0.5)

    # final clear of splash (optional)
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()

# # run this file only to view animation
# splash_screen("ZEET//Efficient Exam Terminal")
