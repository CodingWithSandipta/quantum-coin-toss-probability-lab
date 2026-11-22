"""
pages/7_Quiz.py - Interactive Quantum Computing Knowledge Quiz
10 Multiple-Choice Questions covering qubits, gates, superposition, and measurement.
"""

import os
import streamlit as st
from components.ui_components import render_header, render_metric_card, render_info_banner

st.set_page_config(
    page_title="Quantum Quiz | Quantum Lab",
    page_icon="🧠",
    layout="wide",
)

# Apply CSS styles
css_path = os.path.join(os.path.dirname(__file__), "..", "assets", "styles.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

render_header(
    title="🧠 Quantum Computing Knowledge Quiz",
    subtitle="Test your comprehension of qubits, superposition, quantum gates, and probability distributions.",
    badge="10 Interactive MCQs",
)

QUIZ_QUESTIONS = [
    {
        "id": 1,
        "question": "What mathematical space does a single qubit statevector occupy?",
        "options": [
            "A one-dimensional real space (R¹)",
            "A two-dimensional complex Hilbert space (C²)",
            "A four-dimensional real vector space (R⁴)",
            "An infinite-dimensional Euclidean space",
        ],
        "answer_idx": 1,
        "explanation": "A qubit is represented as a normalized two-dimensional vector with complex amplitudes: |ψ⟩ = α|0⟩ + β|1⟩ in C².",
    },
    {
        "id": 2,
        "question": "What state results from applying a Hadamard gate (H) to the ground state |0⟩?",
        "options": [
            "|1⟩",
            "(|0⟩ - |1⟩) / √2",
            "(|0⟩ + |1⟩) / √2",
            "|0⟩ with an inverted phase",
        ],
        "answer_idx": 2,
        "explanation": "H|0⟩ creates an equal, in-phase superposition state: (|0⟩ + |1⟩)/√2, often denoted as the |+⟩ state.",
    },
    {
        "id": 3,
        "question": "According to the Born Rule, what is the probability of measuring basis state |0⟩ for state |ψ⟩ = α|0⟩ + β|1⟩?",
        "options": [
            "|α|",
            "|α|²",
            "α + β",
            "|α| / (|α| + |β|)",
        ],
        "answer_idx": 1,
        "explanation": "The Born rule states that the measurement probability is the squared magnitude of the amplitude: P(0) = |α|².",
    },
    {
        "id": 4,
        "question": "What is the normalization condition for the probability amplitudes α and β of a valid qubit?",
        "options": [
            "α + β = 1",
            "|α| + |β| = 1",
            "|α|² + |β|² = 1",
            "α² + β² = 0",
        ],
        "answer_idx": 2,
        "explanation": "Total probability must equal 100%, so the sum of the squared moduli |α|² + |β|² must equal 1.",
    },
    {
        "id": 5,
        "question": "Which quantum gate acts as the quantum equivalent of a classical NOT gate?",
        "options": [
            "Pauli-X Gate",
            "Pauli-Z Gate",
            "Hadamard Gate",
            "Phase S Gate",
        ],
        "answer_idx": 0,
        "explanation": "The Pauli-X gate inverts the computational basis: X|0⟩ = |1⟩ and X|1⟩ = |0⟩.",
    },
    {
        "id": 6,
        "question": "How many orthogonal computational basis states exist for an n-qubit system?",
        "options": [
            "n",
            "2n",
            "n²",
            "2ⁿ",
        ],
        "answer_idx": 3,
        "explanation": "An n-qubit system spans an exponential Hilbert space with 2ⁿ orthogonal basis states.",
    },
    {
        "id": 7,
        "question": "If 3 qubits each have a Hadamard gate applied (H⊗H⊗H|000⟩), what is the ideal theoretical probability for state |101⟩?",
        "options": [
            "12.5% (1/8)",
            "25.0% (1/4)",
            "33.3% (1/3)",
            "50.0% (1/2)",
        ],
        "answer_idx": 0,
        "explanation": "For 3 qubits, there are 2³ = 8 states. The uniform probability is P = 1/2³ = 1/8 = 12.5%.",
    },
    {
        "id": 8,
        "question": "What effect does a projective computational basis measurement have on a superposition state?",
        "options": [
            "It doubles the amplitudes of the system",
            "It irreversibly collapses the superposition into a single definite eigenstate",
            "It leaves the superposition unchanged while recording a reading",
            "It resets the qubit to state |0⟩ deterministically regardless of amplitudes",
        ],
        "answer_idx": 1,
        "explanation": "Measurement destroys quantum superposition, collapsing the wave function into one observed basis state according to Born's rule.",
    },
    {
        "id": 9,
        "question": "What is the primary difference between a classical PRNG and a local quantum simulator (e.g. Qiskit Aer)?",
        "options": [
            "The simulator connects directly to a cryogenic dilution refrigerator",
            "The simulator calculates quantum statevector mathematics and samples from it, rather than computing real quantum hardware collapse",
            "The simulator is physically 10,000x faster than classical pseudorandom algorithms",
            "The simulator always produces exact 50/50 splits without statistical variance",
        ],
        "answer_idx": 1,
        "explanation": "Qiskit Aer is a software simulator executing quantum circuit linear algebra on a classical computer; it models quantum physics without being a physical quantum computer.",
    },
    {
        "id": 10,
        "question": "On the geometric Bloch sphere representation of a single qubit, where does the ground state |0⟩ lie?",
        "options": [
            "At the South Pole (Z = -1)",
            "At the North Pole (Z = +1)",
            "Along the positive X-axis on the equator",
            "At the center of the sphere (origin)",
        ],
        "answer_idx": 1,
        "explanation": "By standard quantum convention, the ground state |0⟩ is situated at the North Pole of the Bloch sphere (θ=0, Z=+1).",
    },
]

st.markdown("Answer all 10 questions below and click **Submit Quiz** to calculate your score and review detailed explanations.")

with st.form("quantum_quiz_form"):
    user_answers = {}
    for q in QUIZ_QUESTIONS:
        st.markdown(f"#### Q{q['id']}. {q['question']}")
        user_choice = st.radio(
            label=f"Options for Q{q['id']}:",
            options=range(4),
            format_func=lambda i, opts=q["options"]: opts[i],
            key=f"quiz_q_{q['id']}",
            index=None,
        )
        user_answers[q["id"]] = user_choice
        st.write("")

    submitted = st.form_submit_button("📝 Submit Quiz Answers", type="primary")

if submitted:
    answered_count = sum(1 for v in user_answers.values() if v is not None)
    if answered_count < len(QUIZ_QUESTIONS):
        render_info_banner(
            f"Please answer all questions before submitting. (Answered {answered_count}/{len(QUIZ_QUESTIONS)})",
            alert_type="warning",
        )
    else:
        score = 0
        st.divider()
        st.subheader("🎯 Quiz Results & Detailed Answer Review")

        for q in QUIZ_QUESTIONS:
            ans = user_answers[q["id"]]
            is_correct = ans == q["answer_idx"]
            if is_correct:
                score += 1

            status_icon = "✅" if is_correct else "❌"
            color_style = "#10b981" if is_correct else "#f43f5e"

            st.markdown(f"**{status_icon} Q{q['id']}: {q['question']}**")
            st.markdown(f"- Your Answer: `{q['options'][ans]}`")
            if not is_correct:
                st.markdown(f"- Correct Answer: <span style='color: #10b981; font-weight: 600;'>{q['options'][q['answer_idx']]}</span>", unsafe_allow_html=True)
            st.markdown(f"- *Explanation:* {q['explanation']}")
            st.write("")

        pct_score = (score / len(QUIZ_QUESTIONS)) * 100
        st.divider()
        c1, c2, c3 = st.columns(3)
        with c1:
            render_metric_card("Final Score", f"{score} / {len(QUIZ_QUESTIONS)}", f"{pct_score:.1f}%")
        with c2:
            rating = "Quantum Master! 🌟" if score >= 9 else ("Proficient Student 👏" if score >= 7 else "Keep Practicing 📚")
            render_metric_card("Proficiency", rating, "Based on answers")
        with c3:
            render_metric_card("Status", "Complete", "10 / 10 Evaluated", delta_color="#10b981")
