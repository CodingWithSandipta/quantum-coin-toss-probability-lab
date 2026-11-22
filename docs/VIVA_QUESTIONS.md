# Viva Voce Examination Questions & Model Answers

**Subject:** Quantum Computing Laboratory & Theory  
**Topic:** Superposition, Quantum Measurement, Hadamard Gate & Probability Distributions  

---

### Q1. What is a qubit and how does it differ from a classical bit?
**Answer:**  
A classical bit is a two-state deterministic system that can exist strictly in state $0$ or $1$. A qubit (quantum bit) is a two-level quantum system represented as a unit vector in a two-dimensional complex Hilbert space ($\mathbb{C}^2$):
$$|\psi\rangle = \alpha |0\rangle + \beta |1\rangle$$
where $\alpha, \beta \in \mathbb{C}$ are probability amplitudes satisfying $|\alpha|^2 + |\beta|^2 = 1$. Unlike a classical bit, a qubit can exist in a continuous linear superposition of both basis states simultaneously until observed.

---

### Q2. What is the mathematical action of the Hadamard gate on $|0\rangle$ and $|1\rangle$?
**Answer:**  
The Hadamard gate ($H$) is a single-qubit unitary operator represented by the matrix:
$$H = \frac{1}{\sqrt{2}} \begin{bmatrix} 1 & 1 \\ 1 & -1 \end{bmatrix}$$
When applied to computational basis states:
- $H|0\rangle = \frac{|0\rangle + |1\rangle}{\sqrt{2}} \equiv |+\rangle$
- $H|1\rangle = \frac{|0\rangle - |1\rangle}{\sqrt{2}} \equiv |-\rangle$  
Both states possess equal measurement probabilities ($P(0) = P(1) = 0.5$), but differ in their relative quantum phase ($0$ vs $\pi$).

---

### Q3. State the Born Rule and explain its significance.
**Answer:**  
Formulated by Max Born in 1926, the Born Rule states that for a quantum state $|\psi\rangle = \sum_i \alpha_i |i\rangle$, the probability $P(i)$ of measuring eigenstate $|i\rangle$ is the squared magnitude of its complex probability amplitude:
$$P(i) = |\alpha_i|^2 = |\langle i | \psi \rangle|^2$$
It connects the abstract complex statevector to observable, real-world measurement outcomes.

---

### Q4. What happens to a qubit immediately after a projective measurement?
**Answer:**  
Measurement is non-unitary and irreversible. It causes the quantum statevector to **collapse** onto the eigenstate corresponding to the observed eigenvalue. For instance, if a qubit in superposition $(|0\rangle + |1\rangle)/\sqrt{2}$ is measured and yields $0$, the post-measurement state becomes strictly $|0\rangle$. Subsequent measurements will return $0$ with 100% probability.

---

### Q5. What is the Bloch Sphere and how are single-qubit states mapped onto it?
**Answer:**  
The Bloch sphere is a geometric representation of the pure state space of a two-level quantum system. Any pure state can be written as:
$$|\psi\rangle = \cos\left(\frac{\theta}{2}\right)|0\rangle + e^{i\phi}\sin\left(\frac{\theta}{2}\right)|1\rangle$$
The state maps to a unit vector $\vec{r} = (x, y, z)$ on the unit sphere via Pauli expectation values:
- $x = \langle X \rangle = \sin\theta \cos\phi$
- $y = \langle Y \rangle = \sin\theta \sin\phi$
- $z = \langle Z \rangle = \cos\theta$  
The North pole represents $|0\rangle$, the South pole represents $|1\rangle$, and points on the equator represent balanced superpositions.

---

### Q6. Does the Pauli-Z gate alter the measurement probability of a qubit initialized to $|0\rangle$? Why?
**Answer:**  
No. The Pauli-Z gate is represented by $\begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix}$. Applying $Z$ to $|0\rangle$ yields $Z|0\rangle = |0\rangle$. The amplitude remains $1$, so $P(0) = |1|^2 = 1.0$. Even when applied to $|1\rangle$, $Z|1\rangle = -|1\rangle$; the probability $P(1) = |-1|^2 = 1.0$ remains unchanged. The Z gate affects the relative phase between components in a superposition, which becomes crucial in interference-based algorithms.

---

### Q7. How does an independent multi-qubit superposition differ from an entangled state?
**Answer:**  
- **Independent Superposition ($H^{\otimes n}|0\dots 0\rangle$):** The composite state is a **separable product state**:
  $$|\psi\rangle = |+\rangle_1 \otimes |+\rangle_2 \otimes \dots \otimes |+\rangle_n$$
  Measuring qubit 1 has zero influence on the outcome of qubit 2.
- **Entangled State (e.g. Bell state $(|00\rangle + |11\rangle)/\sqrt{2}$):** The state cannot be factored into tensor products of individual qubit states. Measuring one qubit instantaneously determines the state of the other, regardless of spatial separation.

---

### Q8. Why don't 1,000 shots on an AerSimulator yield exactly 500 Heads and 500 Tails in a quantum coin toss?
**Answer:**  
Quantum measurement is inherently probabilistic. In any finite sample size ($N$), the number of observed events fluctuates due to **stochastic shot noise**. By the Central Limit Theorem, the standard deviation of the observed probability scales as $\sigma \approx \sqrt{p(1-p)/N} = 0.5/\sqrt{N}$. For $N=1,000$, $\sigma \approx 1.58\%$, meaning observed frequencies typically fall between 48.4% and 51.6%. Exact 500/500 outcomes are possible but not guaranteed.

---

### Q9. What is the difference between a classical PRNG and a quantum computer simulation?
**Answer:**  
- A **classical PRNG** (e.g. Python's Mersenne Twister) uses a deterministic mathematical recurrence relation on integer seeds to produce numbers that appear random.
- A **quantum simulator** (e.g. Qiskit Aer) compiles a quantum circuit and calculates state vectors using unitary matrix multiplication on classical hardware. It then samples measurement counts using pseudorandom algorithms to mimic quantum Born-rule probabilities.
- Neither local simulator nor PRNG produces true physical quantum randomness; true quantum randomness requires physical quantum processors measuring physical quantum states.

---

### Q10. What is the purpose of `transpile` in Qiskit?
**Answer:**  
`transpile` rewrites a high-level `QuantumCircuit` to match the specific basis gates, topology, and coupling constraints of a target quantum backend (or simulator). Even for local simulators, transpilation optimizes gate sequences and reduces depth to ensure efficient execution.
