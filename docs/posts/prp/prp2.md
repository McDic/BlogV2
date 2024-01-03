---
date: 2021-12-12
categories:
  - Probability and Random Process
tags:
  - math
  - probability
  - statistics
title: PRP 2. Bernoulli Processes
slug: prp-2
---

안녕하세요. 이 시리즈의 지난 article에서 *Basic Principles of Probability*에 대해 다뤄봤는데요. 이번에는 *Chapter 2. Bernoulli Processes*에 대해 다뤄보겠습니다.

<!-- more -->
---

# Chapter 2. Bernoulli Processes

**Bernoulli Variable**: *A random variable $X: \Omega \rightarrow \\{ 0, 1\\}$*.

**Bernoulli Process**: *Sequence $X_1, X_2, \ldots$ of independent Bernoulli variables with $P(X_i = 1) = p$.*

Princeton 교재에서는 *Bernoulli Process*를 independent trials, 즉 독립적인 yes/no 실행으로 생각하라고 하네요. (ex: 동전 던지기)

- $E(X_i) = 1 \cdot p + 0 \cdot (1-p) = p$

**Binomial Random Variable**: *Let $X_i$ to be Bernoulli Random Variable, then $S_n = \sum_{i=1}^{n} X_i$ is Binomial Random Variable.*

- $P(S_n = k) = \binom{n}{k} p^{k} (1-p)^{n-k}$
- $\sum_{i=0}^{n} P(S_n = i) = \sum_{i=0}^{n} \binom{n}{i} p^{i} (1-p)^{n-i} = (p + (1-p))^n = 1$
- $E(S_n) = \sum_{i=1}^{n} E(X_i) = np$
- 어떤 random variable $Z$가 *Binomial Distribution*($n, p$)를 가질 때, $Z \sim \text{Binom}(n, p)$ 라고 표현합니다.

*Variance*를 유도하는 과정은 조금 복잡한데, 다음과 같습니다.

$$
\begin{aligned} 
Var(S_n) &= E(S_n^2) - E(S_n)^2 \\ 
&= \sum_{i=1}^{n} x^2 \binom{n}{x} p^{x} (1-p)^{n-x} - n^2 p^2 \\ 
&= \sum_{i=1}^{n} nx \binom{n-1}{x-1} p^{x} (1-p)^{n-x} - n^2 p^2 \\ 
&= \sum_{i=0}^{n-1} n (x+1) \binom{n-1}{x} p^{x+1} (1-p)^{n-x-1} - n^2 p^2 \\ 
&= np \biggl( \sum_{x=0}^{n-1} x \binom{n-1}{x} p^x (1-p)^{n-x-1} + \sum_{x=0}^{n-1} \binom{n-1}{x} p^x (1-p)^{n-x-1} \biggr) - n^2 p^2 \\ 
&= np (E(S_{n-1}) + 1) - n^2 p^2 \\ &= np ((n-1)p + 1) - n^2 p^2 = np(1-p) 
\end{aligned}
$$

**Negative Binomial Random Variable**: *Let $T_k$ be $k$-th time of success in Bernoulli Process, then $T_k$ is Negative Binomial Random Variable.*

다시 한글로 정리하면, *Negative Binomial Random Variable*은 매 시간마다 발생할 확률이 $p$인 이벤트를 시도할 때, 해당 이벤트가 $k$번째로 일어나는 시간을 다루는 Random Variable입니다.

$$
\begin{aligned}
P(T_k = n) &= P(X_n = 1, S_{n-1} = k-1) = P(X_n = 1) P(S_{n-1} = k-1) \\
&= p \cdot \binom{n-1}{k-1} p^{k-1} (1-p)^{n-k} = \binom{n-1}{k-1} p^{k} (1-p)^{n-k}
\end{aligned}
$$

*Expectation*을 유도하는 과정은 추후 설명할 *Geometric Distribution*에 의해 쉽게 구할 수 있습니다.

$$
\begin{aligned}
E(T_k) &= E(T_1 + (T_2 - T_1) + (T_3 - T_2) + \cdots + (T_k - T_{k-1})) \\
&= E(T_1) + E(T_2 - T_1) + E(T_3 - T_2) + \cdots + E(T_k - T_{k-1}) = \frac{k}{p}
\end{aligned}
$$

**Geometric Random Variable**: *A random variable which is a special case of Negative Binomial Random Variable, $k = 1$.*

다시 한글로 정리하면, *Geometric Random Variable*은 매 시간마다 발생할 확률이 $p$인 이벤트를 시도할 때, 해당 이벤트가 최초로 일어나는 시간을 다루는 Random Variable입니다. ($k=1$ special case)

