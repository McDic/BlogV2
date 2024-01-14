---
date: 2022-06-03
categories:
  - Linear Algebra
tags:
  - math
  - linear-algebra
title: LA 1. Vector Spaces
slug: la-1
---

!!! info "Migrated article"

    *This article is migrated from which I wrote on my old blog.*

안녕하세요. 반년만의 포스팅이네요.. 제가 1~2달 전쯤부터 온라인으로 수학 스터디를 시작했는데, 스스로 정리를 해가면서 진행해야 할 것 같아서.. 포스팅을 시작하게 되었습니다. 이번 시리즈에서는 Linear Algebra(이하 **LA**)를 다루고자 합니다. 교재는 Stephen H. Friedberg 외 2명이 작성한 [Linear Algebra 5th Edition](https://www.amazon.com/Linear-Algebra-5th-Stephen-Friedberg/dp/0134860241)을 참고했습니다.

<!-- more -->
---

# Chapter 1. Vector Spaces

**Field**: *Field $F$ is a set on which two operations $+$, $\cdot$ are defined so that, for $\forall_{x, y}$ there are unique elements $x+y, x \cdot y$ and following conditions hold;*

- Commutativity(교환법칙) of $+, \cdot$: $a+b=b+a$, $a \cdot b = b \cdot a$
- Associativity(결합법칙) of $+, \cdot$: $(a+b)+c=a+(b+c)$, $(a \cdot b) \cdot c = a \cdot (b \cdot c)$
- Existence of identity elements(항등원 존재) for $+, \cdot$: $0+a = a$, $1 \cdot a = a$
- Existence of inverses(역원) for $+, \cdot$: $\forall_{a} \exists_{a'} a+a'=0$, $\forall_{b} \exists_{b'} b \cdot b' = 1$ ($b \ne 0$)
- Distributivity(분배법칙) of $\cdot$ over $+$: $a \cdot (b+c) = a \cdot b + a \cdot c$

Field의 예시를 들면...

- Set of real numbers of typical addition and multiplication
- Boolean set $\{True, False\}$ where $+$ is "or" and $\cdot$ is "and"

**Vector Space (Linear Space)**: *Vector Space $V$ over a field $F$ with operations $+, \cdot$ (addition and scalar multiplication) are defined so that, $\forall_{x, y \in V}, \forall_{a \in F}$ there are unique elements $x+y$ and $ax$, and following conditions hold;*

- **VS 1** / Commutativity(교환법칙) of $+$: $\forall_{x, y \in V} x+y=y+x$
- **VS 2** / Associativity(결합법칙) of $+$: $\forall_{x, y, z \in V} (x+y)+z = x+(y+z)$
- **VS 3** / Existence of identity elements(항등원) for $+$: $\forall_{x \in V} \exists_{0} x+0 = x$
- **VS 4** / Existence of inverse(역원) for $+$: $\forall_{x \in V} \exists_{x'} x+x'=0$
- **VS 5** / Existence of identity elements(항등원) for $\cdot$: $\forall_{x \in V} 1x = x$
- **VS 6** / Associativity(결합법칙) of $\cdot$: $\forall_{a, b \in F} \forall_{x \in V} (ab)x = a(bx)$
- **VS 7** / Distributivity(분배법칙) of $\cdot$ over $+$ (1): $\forall_{a \in F} \forall_{x, y \in V} a(x+y) = ax+ay$
- **VS 8** / Distributivity(분배법칙) of $\cdot$ over $+$ (2): $\forall_{a, b \in F} \forall_{x \in V} (a+b)x = ax+bx$

$V$의 원소를 **vector**라 부르고, $F$의 원소를 **scalar**라 부르기로 정의합니다.

Vector Space의 예를 들자면..

- Field $F$로부터 만들어지는 모든 $n$-tuple들의 집합을 $F^n$이라 표현합니다. 이때, $F^n$은 Vector Space입니다. ex: $R^3$, $C^2$ 등
- $m \times n$ 크기를 가지는 모든 행렬(**matrix**)들의 집합 또한 Vector Space입니다. 행렬들끼리 곱하면 크기가 달라질 수도 있어서 Vector Space가 아니지 않나? 싶을 수 있는데, **VS** 내용에는 Vector Space 원소들 간의 곱셈에 대한 언급이 없습니다.
- $S$가 공집합이 아닌 어떤 집합이고, $F$가 어떤 Field일 때, $f(S, F)$를 $S$에서 $F$로 가는 임의의 함수들의 집합이라고 합시다. $f = g \iff \forall_{s \in S} f(s) = g(s)$ 라고 할 때, $f(S, F)$는 다음 addition과 scalar multiplication에 대한 Vector Space입니다.

    $$(f+g)(s) = f(s)+g(s), (cf)(s) = c(f(s))$$

- Field $F$로부터 **coefficient**(계수)를 뽑아낸 **Polynomial**(다항식)은 다음과 같이 정의됩니다.

    $$f(x) = \sum_{i=0}^{n} a_i x^i$$

    - Polynomial's **degree**(차수): Polynomial의 계수가 0이 아닌 가장 높은 항의 차수를 의미합니다. 만약 모든 항의 계수가 0일 경우, 이 polynomial은 **zero polynomial**이라고 하며, 차수를 편의상 $-1$로 취급합니다.

    Polynomial의 addition을 계수끼리만 더하는 것으로 생각하고, scalar multiplication을 모든 계수에 똑같은 상수를 곱해주는 것으로 생각하면, 그리고 두 polynomial의 equality를 모든 계수가 동일해야 같다는 것으로 생각하면,, 모든 Polynomial들의 집합 또는 Vector Space입니다. ($n$-tuple과 거의 동일하다고 생각하면 될 것 같습니다.)

- **Sequence**(수열): Sequence in $F$ is a function $\sigma: N \rightarrow F$ where $N$ is set of positive integers. Addition을 $(a+b)_n = a_n + b_n$, scalar multiplication을 $(k \cdot a)_n = k \cdot a_n$으로 생각한다면, Sequence들의 집합 또한 Vector Space입니다. 저는 이 예시가 위의 $f(S, F)$의 특수 케이스라고 생각합니다.

**Cancellation Law for Vector Addition**: Let $V$ be vector space. $\forall_{x, y, z \in V} x+z = y+z \implies x=y$.

증명은 VS 2, 3, 4에 의해 가능합니다.

- *Corollary 1*: Vector $0$ described in VS 3 is unique.

    Let $x \in V$, there are two vectors $0$ and $0'$ which satisfies VS 3. Then $x = x + 0 = x + 0'$, by Cancellation Law for Vector Addition, $0 = 0'$.

- *Corollary 2*: Vector $y$ described in VS 4 is unique.

    Let's suppose there are two vectors $y$ and $y'$ which satisfies VS 4. Then $0 = x + y = x + y'$ ($0$ is unique by Corollary 1), then $y = y'$ by Cancellation Law for Vector Addition.

**Zero Vector**: Vector $0$ in VS 3.

**Additive Inverse of $x$**: Vector $y$ in VS 4.

---

**Subspace**: Vector space $V$'s subset $W$ which satisfies Vector Space conditions.

다행스럽게도, 어떤 Vector Space $V$의 부분집합 $W$가 Subspace인지 증명하는 것은 다음 3가지만 보면 됩니다!

1. Closed under addition: $\forall_{x, y \in W} x+y \in W$
2. Closed under scalar multiplication: $\forall_{c \in F, x \in W} cx \in W$
3. $0 \in W$

Subspace의 예시를 들자면..

- $P_n(F)$를 degree가 $n$ 이하인 모든 Polynomial들의 집합이라고 하면, $P_n(F)$는 Subspace입니다. ($n \ge -1$)

    1. 차수가 $n$ 이하인 두 다항식을 더해도 여전히 차수가 $n$ 이하입니다.
    2. 차수가 $n$ 이하인 다항식에 임의의 상수를 곱해도 여전히 차수가 $n$ 이하입니다.
    3. Zero Polynomial의 차수는 -1이므로, $0 \in P_n(F)$ 입니다.

- $C(R)$을 $R \rightarrow R$인 모든 continuous function들의 집합이라고 하면, $C(R)$은 Subspace입니다.

    1. $\forall_{f, g \in C(R)} (f+g)$ 는 정의역과 치역이 실수인 연속함수입니다. (두 연속함수의 합은 연속함수)
    2. $\forall_{f \in C(R), k \in R} (kf)$ 는 정의역과 치역이 실수인 연속함수입니다. $(kf)(x) = k f(x) = f(x) g(x)$ where $g(x) = k$로 생각할 수 있기 때문입니다.
    3. $f(x) = 0$인 zero function $f \in C(R)$ 입니다.

- 같은 Field와 Vector Space 내의 여러 Subspace들에 대해서, 그 Subspace들의 교집합 또한 Subspace입니다.

    두 Subspace를 각각 $W_1$, $W_2$ 라 하겠습니다.

    1. $\forall_{x, y \in W_1 \cap W_2} x+y \in W_1, x+y \in W_2 \implies x+y \in W_1 \cap W_2$
    2. $\forall_{x \in W_1 \cap W_2, k \in F} kx \in W_1, kx \in W_2 \implies kx \in W_1 \cap W_2$
    3. Vector Space 내의 $0$은 유일하고, $0 \in W_1, 0 \in W_2 \implies 0 \in W_1 \cap W_2$

**Transpose**: Transpose of $m \times n$ matrix $A$ is called $A^t$, which has size $n \times m$ and $A_{i,j} = A^{t}_{j,i}$.

$$
\begin{pmatrix}
1 & 2 \\
3 & 4 \\
5 & 6 \\
\end{pmatrix}^t =
\begin{pmatrix}
1 & 3 & 5 \\
2 & 4 & 6 \\
\end{pmatrix}
$$

**Symmetric Matrix**: Matrix $A$ such that $A = A^t$.

$n \times n$ 크기의 모든 Symmetric Matrix들의 집합(이하 $W$)은 $M_{n \times n}$의 Subspace입니다. 그 이유는

1. Zero matrix의 transpose는 Zero matrix이므로, $0 \in W$ 입니다.
2. $\forall_{A, B \in W} A^t = A, B^t = B \implies (A+B)^t = A^t + B^t = A+B \implies A+B \in W$
3. $\forall_{A \in W} A^t = A \implies \forall_{k \in F} (kA)^t = kA^t = kA \implies kA \in W$

**Upper Triangular**: $i>j \implies A_{i,j} = 0$일때 $A$는 Upper Triangular입니다.

**Diagonal Matrix**: $i \ne j \implies A_{i,j} = 0$일때 $A$는 Diagonal Matrix입니다.

**Trace**: Trace of $n \times n$ sized matrix $M$ is $tr(M) = \sum_{i=1}^{n} M_{i,i}$, which is sum of all diagonal entries.

- $\{ A | A \in M_{n \times n}(R), tr(A) = 0 \}$ 도 Subspace입니다. $tr(A) + tr(B) = tr(A+B)$이고, $k \cdot tr(A) = tr(k \cdot A)$이기 때문입니다.

---

**Linear Combination**: Let $V$ be vector space, $\emptyset \ne S \subseteq V$, Vector $v \in V$ is linear combination of vectors in $S$ if $v = \sum_{i=1}^{n} a_i v_i$ where $a_i \in F, v_i \in S$.

Linear Combination의 예시로는..

- $2x^3 - 2x^2 + 12x - 6$은 $x^3 - 2x^2 - 5x - 3$과 $3x^3 - 5x^2 - 4x - 9$의 Linear Combination입니다. 하지만 $3x^3 - 2x^2 + 7x + 8$은 아닙니다. $f(x) = a(x^3 - 2x^2 - 5x - 3) + b(3x^3 - 5x^2 - 4x - 9)$로 연립방정식을 계산해보면 됩니다.

**Span**: Span of $S$ ($\emptyset \ne S \in W$) is the set consisting of all linear combinations of the vectors in $S$.

편의상, $span(\emptyset) = \{ 0 \}$ 입니다. 이제 Span의 예를 들자면..

- $R^3$ 공간에서 $(1, 0, 0)$ (x축 방향 unit vector)과 $(0, 1, 0)$ (y축 방향 unit vector)의 span은 xy평면입니다.

**Theorem 1.5**: $S (\in V)$의 span은 $S$를 포함하는 $V$의 subspace입니다. 더 나아가 $S$를 포함하는 $V$의 임의의 subspace는 $S$의 span을 포함하는 집합이어야 합니다.

- 증명: $S = \emptyset$인 경우는 자명합니다. $S \ne \emptyset$인 경우,
    - $z \in S \implies 0z = 0 \in span(S)$
    - $x, y \in S \implies x+y \in span(S)$
    - $x \in S, k \in F \implies kx \in span(S)$

    이제 $span(S)$는 $V$의 subspace가 되기 위한 3가지 조건을 충족하였고, $S \subset span(S)$ 이므로, Theorem 1.5는 성립합니다.

**Generates(Spans)**: $S (\subset V)$ generates vector space $V$ if $span(S) = V$.

여기서, 역으로 $V$를 generate하는 집합이 항상 유일하다고 생각하면 안 됩니다! 어떤 Vector Space를 generate하는 집합은 무수히 많을 수 있습니다.(그게 일반적입니다.) 이제 어떤 집합이 특정 Vector Space를 generate하는 것의 예시를 들면..

- x축 방향 unit vector, y축 방향 unit vector, z축 방향 unit vector는 $R^3$을 generate합니다. 더 나아가 임의의 independent한 3개의 vector($R^3$ 내부)는 $R^3$를 generate합니다.

- $\begin{pmatrix} 1 & 1 \\ 0 & 1 \\ \end{pmatrix}, \begin{pmatrix} 1 & 1 \\ 1 & 0 \\ \end{pmatrix}, \begin{pmatrix} 0 & 1 \\ 1 & 1 \\ \end{pmatrix}, \begin{pmatrix} 1 & 0 \\ 1 & 1 \\ \end{pmatrix}$ 는 $M_{2 \times 2}(R)$을 generate합니다.

---

**Linearly Dependent**: Subset $S$ of vector space $V$ is linearly dependent if vectors $v_i \in S$ and coefficients $0 \ne a_i \in F$ exist such that $\sum_{i=1}^{n} a_i v_i = 0$.

예시를 들면..

- $S = \{(1, 3, -4, 2), (2, 2, -4, 0), (1, -3, 2, -4), (-1, 0, 1, 0)\} \subset R^4$은 linearly dependent합니다. ($4a_1 - 3a_2 + 2a_3 = (0, 0, 0, 0)$)

**Linearly Independent**: If subset $S$ of vector space $V$ is not linearly dependent, then it's linearly independent.

몇 가지 특징을 추가로 적어보면..

1. $\emptyset$은 linearly independent합니다.
2. Nonzero vector를 하나 가지고 있는 set은 linearly independent합니다. (증명: $\exists_{a \ne 0} au = 0 \implies u = 0$)

**Theorem 1.6**: Let $S_1 \subset S_2 \subset V$ where $V$ is vector space. If $S_1$ is linearly dependent then $S_2$ is linearly dependent.

- 증명: $\sum_{i=1}^{n} a_i v_i = 0$인 $0 \ne a_i \in F$, $v_i \in S_1$가 존재합니다. $v_i \in S_1 \implies v_i \in S_2$이므로, $S_2$도 linearly independent합니다.

- *Corollary*: If $S_2$ is linearly independent, then $S_1$ is linearly independent. 증명은 Theorem 1.6 명제의 대우로 가능합니다.

**Theorem 1.7**: Let $S$ be linearly independent subset of vector space $V$, and $v \in V, v \not \in S$. Then $S \cup \{ v \}$ is linearly dependent iff $v \in span(S)$.

- 정방향 명제 증명: $S \cup \{v\}$가 linearly dependent하다면, $a v + \sum_{i=1}^{n} a_i v_i = 0$ 인 경우가 존재. 근데 $a = 0$이면 좌변이 0이 될 수 없으므로 $a \ne 0$ 이어야 합니다. 양변을 $-a$로 나누고 $v$를 우변으로 이항하면 $v = \sum_{i=1}^{n} \frac{a_i}{-a} v_i$ 가 되고, 따라서 $v \in span(S)$ 입니다.
- 역방향 명제 증명: $v \in span(S)$라면, $v = \sum_{i=1}^{n} a_i v_i$ ($a_i \ne 0$)인 coefficient set이 존재합니다. 따라서, $\sum_{i=1}^{n} a_i v_i + (-1) v = 0$인 nontrivial representation이 존재하게 되고, $S$는 linearly dependent하게 됩니다.

---

**Basis**: Basis $\beta$ for vector space $V$ is a linearly independent subset of $V$ which generates $V$.

Basis의 예를 들면..

- $span(\emptyset) = \{0\}$ 이고 $\emptyset$은 linearly independent하므로, $\emptyset$은 zero vector의 basis입니다.
- $e_i = (a_1, a_2, \ldots, a_n)$ where

    $$a_j = \begin{cases} 1, & i=j \\ 0, & i \ne j \end{cases}$$

    일때 $\{ e_1, e_2, \ldots, e_n \}$은 $F^n$의 basis입니다. 더불어서 이를 $F^n$의 standard basis라고 합니다.
- $\{ x^0, x^1, \ldots, x^n \}$은 $P_n(F)$의 standard basis입니다. $n = \infty$ 일 수도 있습니다. (이 경우 해당 집합은 $P(F)$의 basis가 됩니다.) 일부 Vector Space의 경우 infinite한 basis를 가지는 경우도 있습니다.

**Theorem 1.8**: Let $V$ be vector space and $v_i \in V (i = 1, 2, \ldots, n)$ be unique vectors. $\beta = \{v_1, v_2, \ldots, v_n\}$ is a basis for $V$ iff $\forall_{v \in V} v = \sum_{i=1}^{n} a_i v_i$ is uniquely expressed. (There is only one $a_i$ solution.)

- 정방향 명제 증명: $v = \sum_{i=1}^{n} a_i v_i = \sum_{i=1}^{n} b_i v_i$ 라고 표현하면, $\sum_{i=1}^{n} (a_i - b_i) v_i = 0$ 입니다. 그리고 $\beta$가 linearly independent하므로(다른 말로 하면 $\beta$에서 만들 수 있는 linear combination으로 zero vector를 만드는 방법은 오직 모든 coefficient를 0으로 만드는 것이므로), $a_i = b_i$입니다. 따라서 솔루션은 하나 뿐입니다.
- 역방향 명제 증명: 대우를 증명해보겠습니다. $\beta$가 basis가 아니라면, $\sum_{i=1}^{n} a_i v_i$가 unique하게 express되지 않는다는 것을 보이겠습니다.
    - Lemma. $span(\beta) \subset V$ 입니다.
        - $\forall_{x, y \in \beta \subset V} x+y \in span(\beta), x+y \in V$
        - $\forall_{x \in \beta \subset V, k \in F} kx \in span(\beta), kx \in V$
        - $0 \in span(\beta), 0 \in V$
    - 따라서 $\beta$가 basis가 아니라면, $V - span(\beta) \ne \emptyset$이거나 아니면 $\beta$가 linearly dependent하다는 뜻입니다.
        1. $V - span(\beta) \ne \emptyset$일때: 이는 어떤 $v \in V - span(\beta)$가 존재하여, 해당 vector를 $\beta$의 linear combination으로 표현할 수 없다는 얘기가 됩니다. (Uniquely express 불가)
        2. $\beta$가 linearly dependent할때: 어떤 $a_i$가 존재하여 $\sum_{i=1}^{n} a_i v_i = 0$이고(최소 하나 이상의 coefficient가 nonzero), $v = \sum_{i=1}^{n} b_i v_i$ 라면, $v = \sum_{i=1}^{n} b_i v_i = \sum_{i=1}^{n} (a_i + b_i) v_i$ 입니다.

**Theorem 1.9**: If vector space $V$ is generated by finite set $S$, then some subset of $S$ is a basis for $V$. Therefore $V$ has a finite basis.

증명은 $S$로부터 원소를 계속 뽑아나가는(단, 뽑힌 원소의 집합이 linearly independent가 되도록) 방식으로 증명을 하네요.. 생략하겠습니다.

**Replacement Theorem(1.10)**: Let $V$ be vector space which is generated by set $G$ where $|G| = n$ and let $L$ be linearly independent subset of $V$ where $|L| = m$. Then $m \le n$ and $H$ exists where $H \subset G, |H| = n-m$, and $L \cup H$ generates $V$.

느낌은 이렇게 보시면 될 것 같습니다. $V$의 linearly independent한 subset은 $V$를 만드는 데 드는 최소 차원 이하의 개수의 원소를 보유하고 있고, $G$의 어떤(임의는 아니고) $m$개 원소를 $L$로 교체시켜서 여전히 $V$를 generate할 수 있다는 느낌으로 보시면 될 것 같습니다.

- 증명:
  $m=0$이면 $L=\emptyset$이고, $H=G$인 자명한 해를 구할 수 있습니다.
  이제 $m$에 대해 수학적 귀납법을 시도하면 되는데.. 증명을 제대로 이해하면 서술하도록 하겠습니다.

- *Corollary*: Let vector space $V$ having a finite basis. Then all bases for $V$ are finite and every basis for $V$ contains the same number of vectors.

    - 증명: 어떤 두 basis $\beta$, $\gamma$가 모두 $V$를 generate하고, $\beta$는 finite하다고 가정해봅시다. 그러면 $\gamma$는 $V$의 independent subset이고, *Replacement Theorem*에 의해서 $| \gamma | \le | \beta |$ 이고, $\gamma$는 finite set이 됩니다. 또 Replacement Theorem을 역으로 $\gamma$에 적용해서 $| \beta | \le | \gamma |$가 되고, 이는 $| \beta | = | \gamma |$를 imply합니다.

**Finite Dimensional**: Vector space is finite-dimensional if it has a basis which has finite number of vectors.

**Dimension**: Dimension of $V$ ($\dim(V)$) is number of vectors in basis of $V$. 위 Corollary에서 finite-dimensional한 Vector Space의 모든 basis의 원소의 개수는 동일하다는 것을 증명했으므로, 아무 basis의 원소의 개수를 구해도 됩니다.

**Infinite Dimensional**: Vector space is infinite-dimensional if it's not finite-dimensional.

Dimension의 예를 들면..

- $\dim(\{0\}) = 0$
- $\dim(F^n) = n$
- $\dim(M_{m \times n}) = mn$
- $\dim(P_n(F)) = n+1$
- $\dim(P(F)) = \infty$
- $\dim(C) = \begin{cases} 1, & F=C \\ 2, & F=R \end{cases}$ (Field에 따라 차원이 달라질 수 있음에 유의하세요.)

이제 dimension과 관련된 lemma를 몇 가지 살펴보면..

- *Corollary*: Let $V$ be vector space with $\dim(V) = n$.
    1. Any finite generating set for $V$ contains at least $n$ vectors. Furthermore, any finite generating set for $V$ with $n$ vectors is a basis for $V$.
    2. Any linearly independent subset of $V$ with $n$ vectors is a basis for $V$.
    3. If $L$ is a linearly independent subset of $V$, then there is a basis $\beta$ where $L \subseteq \beta$.

    증명:

    1. Theorem 1.9에 의해, 임의의 finite generating set $A$는 어떤 basis를 부분집합으로 갖고 있습니다. 그런데 $V$의 basis는 원소의 개수가 $n$이므로, $|A| \ge n$ 입니다. 마찬가지로, $|A| = n$ 이라면, $A$는 basis입니다.
    2. $A$가 linearly independent한 $V$의 subset이고, $\beta$가 $V$의 basis라고 합시다. Replacement Theorem에 의해 $\emptyset \subset \beta$, $A \cup \emptyset = A$이 $V$를 generate합니다. 따라서 $A$는 basis입니다.
    3. 이것 또한 Replacement Theorem으로 증명할 수 있습니다. $B \subset \beta$ ($|B| = n - |A|$)인 $B$를 뽑아서 $A \cup B$가 $V$를 generate하게 만들 수 있습니다. 이때, $A \cup B$는 $A$로부터 extend할 수 있는 $V$의 basis가 됩니다.

책 50쪽에서는 Linearly Independent Sets, Bases, Generating Sets의 관계를 설명합니다. *Bases는 Linearly Independent Sets와 Generating Sets의 교집합입니다.*

**Theorem 1.11**: Let $W$ be subspace of finite-dimensional vector space $V$. Then $W$ is finite-dimensional and $\dim(W) \le \dim(V)$. Moreover, $\dim(W) = \dim(V) \implies V = W$.

- 증명: 이것도 vector를 하나씩 뽑아가면서 $W$의 basis를 만들어가는 식으로 증명을 하네요. 뭔가 이런 step스러운 과정이 아닌 다른 방식의 증명이 있으면 좋을텐데.. 그런 증명은 생각이 안 나네요.

- *Corollary*: If $W$ is a subspace of finite-dimensional vector space $V$, then any basis for $W$ can be extended to a basis for $V$
    - 증명: $W$의 basis는 $W$의 부분집합이면서 동시에 linearly independent합니다. 모든 $W$의 부분집합은 $V$의 부분집합이기도 합니다. Dimension의 Corollary (3)에 의해, 해당 basis(= $V$의 linearly independent subset)를 $V$의 basis로 extend할 수 있습니다.

**Lagrange Polynomial**: Let $c_0, c_1, \ldots, c_n$ be distinct values from an infinite field $F$. The lagrange polynomials $f_0(x), f_1(x), \ldots, f_n(x)$ is defined by $f_i(x) = \prod_{k; k \ne i} \frac{x-c_k}{c_i-c_k}$.

그러면 여기서 다음과 같은 사실을 관찰할 수 있습니다.

1. 각 Lagrange Polynomial의 차수는 $n$입니다. ($i \ne k$인 term이 모두 곱해졌기 때문)
2. $f_i(c_j) = int(i==j)$ 입니다.

특히 2번에 의해, $\beta = \{f_0, f_1, \ldots, f_n\}$는 linearly independent합니다. 증명은 다음과 같습니다.

- 특정 scalar $a_0, a_1, \ldots, a_n$에 대해 $\sum_{i=0}^{n} a_i f_i = 0$ 이라 해봅시다. ($0$는 zero function) 그러면 임의의 $j$에 대해 $\sum_{i=0}^{n} a_i f_i(c_j) = 0$ 입니다. (zero function이기 때문에 어떤 값을 polynomial의 미지수에 대입하더라도 $0$이 나와야 합니다.) 근데 $f_i(c_j) = int(i==j)$ 이므로, $\sum_{i=0}^{n} a_i f_i(c_j) = a_j = 0$ 이 됩니다. $a_0 = a_1 = \cdots = a_n = 0$ 이므로, $\beta$는 linearly independent 합니다.

여기서 $\dim(P_n(F)) = n+1 = |\beta|$ 이므로, $\beta$는 $P_n(F)$의 basis입니다. 이 말인 즉슨, $P_n(F)$에 속하는 임의의 polynomial은 Lagrange Polynomials의 linear combination이라는 뜻입니다. 이 representation(임의의 polynomial을 Lagrange Polynomial의 linear combination으로 나타내는 것)을 **Lagrange Interpolation Formula**라고 합니다!

---

Chapter 1.7은 Optional이라 스킵했습니다. Chapter 1.7의 주 내용은 임의의 Vector Space(infinite-dimensional 포함)가 basis를 가지고 있다는 것을 증명하는 것을 목적으로 하고 있습니다.
제가 학부 1학년 때 배웠던 내용하고는 난이도가 많이 달라서 놀랐습니다. 앞으로도 꽤 험난한 여정이 될 것 같은데.. 그래도 화이팅!!

읽어주셔서 감사합니다.
