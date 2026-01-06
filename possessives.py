import streamlit as st
import random
import streamlit.components.v1 as components

# --- 1. 5TH GRADE LEVEL DATA ---
# Using more sophisticated nouns, possessive tasks, and "Identify the Mistake" challenges
GAME_DATA = [
    # Plurals (-s, -es, -ies) - Spelling Focus
    ("Galaxy", "Spell the Plural form", "Galaxies"),
    ("Process", "Spell the Plural form", "Processes"),
    ("Evidence", "Spell the Plural form", "Evidences"),
    ("Boundary", "Spell the Plural form", "Boundaries"),
    ("Compass", "Spell the Plural form", "Compasses"),
    ("Ability", "Spell the Plural form", "Abilities"),
    ("Witness", "Spell the Plural form", "Witnesses"),
    ("Strategy", "Spell the Plural form", "Strategies"),
    ("Challenge", "Spell the Plural form", "Challenges"),
    ("Library", "Spell the Plural form", "Libraries"),
    ("Volcano", "Spell the Plural form", "Volcanoes"),
    ("Discovery", "Spell the Plural form", "Discoveries"),
    
    # Singular Possessives - Identification Focus
    ("The scientist's theory", "Identify: Singular or Plural Possessive?", "Singular Possessive"),
    ("The principal's office", "Identify: Singular or Plural Possessive?", "Singular Possessive"),
    ("The astronaut's helmet", "Identify: Singular or Plural Possessive?", "Singular Possessive"),
    ("The author's notebook", "Identify: Singular or Plural Possessive?", "Singular Possessive"),
    ("The athlete's trophy", "Identify: Singular or Plural Possessive?", "Singular Possessive"),
    ("The musician's instrument", "Identify: Singular or Plural Possessive?", "Singular Possessive"),
    
    # Plural Possessives - Identification Focus
    ("The players' uniforms", "Identify: Singular or Plural Possessive?", "Plural Possessive"),
    ("The explorers' map", "Identify: Singular or Plural Possessive?", "Plural Possessive"),
    ("The countries' borders", "Identify: Singular or Plural Possessive?", "Plural Possessive"),
    ("The detectives' clues", "Identify: Singular or Plural Possessive?", "Plural Possessive"),
    ("The engineers' design", "Identify: Singular or Plural Possessive?", "Plural Possessive"),
    ("The students' project", "Identify: Singular or Plural Possessive?", "Plural Possessive"),
    ("The wolves' habitat", "Identify: Singular or Plural Possessive?", "Plural Possessive"),

    # Identify the Mistake - Correction Focus
    ("The two churchs were old.", "Identify the Mistake", "Churches (Add -es)"),
    ("The citys lights were bright.", "Identify the Mistake", "Cities (Change y to i and add -es)"),
    ("All the child's played outside.", "Identify the Mistake", "Children (Irregular plural)"),
    ("Both of the boy's bikes are blue.", "Identify the Mistake", "Boys' (Plural possessive needs ' after s)"),
    ("The butterflys wings are fragile.", "Identify the Mistake", "Butterfly's (Singular possessive needs 's)"),
    ("The heros' received an award.", "Identify the Mistake", "Heroes (Plural of hero is heroes, no apostrophe needed)"),
    ("The librarys' books are new.", "Identify the Mistake", "Library's (Singular possessive) or Libraries' (Plural)"),
    ("Three foxs ran into the woods.", "Identify the Mistake", "Foxes (Add -es)"),
    ("The ladys purse was lost.", "Identify the Mistake", "Lady's (Needs apostrophe for ownership)")
]

def init_game(names_list):
    st.session_state.students = [
        {"name": n.strip(), "score": 0, "history": []} 
        for n in names_list if n.strip()
    ]
    st.session_state.pot = GAME_DATA.copy() + (["KABOOM!"] * 5)
    random.shuffle(st.session_state.pot)
    st.session_state.current_student_idx = 0
    st.session_state.current_task = None
    st.session_state.show_answer = False
    st.session_state.game_started = True

# --- 2. STYLES ---
st.set_page_config(page_title="5th Grade Kaboom", layout="wide")