$$P(X = n) = P(T_1 = n) = p (1-p)^{n-1}$$

*Expectation*을 유도하는 과정은 다음과 같습니다.

$$
\begin{aligned}
E(X) &= \sum_{i=0}^{\infty} i p (1-p)^{i-1} = \frac{p}{1-p} \sum_{i=1}^{\infty} i (1-p)^{i} \\
&= \frac{p}{1-p} \biggl( (1-p) + 2 (1-p)^2 + 3 (1-p)^3 + \cdots \biggr) \\
\frac{1}{1-p} E(X) &= \frac{p}{1-p} \biggl( 1 + 2 (1-p) + 3 (1-p)^2 + \cdots \biggr) \\
\frac{-p}{1-p} E(X) &= \frac{p}{1-p} \biggl( -1 - (1-p) - (1-p)^2 - \cdots \biggr) \\
E(X) &= \sum_{j=0}^{\infty} (1-p)^j = \frac{1}{p}
\end{aligned}
$$

Princeton 교재에서는 calculus trick을 쓰네요. 

$$E(X) = \sum_{n=1}^{\infty} np(1-p)^{n-1} = p \frac{d}{dq} \sum_{n=1}^{\infty} q^n = p \frac{d}{dq} \frac{q}{1-q} = \frac{p}{(1-q)^2} = \frac{1}{p}$$

- *Geometric Random Variable*을 다르게 쓰면, 첫 성공이 나오기까지 Bernoulli Trial을 실행하는 횟수입니다. (실패하는 횟수로 생각할 수도 있는데, 이 경우 $P(X)$와 $E(X)$값이 살짝 달라집니다.)
- Bernoulli Process에서 임의의 두 success 사이의 간격은 서로 independent하며, 더 나아가 이 간격은 Geometric Distribution을 따릅니다!
  - 여기서 말하는 임의의 두 success 사이의 간격은 $T_k - T_{k-1}$ 입니다. ($k \ge 2$)

**Law of Large Numbers**: *Let $A$ be event, $A_i$ be individual trial for $A$, and $S_n = \sum_{k=1}^{n} 1_{A_k}$, then $\lim_{n \rightarrow \infty} \frac{S_n}{n} = P(A)$.*

- 한글로 요약하면, 독립시행 횟수가 늘어날수록 어떤 Event $A$가 일어나는 통계적 확률이 수학적 확률에 수렴한다는 것입니다.
- 좀 더 [formal](https://en.wikipedia.org/wiki/Law_of_large_numbers)하게 살펴보면, *LLN*에는 *Weak law*와 *Strong law*가 있습니다.
  - *Let $\overline{X}_{n} = \frac{1}{n} \sum_{i=1}^{n} X_i$ where $X_i$ are independent and identically distributed random variables.*
  - **Weak Law**: $\forall_{\epsilon > 0} \lim_{n \rightarrow \infty} P(\|\overline{X}_{n} - E(X)\| < \epsilon) = 1$
  - **Strong Law**: $P(\lim_{n \rightarrow \infty} \overline{X}_{n} = E(X)) = 1$
  - Strong Law가 Weak Law보다 훨씬 증명하기 어렵다네요. Strong Law와 Weak Law의 차이는, Weak Law는 $\|\overline{X}_{n} - E(X)\| > \epsilon$이 무수히 많이 일어날 가능성이 있는데, Strong Law에서는 이걸 원천적으로 차단한다고 합니다.
  - $Var(X)$가 finite하다고 가정한 상황에서는 *Chebyshev's Inequality*를 이용해서 [weak law를 비교적 쉽게 증명](https://en.wikipedia.org/wiki/Law_of_large_numbers#Proof_using_Chebyshev's_inequality_assuming_finite_variance)할 수 있습니다!

**Variance**: *$Var(X) = E((X - E(X))^2)$.*

*Variance*가 비교적 늦게 소개되었네요. Princeton 교재에서는 Variance가 높을수록 $X$가 *"more random"*하다고 표현합니다. 다음은 *Variance*의 특성입니다.

- $Var(X) \ge 0$
- $Var(X) = 0 \iff \exists_a P(X = a) = 1$
- $Var(X) = E(X^2 - 2XE(X) + E(X)^2) = E(X^2) - 2E(X)^2 + E(X)^2 = E(X^2) - E(X)^2$
- $X \bot Y \implies Var(X+Y) = Var(X) + Var(Y)$
- $Var(aX) = E(a^2 X^2) - E(aX)^2 = a^2 Var(X)$

**Poisson Random Variable**: A random variable $Z$ which has distribution $P(Z = k) = \frac{e^{-\mu} \mu^k}{k!}$ ($Z \sim Pois(\lambda)$).

