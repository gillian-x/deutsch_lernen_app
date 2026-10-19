# print("Hello, my listening app is starting!")

import random
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="German Listening Practice",
    page_icon="🍺",
    layout="centered",
)

LESSONS = [
    ("Max", "Servus! Habt ihr noch einen Tisch für zwei?"),
    ("Kellner", "Servus, ja, da hinten ist noch ein Tisch frei."),
    ("Kellner", "Unter dem Kastanienbaum."),
    ("Max", "Super, dann setzen wir uns da hin."),
    ("Kellner", "Hier sind noch zwei Karten."),
    ("Max & Anna", "Danke!"),
    ("Kellner", "So, habt ihr schon gewählt?"),
    ("Kellner", "Was darf ich euch bringen?"),
    ("Max", "Wir hätten gerne eine Maß Bier und eine Maß Radler, bitte."),
    ("Kellner", "Gerne. Ein Bier und ein Radler."),
    ("Kellner", "Und zu essen?"),
    ("Anna", "Für mich bitte eine Portion Obatzda mit einer Breze."),
    ("Max", "Und für mich die Bratwürste mit Sauerkraut, bitte."),
    ("Kellner", "Gerne. Das bringe ich euch gleich."),
    ("Anna", "Vielen Dank!"),
    ("Kellner", "So, hier sind die Getränke."),
    ("Kellner", "Und hier ist das Essen. Guten Appetit!"),
    ("Max", "Dankeschön! Das sieht wirklich gut aus."),
    ("Anna", "Ja, aber wirklich. Prost!"),
    ("Anna", "Auf das schöne Wochenende!"),
    ("Max", "Prost, Anna! Und guten Appetit."),
    ("Kellner", "So, hat alles gepasst?"),
    ("Anna", "Ja, das war sehr lecker, danke!"),
    ("Anna", "Wir würden dann gerne zahlen."),
    ("Kellner", "Jawoll. Zahlen könnt ihr beim Kollegen, vorne an der Kasse."),
    ("Max", "Okay, machen wir."),
    ("Kellner", "Danke euch und ein schönes Wochenende!"),
    ("Max & Anna", "Danke, euch auch! Servus!"),
]


def shuffle_words(sentence):
    words = sentence.split()

    # Ensure the initial arrangement isn't already correct.
    shuffled = words[:]
    while len(words) > 1 and shuffled == words:
        random.shuffle(shuffled)

    return shuffled


def initialize_sentence(index):
    sentence = LESSONS[index][1]
    st.session_state.selected = []
    st.session_state.options = shuffle_words(sentence)
    st.session_state.checked = False
    st.session_state.correct = False
    st.session_state.hint = False


if "index" not in st.session_state:
    st.session_state.index = 0
    st.session_state.completed = set()
    initialize_sentence(0)


def go_to_sentence(new_index):
    st.session_state.index = new_index
    initialize_sentence(new_index)


speaker, sentence = LESSONS[st.session_state.index]
total = len(LESSONS)

st.title("🍺 Im Biergarten")
st.caption("German listening practice · A2–B1")

st.progress(len(st.session_state.completed) / total)
st.write(
    f"Sentence {st.session_state.index + 1} of {total} "
    f"· {len(st.session_state.completed)} completed correctly"
)

st.subheader(f"Speaker: {speaker}")

# Browser speech synthesis: no audio file required.
audio_text = (
    sentence.replace("\\", "\\\\")
    .replace("'", "\\'")
    .replace("\n", " ")
)

components.html(
    f"""
    <div style="font-family: sans-serif;">
      <button id="play"
        style="padding:10px 18px;border-radius:8px;cursor:pointer;">
        ▶ Play German audio
      </button>
      <button id="stop"
        style="padding:10px 18px;border-radius:8px;cursor:pointer;">
        ■ Stop
      </button>
      <br><br>
      <label for="speed">Speech speed: </label>
      <input id="speed" type="range"
        min="0.6" max="1.2" step="0.1" value="0.85">
      <span id="speedValue">0.85×</span>
    </div>
    <script>
      const text = '{audio_text}';
      const speed = document.getElementById('speed');
      speed.addEventListener('input', () => {{
        document.getElementById('speedValue').textContent =
          speed.value + '×';
      }});
      document.getElementById('play').onclick = () => {{
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'de-DE';
        utterance.rate = Number(speed.value);
        window.speechSynthesis.speak(utterance);
      }};
      document.getElementById('stop').onclick = () => {{
        window.speechSynthesis.cancel();
      }};
    </script>
    """,
    height=110,
)

st.divider()
st.subheader("🧩 Build the sentence")
st.write("Listen to the audio, then select the words in the correct order.")

# Display selected words in the answer area.
st.markdown("**Your sentence:**")

if not st.session_state.selected:
    st.info("Your sentence will appear here.")

cols = st.columns(4)

for i, word in enumerate(st.session_state.selected):
    with cols[i % 4]:
        if st.button(
            f"{word} ×",
            key=f"selected_{st.session_state.index}_{i}",
            disabled=st.session_state.checked,
            use_container_width=True,
        ):
            st.session_state.selected.pop(i)
            st.session_state.options.append(word)
            st.rerun()

st.markdown("**Available words:**")
cols = st.columns(4)

for i, word in enumerate(st.session_state.options):
    with cols[i % 4]:
        if st.button(
            word,
            key=f"option_{st.session_state.index}_{i}",
            disabled=st.session_state.checked,
            use_container_width=True,
        ):
            st.session_state.selected.append(word)
            st.session_state.options.pop(i)
            st.rerun()

if not st.session_state.checked:
    if st.button(
        "Check answer",
        type="primary",
        disabled=bool(st.session_state.options),
        use_container_width=True,
    ):
        # Compare punctuation as well as word order.
        answer = " ".join(st.session_state.selected)
        correct = answer == sentence

        st.session_state.checked = True
        st.session_state.correct = correct

        if correct:
            st.session_state.completed.add(st.session_state.index)

        st.rerun()

else:
    if st.session_state.correct:
        st.success("Sehr gut! Your answer is correct.")
    else:
        st.warning("Not quite. Listen again and try once more.")

    if st.session_state.hint:
        st.info(f"Correct sentence: {sentence}")

    if not st.session_state.correct:
        if st.button("Try again", use_container_width=True):
            initialize_sentence(st.session_state.index)
            st.rerun()

    if st.button("Show / hide answer"):
        st.session_state.hint = not st.session_state.hint
        st.rerun()

    if st.button("Next sentence →", type="primary",
                 use_container_width=True):
        go_to_sentence((st.session_state.index + 1) % total)
        st.rerun()

left, right = st.columns(2)

with left:
    if st.button("← Previous", disabled=st.session_state.index == 0):
        go_to_sentence(st.session_state.index - 1)
        st.rerun()

with right:
    if st.button("Reset sentence"):
        initialize_sentence(st.session_state.index)
        st.rerun()
