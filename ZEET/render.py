from __future__ import annotations  # for forward type references
from prompt_toolkit import Application
from prompt_toolkit.layout import Layout, HSplit, VSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.widgets import TextArea, Frame
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style
from prompt_toolkit.shortcuts import input_dialog, message_dialog

from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn
import soundsfn

def menu_render(menu, selected):
    lines = []
    lines.append(("class:title", "  ZEET — Zuper Efficient Exam Terminal\n\n"))
    for i, it in enumerate(menu):
        if i == selected:
            lines.append(("class:selected", f" → {it}\n"))
        else:
            lines.append(("class:menu", f"   {it}\n"))
    lines.append(("", "\n  Use ↑ ↓ and Enter. Toggle sound with 's'."))
    return lines


def start_menu(menu, styleMenu, SETTINGS, toggle_sound, selected_ref):
    # selected_ref should be a one-element list, e.g. [0]
    menu_control = FormattedTextControl(lambda: menu_render(menu, selected_ref[0]))
    menu_window = Window(menu_control, height=10)
    body = TextArea(text="Press Enter to choose, 's' toggles sound.", height=6)
    status = FormattedTextControl(lambda: [("class:cmd", f" sound: {'ON' if SETTINGS['sound'] else 'OFF'}  |  Commands: ::quit ::mark ::explain ::<n> ")])
    status_win = Window(status, height=1)

    kb = KeyBindings()

    @kb.add("up")
    def _up(event):
        selected_ref[0] = (selected_ref[0] - 1) % len(menu)
        soundsfn.play("SWITCH")
        event.app.invalidate()

    @kb.add("down")
    def _down(event):
        selected_ref[0] = (selected_ref[0] + 1) % len(menu)
        soundsfn.play("SWITCH")
        event.app.invalidate()

    @kb.add("s")
    def _s(event):
        toggle_sound()
        event.app.invalidate()

    @kb.add("enter")
    def _enter(event):
        soundsfn.play("BUTTON")
        event.app.exit(result=menu[selected_ref[0]])

    root = HSplit([Frame(menu_window), Frame(body), status_win])
    app = Application(layout=Layout(root), key_bindings=kb, style=styleMenu, full_screen=True)
    return app.run()

# ---------- Carousel interactive mode ----------
def progress_text(sess): #the sess should be equivalent to Session
    cur = sess.current_index + 1
    total = len(sess.questions)
    return f"Question {cur}/{total}  |  {int((cur/total)*100)}%"

def render_question_text(q): #q should be equivalent to QuestionState
    out = []
    out.append(f"Q{q.id} [{q.type}]  (Points: {q.points})\n\n")
    out.append(q.stem + "\n\n")
    if q.type == "mcq" and q.options:
        for i, o in enumerate(q.options):
            sel = "(x)" if q.user_response is not None and str(q.user_response) == str(i) else "( )"
            out.append(f" {i}. {sel} {o}\n")
    if q.user_response:
        out.append(f"\nYour answer: {q.user_response}\n")
    return "".join(out)

def auto_grade(q) -> float:
    if q.type == "mcq":
        try:
            if q.user_response is None:
                return 0.0
            return float(q.points) if str(q.user_response) == str(q.answer) else 0.0
        except Exception:
            return 0.0
    elif q.type in ("short", "essay"):
        if not q.user_response or not q.answer:
            return 0.0
        ans_tokens = set(str(q.answer).lower().split())
        usr = set(str(q.user_response).lower().split())
        if not ans_tokens:
            return 0.0
        overlap = len(ans_tokens & usr)
        return round(q.points * (overlap / max(1, len(ans_tokens))), 2)
    return 0.0

def interactive_carousel(sess):
    q_area = TextArea(text="", height=15, scrollbar=True)
    status = FormattedTextControl(lambda: [("class:cmd", progress_text(sess))])
    status_win = Window(status, height=1)
    cmd = TextArea(prompt=":: ", height=1, multiline=False)

    def show_q():
        q_area.text = render_question_text(sess.questions[sess.current_index])

    def handle_cmd(buff):
        text = cmd.text.strip()
        cmd.text = ""
        if not text:
            return
        if text == "::quit":
            path = sess.save()
            soundsfn.play("GRADE")
            message_dialog(title="Saved", text=f"Session saved to {path}").run()
            raise SystemExit("Quitting (saved).")
        if text.startswith("::"):
            tkn = text[2:].split()
            head = tkn[0] if tkn else ""
            if head.isdigit():
                idx = int(head) - 1
                if 0 <= idx < len(sess.questions):
                    sess.current_index = idx
                    show_q()
            elif head == "mark":
                if "-a" in tkn:
                    for qq in sess.questions:
                        qq.score = auto_grade(qq)
                    soundsfn.play("GRADE")
                    message_dialog(title="Marked", text="All questions auto-graded").run()
                else:
                    q = sess.questions[sess.current_index]
                    q.score = auto_grade(q)
                    soundsfn.play("GRADE")
                    message_dialog(title="Marked", text=f"Q{q.id} -> {q.score}/{q.points}").run()
            elif head == "explain":
                q = sess.questions[sess.current_index]
                message_dialog(title=f"Explain Q{q.id}", text=f"Answer: {q.answer}\n\n(Placeholder explanation; hook LLM here)").run()
            else:
                message_dialog(title="Unknown", text=f"Unknown command: {text}").run()
            return
        # otherwise treat as answer
        q = sess.questions[sess.current_index]
        q.user_response = text
        message_dialog(title="Saved answer", text=f"Recorded for Q{q.id}").run()
        show_q()

    cmd.accept_handler = lambda buff: handle_cmd(buff)

    kb = KeyBindings()

    @kb.add("left")
    def _left(event):
        if sess.current_index > 0:
            sess.current_index -= 1
            soundsfn.play("SWITCH")
            show_q()

    @kb.add("right")
    def _right(event):
        if sess.current_index < len(sess.questions) - 1:
            sess.current_index += 1
            soundsfn.play("SWITCH")
            show_q()

    @kb.add("enter")
    def _enter(event):
        # focus command box for typing answer
        event.app.layout.focus(cmd)
        soundsfn.play("BUTTON")

    root = HSplit([Frame(Window(FormattedTextControl(lambda: [("class:title", f"  Interactive — {sess.title}")]), height=1)),
                   Frame(q_area, title="Question"),
                   status_win,
                   cmd])
    app = Application(layout=Layout(root), key_bindings=kb, full_screen=True, style=Style.from_dict({
        "title": "#00ffff bold",
        "cmd": "bg:#222222 #cccccc",
    }))
    show_q()
    app.run()