*Poisson Random Variable*의 motivation은 Binomial에서 $n \rightarrow \infty$, $p \rightarrow 0$, $np \rightarrow \lambda$로 시작합니다.

$$
\begin{aligned}
P(X = k) &= \lim_{n \rightarrow \infty, p = \lambda/n} P(S_n = k) = \lim_{n \rightarrow \infty} \binom{n}{k} (\frac{\lambda}{n})^k (1-\frac{\lambda}{n})^{n-k} \\
&= \lim_{n \rightarrow \infty} \frac{\lambda^k}{k!} \frac{n!}{(n-k)! n^k} (1 - \frac{\lambda}{n})^n (1 - \frac{\lambda}{n})^{-k} \\
&= \frac{\lambda^k}{k!} \cdot 1 \cdot e^{-\lambda} \cdot 1 = \frac{\lambda^k}{k!} e^{-\lambda}
\end{aligned}
$$

즉, Poisson Random Variable $X$에 대해, $P(X = k)$는 단위시간 혹은 단위공간 내의 이벤트가 $k$번 발생할 확률입니다.

$$
E(X) = \sum_{k=0}^{\infty} k \frac{\lambda^k}{k!} e^{-\lambda}
= \lambda \sum_{k=1}^{\infty} \frac{\lambda^{k-1}}{(k-1)!} e^{-\lambda} = \lambda \sum_{k=1}^{\infty} P(X=k-1) = \lambda
$$

$Var(X)$는 $np \rightarrow \lambda, p \rightarrow 0$를 감안하면 $\lambda$로 수렴할 것 같다라는 것을 직관적으로 생각할 수 있는데요. 실제로도 그럽니다.

$$
\begin{aligned}
Var(X) &= \sum_{k=0}^{\infty} k^2 \frac{\lambda^k}{k!} e^{-\lambda} - \lambda^2 \\
&= \lambda e^{-\lambda} + \sum_{k=2}^{\infty} \biggl( k(k-1) \frac{\lambda^k}{k!} e^{-\lambda} + k \frac{\lambda^k}{k!} e^{-\lambda} \biggr) - \lambda^2 \\
&= \lambda e^{-\lambda} + \lambda^2 \sum_{k=2}^{\infty} \frac{\lambda^{k-2}}{(k-2)!} e^{-\lambda} + \sum_{k=2}^{\infty} k \frac{\lambda^k}{k!} e^{-\lambda} - \lambda^2 \\
&= \lambda^2 \sum_{k=2}^{\infty} P(X=k-2) + \sum_{k=0}^{\infty} k \frac{\lambda^k}{k!} e^{-\lambda} - \lambda^2 \\
&= E(X) = \lambda
\end{aligned}
$$

**Gamma Random Variable**: *A random variable $T$ which has $P(T \le t) = 1 - \sum_{i=0}^{k-1} \frac{e^{-\lambda t}(\lambda t)^i}{i!}$ ($T \sim Gamma(k, \lambda)$)*

먼저 motivation을 들어봅시다.

- *단위시간 당 평균적으로 $\lambda$번 발생하는 이벤트가 있습니다. $k$번째 이벤트가 시간 $t$ 이전에 발생할 확률은 얼마일까요?*

$k$번째 이벤트가 시간 $t$ 이전에 발생할 확률은, *$t$ 시간 당 평균적으로 $t \lambda$번 발생하는 이벤트가 $k$번 이상 발생할 확률을 의미합니다.*

$$
\begin{aligned}
P(T_k \le t) &= P(Z \ge k; t \lambda) = 1 - P(Z < k; t \lambda) \\
&= 1 - \sum_{i=0}^{k-1} \frac{(t\lambda)^i}{i!} e^{-t \lambda}
\end{aligned}
$$

$P(T_k = t)$는 *Gamma Function*을 사용하여 나타내어질 수 있는데, 프린스턴 교재에 해당 내용이 나오면 짚고 넘어가고, 아니면 스킵하겠습니다.

**Exponential Random Variable**: *Special case when $k=1$ of Gamma Random Variable. $P(T_1 \le t) = 1 - e^{-\lambda t}$ ($T_1 \sim Expon(\lambda)$).*

Exponential Random Variable은 Gamma Random Variable의 $k=1$ 특수 케이스로, *단위시간 당 평균적으로 $\lambda$번 발생하는 이벤트가 최초로 발생하는 시간*에 대해 다루는 Random Variable입니다.

---

이상으로, Bernoulli Process와 관련된 여러 Random Variable들을 훑어보았습니다. 다음 챕터에서는 Continuous Random Variable에 대해 본격적으로 다뤄보도록 하겠습니다. 감사합니다.