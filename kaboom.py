import streamlit as st
import random

# Updated word list to include singular and plural possessives based on the lesson
WORD_LIST = [
    # Regular Plurals
    "Desk", "Cup", "Pencil", "Cat", "Book", "Lamp", "Sticker", "Friend", 
    "Game", "Snack", "Rock", "Chair", "Apple", "Shirt", "Pen",
    "Bus", "Box", "Lunch", "Wish", "Fox", "Church", "Brush", 
    "Beach", "Glass", "Bench", "Dish", "Tax", "Dress", "Flash", "Watch",
    # Singular Possessives (One Owner)
    "The bird's nest", "The baby's toy", "The teacher's desk", "The dog's bone",
    "The girl's hat", "The cat's tail", "The student's pencil",
    # Plural Possessives (Many Owners)
    "The birds' tree", "The students' school", "The babies' room", "The dogs' park",
    "The girls' team", "The teachers' lounge", "The cats' food"
]

def init_game(names_list):
    """Initializes the game state."""
    st.session_state.students = [
        {"name": name.strip(), "score": 0, "words": []} 
        for name in names_list if name.strip()
    ]
    # Create the pot: words + 4 KABOOM sticks
    st.session_state.pot = WORD_LIST.copy() + (["KABOOM!"] * 4)
    random.shuffle(st.session_state.pot)
    st.session_state.current_student_idx = 0
    st.session_state.current_word = None
    st.session_state.game_started = True

# UI Styling
st.set_page_config(page_title="Digital Noun Kaboom!", layout="wide")

st.markdown("""
    <style>
    .main-word {
        font-size: 60px !important;
        font-weight: 800;
        text-align: center;
        padding: 40px;
        color: #1e293b;
        background-color: white;
        border-radius: 20px;
        border: 4px solid #e2e8f0;
        margin: 20px 0;
        line-height: 1.2;
    }
    .kaboom-text {
        color: #ef4444 !important;
        animation: blinker 1s linear infinite;
        font-size: 80px !important;
    }
    @keyframes blinker {
        50% { opacity: 0; }
    }
    .sidebar-rule {
        background-color: #f1f5f9;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 10px;
        font-size: 0.9rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar Grammar Guide
with st.sidebar:
    st.header("📖 Grammar Guide")
    st.markdown("""
    <div class="sidebar-rule">
        <b>Singular:</b> Just one (Cat)
    </div>
    <div class="sidebar-rule">
        <b>Plural:</b> More than one (Cats)
    </div>
    <div class="sidebar-rule">
        <b>Singular Possessive:</b> One owner. Add <b>'s</b><br>
        <i>The cat's toy</i>
    </div>
    <div class="sidebar-rule">
        <b>Plural Possessive:</b> Many owners. Add <b>'</b><br>
        <i>The cats' toys</i>
    </div>
    """, unsafe_allow_html=True)

# 1. Setup Phase
if "game_started" not in st.session_state:
    st.title("💥 Noun Kaboom Setup")
    st.write("Welcome! This game now includes Singular and Plural Possessives.")
    names_input = st.text_area("Enter student names (one per line):", height=200)
    if st.button("Start Game", use_container_width=True):
        if names_input:
            init_game(names_input.split("\n"))
            st.rerun()
        else:
            st.error("Please enter at least one name.")

# 2. Game Phase
else:
    students = st.session_state.students
    idx = st.session_state.current_student_idx
    current_student = students[idx]

    st.title(f"🎮 {current_student['name']}'s Turn")

    col1, col2 = st.columns([2, 1])

    with col1:
        # Display Area
        if st.session_state.current_word:
            word = st.session_state.current_word
            is_kaboom = word == "KABOOM!"
            style_class = "main-word kaboom-text" if is_kaboom else "main-word"
            st.markdown(f'<div class="{style_class}">{word}</div>', unsafe_allow_html=True)
            
            if is_kaboom:
                st.error("OH NO! KABOOM!")
                if st.button("Reset Score & Next Turn", use_container_width=True):
                    # Return words to pot
                    st.session_state.pot.extend(current_student["words"])
                    random.shuffle(st.session_state.pot)
                    # Reset student
                    current_student["score"] = 0
                    current_student["words"] = []
                    # Progress turn
                    st.session_state.current_word = None
                    st.session_state.current_student_idx = (idx + 1) % len(students)
                    st.rerun()
            else:
                st.info("Student: Identify if this is Singular, Plural, Singular Possessive, or Plural Possessive!")
                c1, c2 = st.columns(2)
                if c1.button("✅ Correct!", use_container_width=True):
                    current_student["score"] += 1
                    current_student["words"].append(word)
                    st.session_state.current_word = None
                    st.session_state.current_student_idx = (idx + 1) % len(students)
                    st.rerun()
                
                if c2.button("❌ Try Again", use_container_width=True):
                    # Put word back in pot
                    st.session_state.pot.append(word)
                    random.shuffle(st.session_state.pot)
                    st.session_state.current_word = None
                    st.session_state.current_student_idx = (idx + 1) % len(students)
                    st.rerun()
        else:
            if st.button("🎲 Draw Card", use_container_width=True):
                if not st.session_state.pot:
                    st.session_state.pot = WORD_LIST.copy() + (["KABOOM!"] * 4)
                    random.shuffle(st.session_state.pot)
                st.session_state.current_word = st.session_state.pot.pop()
                st.rerun()

    with col2:
        st.subheader("🏆 Leaderboard")
        for i, s in enumerate(students):
            active_marker = "➡️" if i == idx else ""
            with st.expander(f"{active_marker} {s['name']}: {s['score']} points", expanded=(i == idx)):
                st.write(f"**Collected:** {', '.join(s['words']) if s['words'] else 'None'}")

    if st.button("⚙️ Reset Entire Game", type="secondary"):
        del st.session_state.game_started
        st.rerun()
