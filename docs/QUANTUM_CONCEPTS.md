# Quantum Computing Concepts & Theoretical Foundations

This document provides a comprehensive educational reference for the **Quantum Coin Toss and Probability Laboratory**. It covers fundamental principles, mathematical formulations, and physical interpretations of quantum mechanics applied to computation.

---

## 1. Classical vs Quantum Computing

### Classical Computation
- **Information Unit:** The classical **bit** exists strictly in one of two states: $0$ (low voltage) or $1$ (high voltage).
- **Determinism:** Given an initial state and deterministic logic gates (AND, OR, NOT), a classical computer follows a singular, predictable trajectory through state space.
- **Randomness:** Classical computers cannot generate true physical randomness algorithmically; they utilize deterministic mathematical formulas known as **Pseudo-Random Number Generators (PRNGs)**, such as the Mersenne Twister ($2^{19937}-1$ period).

### Quantum Computation
- **Information Unit:** The quantum bit or **qubit** is a physical two-level quantum system (such as electron spin or photon polarization).
- **State Space:** Unlike classical bits, qubits can exist in linear combinations of basis states called **superpositions**.
- **Entanglement & Interference:** Multiple qubits can exhibit non-classical correlations (entanglement) and probability amplitude cancellations (destructive interference) that have no classical analog.

---

## 2. Mathematical Definition of a Qubit

A single qubit is represented as a normalized statevector in a two-dimensional complex Hilbert space ($\mathbb{C}^2$):

$$|\psi\rangle = \alpha |0\rangle + \beta |1\rangle = \begin{bmatrix} \alpha \\ \beta \end{bmatrix}$$

where $\alpha, \beta \in \mathbb{C}$ are **probability amplitudes**, and:

$$|0\rangle = \begin{bmatrix} 1 \\ 0 \end{bmatrix}, \quad |1\rangle = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$$

### Normalization Condition
Because the total probability of all mutually exclusive measurement outcomes must equal 1 (100%), the amplitudes must satisfy:

$$\langle \psi | \psi \rangle = |\alpha|^2 + |\beta|^2 = 1$$

---

## 3. Quantum Superposition

Superposition is the physical principle stating that if $|0\rangle$ and $|1\rangle$ are valid states of a quantum system, any linear combination $|\psi\rangle = \alpha|0\rangle + \beta|1\rangle$ is also a valid state.

Until measured, the system does not "possess" a hidden definite classical value. The qubit simultaneously explores both basis states with complex weights $\alpha$ and $\beta$.

---

## 4. Quantum Measurement & The Born Rule

Measurement in quantum computing is described by projection operators:

$$M_0 = |0\rangle\langle 0| = \begin{bmatrix} 1 & 0 \\ 0 & 0 \end{bmatrix}, \quad M_1 = |1\rangle\langle 1| = \begin{bmatrix} 0 & 0 \\ 0 & 1 \end{bmatrix}$$

### The Born Rule
The probability $P(m)$ of obtaining measurement outcome $m \in \{0, 1\}$ is given by:

$$P(0) = \langle \psi | M_0^\dagger M_0 | \psi \rangle = |\alpha|^2$$

$$P(1) = \langle \psi | M_1^\dagger M_1 | \psi \rangle = |\beta|^2$$

### Wave Function Collapse
Measurement irreversibly alters the quantum system. Upon measuring outcome $0$, the post-measurement state collapses to:

$$|\psi'\rangle = \frac{M_0 |\psi\rangle}{\sqrt{P(0)}} = \frac{\alpha}{|\alpha|} |0\rangle \equiv |0\rangle$$

Subsequent measurements in the same basis will yield $0$ with 100% certainty.

---

## 5. Quantum Logic Gates (Unitary Matrices)

All reversible operations in quantum mechanics are represented by **unitary operators** $U$ satisfying $U^\dagger U = U U^\dagger = I$, which preserves the inner product $\langle \psi | \psi \rangle = 1$.

### The Hadamard Gate ($H$)
The Hadamard gate creates an equal superposition with real, positive amplitudes when applied to ground state $|0\rangle$:

$$H = \frac{1}{\sqrt{2}} \begin{bmatrix} 1 & 1 \\ 1 & -1 \end{bmatrix}$$

Applying $H$ to basis states:

$$H|0\rangle = \frac{1}{\sqrt{2}}(|0\rangle + |1\rangle) \equiv |+\rangle$$

