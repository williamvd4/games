import streamlit as st
import random
import streamlit.components.v1 as components

# --- 1. CONFIG & DATA ---
# Focused exclusively on -s, -es, and -ies spelling rules
GAME_DATA = [
    # Add -s
    ("Desk", "Spell the Plural form", "Desks"),
    ("Cup", "Spell the Plural form", "Cups"),
    ("Pencil", "Spell the Plural form", "Pencils"),
    ("Book", "Spell the Plural form", "Books"),
    ("Lamp", "Spell the Plural form", "Lamps"),
    ("Sticker", "Spell the Plural form", "Stickers"),
    ("Friend", "Spell the Plural form", "Friends"),
    ("Snack", "Spell the Plural form", "Snacks"),
    # Add -es (s, x, ch, sh)
    ("Bus", "Spell the Plural form", "Buses"),
    ("Box", "Spell the Plural form", "Boxes"),
    ("Lunch", "Spell the Plural form", "Lunches"),
    ("Wish", "Spell the Plural form", "Wishes"),
    ("Fox", "Spell the Plural form", "Foxes"),
    ("Church", "Spell the Plural form", "Churches"),
    ("Brush", "Spell the Plural form", "Bushes"),
    ("Beach", "Spell the Plural form", "Beaches"),
    ("Glass", "Spell the Plural form", "Glasses"),
    ("Tax", "Spell the Plural form", "Taxes"),
    ("Dress", "Spell the Plural form", "Dresses"),
    ("Watch", "Spell the Plural form", "Watches"),
    # Add -ies (Consonant + y)
    ("Baby", "Spell the Plural form", "Babies"),
    ("City", "Spell the Plural form", "Cities"),
    ("Candy", "Spell the Plural form", "Candies"),
    ("Puppy", "Spell the Plural form", "Puppies"),
    ("Party", "Spell the Plural form", "Parties"),
    ("Story", "Spell the Plural form", "Stories"),
    ("Family", "Spell the Plural form", "Families"),
    ("Berry", "Spell the Plural form", "Berries"),
    ("Penny", "Spell the Plural form", "Pennies"),
    ("Lady", "Spell the Plural form", "Ladies")
]

def init_game(names_list):
    """Initializes the game state in memory (No Firestore)."""
    st.session_state.students = [
        {"name": n.strip(), "score": 0, "history": []} 
        for n in names_list if n.strip()
    ]
    # Create the pot: words + 5 KABOOM sticks
    st.session_state.pot = GAME_DATA.copy() + (["KABOOM!"] * 5)
    random.shuffle(st.session_state.pot)
    st.session_state.current_student_idx = 0
    st.session_state.current_task = None
    st.session_state.show_answer = False
    st.session_state.game_started = True

# --- 2. STYLES ---
st.set_page_config(page_title="Noun Kaboom", layout="wide")

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
    .shortcut-hint { font-size: 0.8rem; color: #94a3b8; margin-top: 10px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. KEYBOARD SHORTCUTS ENGINE ---
# This component listens for key presses and clicks the corresponding buttons
components.html(
    """
    <script>
    const doc = window.parent.document;
    doc.addEventListener('keydown', function(e) {
        if (e.code === 'Space') {
            e.preventDefault();
            // Try Draw Card first, then Show Answer
            let drawBtn = Array.from(doc.querySelectorAll('button')).find(el => el.innerText.includes('🎲 Draw a Word'));
            let showBtn = Array.from(doc.querySelectorAll('button')).find(el => el.innerText.includes('Show Answer'));
            if (drawBtn) drawBtn.click();
            else if (showBtn) showBtn.click();
        } else if (e.key.toLowerCase() === 'c') {
            let correctBtn = Array.from(doc.querySelectorAll('button')).find(el => el.innerText.includes('✅ Spelled Correctly!'));
            if (correctBtn) correctBtn.click();
        } else if (e.key.toLowerCase() === 'w') {
            let wrongBtn = Array.from(doc.querySelectorAll('button')).find(el => el.innerText.includes('❌ Wrong (Back in pot)'));
            if (wrongBtn) wrongBtn.click();
        }
    });
    </script>
    """,
    height=0,
)

# --- 4. APP LOGIC ---

# Setup Screen
if "game_started" not in st.session_state:
    st.title("💥 Noun Kaboom: Plural Spelling")
    st.subheader("Practicing -s, -es, and -ies")
    names_input = st.text_area("Enter student names (one per line):", height=200)
    if st.button("Start Game", use_container_width=True):
        if names_input:
            init_game(names_input.split("\n"))
            st.rerun()
        else:
            st.error("Please enter at least one name.")

# Game Screen
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
                    # Return their collected words to the pot
                    st.session_state.pot.extend(current_student["history"])
                    random.shuffle(st.session_state.pot)
                    # Reset score
                    current_student["score"] = 0
                    current_student["history"] = []
                    # Next turn
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
                    st.markdown('<div class="shortcut-hint">Press <b>Spacebar</b> to show answer</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="answer-box">{answer}</div>', unsafe_allow_html=True)
                    c1, c2 = st.columns(2)
                    if c1.button("✅ Spelled Correctly!", use_container_width=True):
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
                    st.markdown('<div class="shortcut-hint">Press <b>C</b> for Correct or <b>W</b> for Wrong</div>', unsafe_allow_html=True)
        else:
            if st.button("🎲 Draw a Word", use_container_width=True):
                if not st.session_state.pot:
                    st.balloons()
                    st.success("All words finished!")
                else:
                    # Logic: Cannot get Kaboom if score < 2
                    found_valid_card = False
                    temp_discard = []
                    
                    while not found_valid_card:
                        candidate = st.session_state.pot.pop()
                        
                        if candidate == "KABOOM!" and current_student["score"] < 2:
                            temp_discard.append(candidate)
                            if not st.session_state.pot: # Pot only has KABOOMs left
                                st.session_state.pot = temp_discard
                                random.shuffle(st.session_state.pot)
                                st.warning("Only KABOOMs left, but you are safe! Drawing from reshuffled deck.")
                                candidate = st.session_state.pot.pop()
                                found_valid_card = True
                        else:
                            found_valid_card = True
                            st.session_state.current_task = candidate
                    
                    # Put the discarded KABOOMs back in the pot for later
                    st.session_state.pot.extend(temp_discard)
                    random.shuffle(st.session_state.pot)
                    
                    st.session_state.show_answer = False
                    st.rerun()
            st.markdown('<div class="shortcut-hint">Press <b>Spacebar</b> to draw</div>', unsafe_allow_html=True)

    with col2:
        st.subheader("📊 Scoreboard")
        for i, s in enumerate(students):
            marker = "➡️" if i == idx else " "
            st.write(f"{marker} **{s['name']}**: {s['score']} pts")

    if st.button("🔄 Reset Entire Game"):
        del st.session_state.game_started
        st.rerun()