st.markdown("""
    <style>
    .display-box { 
        background-color: white; 
        border: 4px solid #6366f1; 
        border-radius: 24px; 
        padding: 50px; 
        text-align: center; 
        margin: 20px 0; 
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    .main-text { font-size: 75px !important; font-weight: 800; color: #1e1b4b; }
    .instruction { font-size: 26px !important; color: #4f46e5; margin-bottom: 15px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; }
    .answer-box { 
        font-size: 65px !important; 
        font-weight: 900; 
        color: #059669; 
        background: #ecfdf5; 
        border: 4px solid #10b981; 
        border-radius: 20px; 
        padding: 25px; 
        margin-top: 25px; 
    }
    .kaboom-text { color: #dc2626 !important; font-size: 110px !important; font-weight: 900; animation: pulse 0.5s infinite; }
    @keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.05); } 100% { transform: scale(1); } }
    .shortcut-hint { font-size: 0.9rem; color: #64748b; margin-top: 15px; text-align: center; font-style: italic; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. KEYBOARD ENGINE ---
components.html(
    """
    <script>
    const doc = window.parent.document;
    doc.addEventListener('keydown', function(e) {
        if (e.code === 'Space') {
            e.preventDefault();
            let drawBtn = Array.from(doc.querySelectorAll('button')).find(el => el.innerText.includes('🎲 Draw a Card'));
            let showBtn = Array.from(doc.querySelectorAll('button')).find(el => el.innerText.includes('Show Answer'));
            if (drawBtn) drawBtn.click();
            else if (showBtn) showBtn.click();
        } else if (e.key.toLowerCase() === 'g') {
            let correctBtn = Array.from(doc.querySelectorAll('button')).find(el => el.innerText.includes('✅ Correct!'));
            if (correctBtn) correctBtn.click();
        } else if (e.key.toLowerCase() === 'w') {
            let wrongBtn = Array.from(doc.querySelectorAll('button')).find(el => el.innerText.includes('❌ Wrong'));
            if (wrongBtn) wrongBtn.click();
        }
    });
    </script>
    """,
    height=0,
)

# --- 4. APP LOGIC ---

if "game_started" not in st.session_state:
    st.title("🚀 5th Grade Noun Kaboom")
    st.write("Vocabulary expansion + Possessive mastery.")
    names_input = st.text_area("Enter student names (one per line):", height=150, value="Alex\nJordan\nTaylor\nCharlie")
    if st.button("Initialize Class Game", use_container_width=True):
        init_game(names_input.split("\n"))
        st.rerun()
else:
    students = st.session_state.students
    idx = st.session_state.current_student_idx
    current_student = students[idx]

    st.title(f"👉 Current Turn: {current_student['name']}")

    col1, col2 = st.columns([2, 1])

    with col1:
        if st.session_state.current_task:
            task = st.session_state.current_task
            
            if task == "KABOOM!":
                st.markdown('<div class="display-box"><div class="kaboom-text">💥 KABOOM! 💥</div></div>', unsafe_allow_html=True)
                st.warning("You had at least 2 points, so the Kaboom was active! Scores reset.")
                if st.button("Reset Score & Pass Turn", use_container_width=True):
                    st.session_state.pot.extend(current_student["history"])
                    random.shuffle(st.session_state.pot)
                    current_student["score"] = 0
                    current_student["history"] = []
                    st.session_state.current_task = None
                    st.session_state.current_student_idx = (idx + 1) % len(students)
                    st.rerun()
            else:
                word, instr, answer = task
                st.markdown(f'''
                    <div class="display-box">
                        <div class="instruction">{instr}</div>
                        <div class="main-text">{word}</div>
                    </div>
                ''', unsafe_allow_html=True)
                
                if not st.session_state.show_answer:
                    if st.button("Show Answer", use_container_width=True):
                        st.session_state.show_answer = True
                        st.rerun()
                    st.markdown('<div class="shortcut-hint">[Spacebar] Show Answer</div>', unsafe_allow_html=True)
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
                    if c2.button("❌ Wrong (Back to Pot)", use_container_width=True):
                        st.session_state.pot.append(task)
                        random.shuffle(st.session_state.pot)
                        st.session_state.current_task = None
                        st.session_state.show_answer = False
                        st.session_state.current_student_idx = (idx + 1) % len(students)
                        st.rerun()
                    st.markdown('<div class="shortcut-hint">[C] Correct | [W] Wrong</div>', unsafe_allow_html=True)
        else:
            if st.button("🎲 Draw a Card", use_container_width=True):
                if not st.session_state.pot:
                    st.balloons()
                    st.success("The deck is empty! Great job everyone.")
                else:
                    # KABOOM SAFETY LOGIC
                    found_valid = False
                    temp_hold = []
                    while not found_valid:
                        card = st.session_state.pot.pop()
                        # If Kaboom but score < 2, put it aside and draw again
                        if card == "KABOOM!" and current_student["score"] < 2:
                            temp_hold.append(card)
                            if not st.session_state.pot: # Only Kabooms left
                                st.session_state.pot = temp_hold
                                random.shuffle(st.session_state.pot)
                                card = st.session_state.pot.pop()
                                found_valid = True
                        else:
                            found_valid = True
                    
                    st.session_state.current_task = card
                    st.session_state.pot.extend(temp_hold)
                    random.shuffle(st.session_state.pot)
                    st.session_state.show_answer = False
                    st.rerun()
            st.markdown('<div class="shortcut-hint">[Spacebar] Draw Card</div>', unsafe_allow_html=True)

    with col2:
        st.subheader("🏆 Leaderboard")
        for i, s in enumerate(students):
            prefix = "⭐" if i == idx else "  "
            st.write(f"{prefix} **{s['name']}**: {s['score']} pts")
            if i == idx:
                st.caption(f"Protecting {len(s['history'])} words in pile.")

    if st.sidebar.button("Reset Entire Game"):
        del st.session_state.game_started
        st.rerun()
