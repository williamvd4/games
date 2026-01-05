import streamlit as st
import random

# Data structure: (Display Text, Instruction, Correct Answer/Category)
GAME_DATA = [
    # Regular Plurals: The student must SPELL these
    ("Desk", "Spell the Plural form", "Desks"),
    ("Bus", "Spell the Plural form", "Buses"),
    ("Box", "Spell the Plural form", "Boxes"),
    ("Lunch", "Spell the Plural form", "Lunches"),
    ("Wish", "Spell the Plural form", "Wishes"),
    ("Fox", "Spell the Plural form", "Foxes"),
    ("Church", "Spell the Plural form", "Churches"),
    ("Brush", "Spell the Plural form", "Brushes"),
    ("Beach", "Spell the Plural form", "Beaches"),
    ("Glass", "Spell the Plural form", "Glasses"),
    ("Tax", "Spell the Plural form", "Taxes"),
    ("Dress", "Spell the Plural form", "Dresses"),
    ("Flash", "Spell the Plural form", "Flashes"),
    ("Watch", "Spell the Plural form", "Watches"),
    ("Friend", "Spell the Plural form", "Friends"),
    ("Snack", "Spell the Plural form", "Snacks"),
    
    # Singular Possessives: The student must IDENTIFY these
    ("The bird's nest", "Identify: Singular or Plural Possessive?", "Singular Possessive"),
    ("The baby's toy", "Identify: Singular or Plural Possessive?", "Singular Possessive"),
    ("The teacher's desk", "Identify: Singular or Plural Possessive?", "Singular Possessive"),
    ("The dog's bone", "Identify: Singular or Plural Possessive?", "Singular Possessive"),
    ("The student's pencil", "Identify: Singular or Plural Possessive?", "Singular Possessive"),
    
    # Plural Possessives: The student must IDENTIFY these
    ("The birds' tree", "Identify: Singular or Plural Possessive?", "Plural Possessive"),
    ("The students' school", "Identify: Singular or Plural Possessive?", "Plural Possessive"),
    ("The babies' room", "Identify: Singular or Plural Possessive?", "Plural Possessive"),
    ("The dogs' park", "Identify: Singular or Plural Possessive?", "Plural Possessive"),
    ("The teachers' lounge", "Identify: Singular or Plural Possessive?", "Plural Possessive"),
    ("The cats' food", "Identify: Singular or Plural Possessive?", "Plural Possessive")
]

def init_game(names_list):
    st.session_state.students = [
        {"name": name.strip(), "score": 0, "history": []} 
        for name in names_list if name.strip()
    ]
    # Game "pot" with words and Kaboom sticks
    st.session_state.pot = GAME_DATA.copy() + (["KABOOM!"] * 5)
    random.shuffle(st.session_state.pot)
    st.session_state.current_student_idx = 0
    st.session_state.current_task = None
    st.session_state.show_answer = False
    st.session_state.game_started = True

st.set_page_config(page_title="Noun Kaboom", layout="wide")

# Custom CSS for a clean, large UI
st.markdown("""
    <style>
    .display-box { 
        background-color: white; 
        border: 4px solid #e2e8f0; 
        border-radius: 20px; 
        padding: 40px; 
        text-align: center;
        margin: 20px 0;
    }
    .main-text { font-size: 70px !important; font-weight: 800; color: #1e293b; }
    .instruction { font-size: 28px !important; color: #64748b; margin-bottom: 10px; font-weight: 600; }
    .answer-box { 
        font-size: 60px !important; 
        font-weight: 900; 
        color: #16a34a; 
        background: #f0fdf4; 
        border: 3px solid #bbf7d0; 
        border-radius: 15px; 
        padding: 20px; 
        margin-top: 20px; 
    }
    .kaboom-text { color: #ef4444 !important; font-size: 100px !important; font-weight: 900; animation: blinker 0.8s linear infinite; }
    @keyframes blinker { 50% { opacity: 0; } }
    </style>
    """, unsafe_allow_html=True)

if "game_started" not in st.session_state:
    st.title("💥 Noun Kaboom: Class Edition")
    st.write("Mix of spelling practice and possessive identification.")
    names_input = st.text_area("Enter student names (one per line):", height=200)
    if st.button("Start Game", use_container_width=True):
        if names_input:
            init_game(names_input.split("\n"))
            st.rerun()
else:
    students = st.session_state.students
    idx = st.session_state.current_student_idx
    current_student = students[idx]

    st.title(f"👤 Player: {current_student['name']}")

    col1, col2 = st.columns([2, 1])

    with col1:
        if st.session_state.current_task:
            task = st.session_state.current_task
            
            if task == "KABOOM!":
                st.markdown('<div class="display-box"><div class="kaboom-text">KABOOM! 💥</div></div>', unsafe_allow_html=True)
                if st.button("Return words & Pass Turn", use_container_width=True):
                    st.session_state.pot.extend(current_student["history"])
                    random.shuffle(st.session_state.pot)
                    current_student["score"] = 0
                    current_student["history"] = []
                    st.session_state.current_task = None
                    st.session_state.current_student_idx = (idx + 1) % len(students)
                    st.rerun()
            else:
                display_word, instr, answer = task
                st.markdown(f'''
                    <div class="display-box">
                        <div class="instruction">{instr}</div>
                        <div class="main-text">{display_word}</div>
                    </div>
                ''', unsafe_allow_html=True)
                
                if not st.session_state.show_answer:
                    if st.button("Show Answer", use_container_width=True):
                        st.session_state.show_answer = True
                        st.rerun()
                else:
                    st.markdown(f'<div class="answer-box">{answer}</div>', unsafe_allow_html=True)
                    c1, c2 = st.columns(2)
                    if c1.button("✅ Correct!", use_container_width=True):
                        current_student["score"] += 1
                        current_student["history"].append(task)
                        st.session_state.current_task = None
                        st.session_state.show_answer = False
                        st.session_state.current_student_idx = (idx + 1) % len(students)
                        st.rerun()
                    if c2.button("❌ Wrong (Back in pot)", use_container_width=True):
                        st.session_state.pot.append(task)
                        random.shuffle(st.session_state.pot)
                        st.session_state.current_task = None
                        st.session_state.show_answer = False
                        st.session_state.current_student_idx = (idx + 1) % len(students)
                        st.rerun()
        else:
            if st.button("🎲 Draw a Card", use_container_width=True):
                if not st.session_state.pot:
                    st.balloons()
                    st.success("All cards finished!")
                else:
                    st.session_state.current_task = st.session_state.pot.pop()
                    st.session_state.show_answer = False
                    st.rerun()

    with col2:
        st.subheader("📊 Scoreboard")
        for i, s in enumerate(students):
            marker = "➡️" if i == idx else " "
            st.write(f"{marker} **{s['name']}**: {s['score']} pts")
            if i == idx:
                st.caption(f"Has {len(s['history'])} words in their pile.")

    if st.button("🔄 Reset App"):
        del st.session_state.game_started
        st.rerun()