$$H|1\rangle = \frac{1}{\sqrt{2}}(|0\rangle - |1\rangle) \equiv |-\rangle$$

In the quantum coin toss, measuring state $|+\rangle$ yields:
- $P(0) = |1/\sqrt{2}|^2 = 0.5$ (50%)
- $P(1) = |1/\sqrt{2}|^2 = 0.5$ (50%)

### Pauli-X Gate (Bit-Flip / Quantum NOT)
$$X = \begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}, \quad X|0\rangle = |1\rangle, \quad X|1\rangle = |0\rangle$$

### Pauli-Y Gate (Bit & Phase-Flip)
$$Y = \begin{bmatrix} 0 & -i \\ i & 0 \end{bmatrix}, \quad Y|0\rangle = i|1\rangle, \quad Y|1\rangle = -i|0\rangle$$

### Pauli-Z Gate (Phase-Flip)
$$Z = \begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix}, \quad Z|0\rangle = |0\rangle, \quad Z|1\rangle = -|1\rangle$$

---

## 6. Geometric Representation: The Bloch Sphere

Any pure single-qubit state $|\psi\rangle$ can be parameterized using two spherical angles $\theta \in [0, \pi]$ and $\phi \in [0, 2\pi)$:

$$|\psi\rangle = \cos\left(\frac{\theta}{2}\right)|0\rangle + e^{i\phi}\sin\left(\frac{\theta}{2}\right)|1\rangle$$

This corresponds to a unit vector $\vec{r} = (x, y, z)$ on the surface of the **Bloch Sphere**:

$$x = \sin\theta \cos\phi = \langle X \rangle = 2\text{Re}(\alpha^* \beta)$$

$$y = \sin\theta \sin\phi = \langle Y \rangle = 2\text{Im}(\alpha^* \beta)$$

$$z = \cos\theta = \langle Z \rangle = |\alpha|^2 - |\beta|^2$$

- **North Pole ($\theta = 0, z = +1$):** Computational state $|0\rangle$.
- **South Pole ($\theta = \pi, z = -1$):** Computational state $|1\rangle$.
- **Equator ($z = 0, \theta = \pi/2$):** Balanced superposition states ($|+\rangle, |-\rangle, |+i\rangle, |-i\rangle$).

---

## 7. Multi-Qubit Systems & Tensor Products

When combining $n$ independent qubits, the composite state space is given by the tensor product ($\otimes$):

$$\mathcal{H} = \mathbb{C}^2 \otimes \mathbb{C}^2 \otimes \dots \otimes \mathbb{C}^2 = (\mathbb{C}^2)^{\otimes n}$$

For $n$ qubits, the dimension of the state space is $2^n$.

### Independent Hadamard Superposition
Applying Hadamard gates to $n$ qubits initialized in $|0\dots 0\rangle$:

$$|\psi_n\rangle = H^{\otimes n} |0\dots 0\rangle = \left(\frac{|0\rangle + |1\rangle}{\sqrt{2}}\right)^{\otimes n} = \frac{1}{\sqrt{2^n}} \sum_{x \in \{0, 1\}^n} |x\rangle$$

The theoretical probability of observing any specific bitstring $x$ is:

$$P(x) = \left|\frac{1}{\sqrt{2^n}}\right|^2 = \frac{1}{2^n}$$

For example:
- **1 Qubit:** 2 outcomes, $P(0) = P(1) = 50\%$
- **2 Qubits:** 4 outcomes, $P(00) = P(01) = P(10) = P(11) = 25\%$
- **3 Qubits:** 8 outcomes, $P(x) = 12.5\%$
- **4 Qubits:** 16 outcomes, $P(x) = 6.25\%$
- **5 Qubits:** 32 outcomes, $P(x) = 3.125\%$

---

## 8. Finite Sampling & Statistical Convergence

In practical simulations and physical hardware experiments, we measure a finite number of shots $N$. The observed probability of state $x$ is:

$$P_{\text{obs}}(x) = \frac{\text{Counts}(x)}{N}$$

By the **Central Limit Theorem**, the standard error $\sigma$ of the estimated probability scales inversely with the square root of shots:

$$\sigma \approx \sqrt{\frac{p(1-p)}{N}} \propto \frac{1}{\sqrt{N}}$$

As $N \to \infty$, $P_{\text{obs}}(x) \to P_{\text{theoretical}}(x)$.
