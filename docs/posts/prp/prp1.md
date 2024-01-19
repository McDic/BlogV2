---
categories:
  - Probability and Random Process
tags:
  - math
  - probability
  - statistics
title: PRP 1. Basic Principles of Probability
---

!!! migrated

    *This article is migrated from which I wrote on my old blog.*

안녕하세요.
이번 시리즈에서는 대학교 컴공에서 주로 가르치는 Probability and Random Process(이하 **PRP**)를 다루고자 합니다.
교재는 Princeton 대학교의 **[ORF309](https://web.math.princeton.edu/~rvan/ORF309.pdf)**를 참고했습니다.

<!-- more -->
---

# Chapter 1. Basic Principles of Probability

**Sample space**($\Omega$): *Set of all possible outcomes of a random experiment.* 예를 들면, 다음과 같습니다.

- 주사위 2개를 굴리는 모든 경우: $\Omega = \{ (i, j) | 1 \le i, j \le 6 \text{ , } i \in \mathbb{N} \text{ , } j \in \mathbb{N} \}$, $( | \Omega | = 36)$
- 버스를 기다리는 경우(즉시 도착부터 무기한 연기까지): $\Omega = [0, +\infty)$
- 꿀벌이 5초 동안 입체적으로 날아다니는 모든 경로: $\Omega = \{ \text{all continuous paths } w: [0, 5] \rightarrow \mathbb{R}^3 \}$

**Event**($A$, $B$, etc): *Subset of sample space $\Omega$*. 위 Sample space와 연계되는 예를 들면, 다음과 같습니다.

- 주사위 2개를 던졌는데 그 두 수의 합이 $x$인 경우: $A = \{ (i, j) | 1 \le i, j \le 6 \text{ , } i \in \mathbb{N} \text{ , } j \in \mathbb{N} \text{ , } i + j = x \}$
- 기다리는 버스가 1시간 안에 올 경우: $A = [0, 1]$
- 꿀벌이 첫 1초 동안 집($=House$) 안에서만 돌아다니는 모든 경로: $A = \{ \text{all continuous paths } w: [0, 5] \rightarrow \mathbb{R}^3 \text{ , } w(t) \in House \text{ for } t \in [0, 1] \}$

Sample space와 Event는 집합이므로, 임의의 집합 연산($A \cap B, A \cup B, A^C$)이 가능합니다.

**Probability**($P(A)$): *Assignment of a number to every event $A$ in respect of followings.*

1. $0 \le P(A) \le 1$
2. $P(\Omega) = 1$
3. $A \cap B = \emptyset \implies P(A \cup B) = P(A) + P(B)$

확률은 기본적으로 위 3가지를 만족하는 함수입니다. 모든 확률적 모델링은 이 3가지를 기반으로 시작됩니다. 이 3가지로부터 증명 가능한 것들을 들자면..

- $P(\Omega) = P(A \cup A^C) = P(A) + P(A^C) = 1$
- $A \in B \implies P(B) = P(A \cup (B-A)) = P(A) + P(B-A) \geq P(A)$
- $P(A) = \sum_{w \in A} P( \{ w \} )$ (단, $A$가 discrete할 때만 성립)

등등이 있습니다.

**Conditional Probability**: $P(A|B) = \frac{P(A \cap B)}{P(B)}$ ($P(B) > 0$)

$P(A|B)$는 $B$가 일어났다고 가정했을 때, $A$가 일어날 확률입니다. 한글로 직역해서 조건부 확률입니다. 이것도 정의로부터 증명 가능한 것들을 들자면..

- $P(A \cap B) = P(A | B) P(B) = P(B | A) P(A)$
- $P(A | A) = 1$
- $P(A \cap B) \le P(B) \implies 0 \le P(A | B) \le 1$
- $A \cap B = \emptyset \implies P(A \cup B | C) = P(A | C) + P(B | C)$

**Bayes Formula**: 목표 이벤트와 전제의 위치를 바꿔주는 신묘한 공식입니다.

$$
P(A) = P(A \cap B) + P(A \cap B^C) = P(A | B) P(B) + P(A | B^C) P(B^C) \\
\therefore P(B | A) = \frac{P(A \cap B)}{P(A)} = \frac{P(A | B) P(B)}{P(A | B) P(B) + P(A | B^C) P(B^C)}
$$

다음은 *Bayes Formula*의 예제 문제입니다.

- 어떤 medical test가 있습니다. 해당 test는 실제 환자가 검사하면 95%의 확률로 양성이 나오고, 환자가 아닌 사람이 검사하면 2%의 확률로 양성이 나옵니다. 전체 population 중에서 0.1%에 해당하는 사람이 실제 환자입니다. 당신이 positive가 나왔을 때, 당신이 실제 환자일 확률은 얼마일까요?

$$
D = \begin{cases} 1 \text{ if disease} \\ 0 \text{ else} \end{cases},
O = \begin{cases} 1 \text{ if positive} \\ 0 \text{ else} \end{cases}
$$

$$
\begin{aligned}
P(D | O) &= \frac{P(O | D) P(D)}{P(O | D) P(D) + P(O | D^C) P(D^C)} \\
&= \frac{0.95 \cdot 0.001}{0.95 \cdot 0.001 + 0.02 \cdot 0.999} \approx 0.045389
\end{aligned}
$$

Princeton 교재에서는, 인간의 직감 상으로 봤을 때는 positive가 나오면 매우 높은 확률로 환자일 것 같지만, 실제로 그럴 확률은 낮다는 점을 지적하고 있습니다. 확률적인 사고를 기르는 것이 이런 함정에 빠지지 않도록 하는 데 큰 도움을 줄 것이라 생각이 되네요.

**Independent Events**: *$A$ and $B$ are independent if $P(A | B) = P(A)$.*

- $P(A | B) = \frac{P(A \cap B)}{P(B)} = P(A) \iff P(A \cap B) = P(A) P(B)$
- $A, B$가 독립이면 $A, B^C$도 독립입니다. 역도 성립합니다.
- 독립을 $n$개 항으로 일반화하면, *$A_1, A_2, \ldots, A_n$ are independent if $P(\bigcap_i A_i) = \prod_i P(A_i)$.*

**Random Variables**: *Function mapping from sample space to set of values.*

이 중에서 특히 *set of values*에 해당하는 집합이 $\mathbb{R}, \mathbb{C}$ 등 숫자 집합일 경우, random variable이 *numerical*하다고 표현합니다.

Random variables의 예를 들면 다음과 같은 것들이 있습니다.

- 동전을 3번 던져서 나온 head의 개수. $X(HHH) = 3$, $X(HHT) = X(HTH) = X(THH) = 2$, $X(HTT) = X(THT) = X(TTH) = 1$, $X(TTT) = 0$.
- head가 나올 때까지 동전을 계속해서 던진 횟수. $X: \Omega \rightarrow \mathbb{N} \cup \{ +\infty \}$
- $[0, 1]$에서 random하게 뽑은 실수. $X: \Omega \rightarrow [0, 1]$

Random variables는 크게 *discrete*, *continuous* 2가지로 나눌 수 있는데요. 어떤 Random variable의 치역이 *finite*하거나 *countable*하면 *discrete*하고, 그렇지 않으면 *continuous*합니다.

**Expectation**: *$X: \Omega \rightarrow D$, $f: D \rightarrow \mathbb{R}$. Then $E(f(X)) = \sum_{i \in D} f(i) P(X = i)$. (for discrete random variables)*

특히, $X$가 *numerical*하면 $E(X) = \sum_{i \in D} i P(X = i)$ 입니다.

Expectation 계산의 예를 들면..

$$
1_A(w) = \begin{cases} 1 & \text{if } w \in A \\ 0 & \text{else} \end{cases}
\implies E(1_A) = 1 \cdot P(1_A = 1) + 0 \cdot P(1_A = 0) = P(A)
$$

**Distribution**: *$X: \Omega \rightarrow D$, Collection $P(X = i)_{i \in D}$ is distribution of $X$.*

- 서로 다른 random variable이 같은 distribution을 가질 수 있습니다. (ex: 주사위 2번 던지기 - 첫 번째 주사위의 값과 두 번째 주사위의 값을 각각 random variable로 생각했을 때, 두 random variable들은 같은 distribution을 갖습니다.)
- 둘 이상의 random variable이 연관될 경우 이를 *Joint Distribution*이라고 합니다.
- $E(f(X, Y)) = \sum_{i \in D, j \in D'} f(i, j) P(X=i, Y=j)$

**Linearity of Expectation**: $E(aX + bY) = aE(X) + bE(Y)$.

$$E(aX) = \sum_{i \in D} ai P(X=i) = a \sum_{i \in D} i P(X=i) = aE(X)$$

$$
\begin{aligned}
E(X+Y) &= \sum_{x \in D} \sum_{y \in D'} (x+y) P(X=x, Y=y) \\
&= \sum_{x \in D} \sum_{y \in D'} x P(X=x, Y=y) + \sum_{x \in D} \sum_{y \in D'} y P(X=x, Y=y) \\
&= \sum_{x \in D} x P(X=x) + \sum_{y \in D'} y P(Y=y) = E(X) + E(Y)
\end{aligned}
$$

- $\sum_{x \in D} P(X=x, Y=y) = P(Y=y)$ 입니다. (Probability의 3번째 특성을 참조해주세요.)

**Independent Random Variables**: *$X: \Omega \rightarrow D_X, Y: \Omega \rightarrow D_Y, X \bot Y \text{ if } \forall_{x \in D, y \in D'} P(X=x | Y=y) = P(X=x)$.*

추가적으로, 두 random variable에게서 나올 수 있는 가능한 모든 event의 쌍의 두 event가 서로 *independent*하면 두 random variable을 *independent*하다고 표현합니다.

$$
X \bot Y \iff \forall_{x \in D, y \in D'} P(X=x, Y=y) = P(X=x) P(Y=y)
\implies \forall_{x \in D, y \in D'} E(f(X) g(Y)) = E(f(X)) E(g(Y))
$$

**Conditional Expectation**: *$E(f(X) | Y=y) = \sum_{x \in D} f(x) P(X=x | Y=y)$.*

Linearity of Expectation과 거의 동일한 테크닉으로, *Linearity of Conditional Expectation*을 증명할 수 있습니다.

$$
E(aX | Y=y) = \sum_{x \in D} aX P(X=x | Y=y) = aE(X | Y=y)
$$

$$
\begin{aligned}
E(X+Y | Z=z) &= P(Z=z)^{-1} \sum_{x \in D} \sum_{y \in D'} (x+y) P(X=x, Y=y, Z=z) \\
&= P(Z=z)^{-1} \biggl( \sum_{x \in D} \sum_{y \in D'} x P(X=x, Y=y, Z=z) + \sum_{x \in D} \sum_{y \in D'} y P(X=x, Y=y, Z=z) \biggr) \\
&= P(Z=z)^{-1} \biggl( \sum_{x \in D} x P(X=x, Z=z) + \sum_{y \in D'} y P(Y=y, Z=z) \biggr) \\
&= E(X | Z=z) + E(Y | Z=z)
\end{aligned}
$$

다음은 *Conditional Expectation*의 예제 문제입니다.

- 주사위를 6이 나올 때까지 던진다고 가정해봅시다. 주사위를 $k$번 던졌다는 것을 알 때, 주사위의 눈이 $1$이 나온 횟수의 Expectation은 얼마일까요?

$X_i$를 $i$번째 주사위의 눈이라고 정의합니다.

$$
\begin{aligned}
\text{answer} &= E(\sum_{i=1}^{k-1} 1_{X_i=1} | X_k = 6) \\
&= \sum_{i=1}^{k-1} E(1_{X_i=1} | X_k=6) \\
&= \sum_{i=1}^{k-1} P(X_i=1, X_{i+1} \ne 6, X_{i+2} \ne 6, \cdots, X_{k-1} \ne 6 | X_k = 6) \\
&= \sum_{i=1}^{k-1} \frac{P(X_1 \ne 6, X_2 \ne 6, \cdots, X_i = 1, \cdots, X_{k-1} \ne 6, X_k = 6)}{P(X_1 \ne 6, X_2 \ne 6, \cdots, X_i \ne 6, \cdots, X_{k-1} \ne 6, X_k = 6)} \\
&= \sum_{i=1}^{k-1} \frac{1}{5} = \frac{k-1}{5}
\end{aligned}
$$

$X_i$가 서로 independent한지 여부를 알지 않고도 문제를 풀 수 있음에 주목해주시기 바랍니다.

**Conditional Distribution**: *$X: \Omega \rightarrow D, Y: \Omega \rightarrow D'$. Collection $P(X=i | Y=j)_{i \in D, j \in D'}$ is conditional distribution.*

$$
\begin{cases}
P(X=x) = \sum_{y} P(X=x, Y=y) = \sum_{y} P(X=x | Y=y) P(Y=y) \\
E(X) = \sum_{y} x P(X=x, Y=y) = \sum_{y} E(X | Y=y) P(Y=y)
\end{cases}
$$

위 두 공식에 대한 증명은 다음과 같습니다.

$$
\sum_{y} P(X=x | Y=y) P(Y=y) = \sum_{y} P(X=x, Y=y) = P(X=x)
$$

$$
\begin{aligned}
\sum_{y} E(X | Y=y) P(Y=y) &= \sum_{y} \sum_{x} x P(X=x | Y=y) P(Y=y) \\
&= \sum_{y} \sum_{x} x P(X=x, Y=y) \\
&= \sum_{x} x P(X=x) = E(X)
\end{aligned}
$$

---

이상으로, Probability에 대해 기본을 훑어보았습니다. *Variance* 같은 것들이 남아있긴 하지만, *ORF309*에서 이걸 뒷 chapter에서 다루면 뒷 chapter에 해당하는 게시글에, 그렇지 않다면 이 게시글에 추가해두도록 하겠습니다!

읽어주셔서 감사합니다.
