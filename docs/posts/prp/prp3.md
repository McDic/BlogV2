---
categories:
  - Probability and Random Process
tags:
  - math
  - probability
  - statistics
title: PRP 3. Continuous Random Variables
slug: prp-3
---

!!! migrated

    *This article is migrated from which I wrote on my old blog.*

안녕하세요. 이 시리즈의 지난 article에서 *Bernoulli Processes*에 대해 다뤄봤는데요. 이번에는 *Chapter 3. Continuous Random Variables*에 대해 다뤄보겠습니다. 이번 Chapter의 목표는 Chapter 1에서 배웠던 basic principle들을 Continuous Random Variable로 확장하는 것입니다.

<!-- more -->
---

# Chapter 3. Continuous Random Variables

**Expectation in Continuous R.V.**: *$E(g(X)) = \lim_{|x_{i+1} - x_i| \rightarrow 0} \sum_{i} g(x_i) P(x_i < X \le x_{i+1}) = \int g(x) P(X=x) dx$*

Princeton 교재에서는 Expectation을 히스토그램의 가로 크기가 0을 향해 가는 걸로 설명하네요.

**Probability Density Function (PDF), Cumulative Distribution Function (CDF)**: The function *$F(x) = P(X \le x)$ is CDF of random variable $X$, and the function $\frac{dF(x)}{dx}$ is PDF of random variable $X$.*

위 Expectation의 정의에 $F(x)$를 끼워넣으면 다음과 같습니다.

$$
\begin{aligned}
E(g(X)) &= \lim_{|x_{i+1} - x_i| \rightarrow 0} \sum_{i} g(x_i) P(x_i < X \le x_{i+1}) \\
&= \lim_{|x_{i+1} - x_i| \rightarrow 0} \sum_{i} g(x_i) (F(x_{i+1}) - F(x_i)) \\
&= \int g(x) \frac{dF(x)}{dx} dx
\end{aligned}
$$

그래서 $\frac{dF(x)}{dx} = P(X = x)$가 되고, 이때 $f(x) = \frac{dF(x)}{dx}$를 $X$의 *PDF*라고 정의합니다.

또 CDF, PDF에 관한 몇 가지 성질을 쓰면..

- PDF는 항상 0 이상이므로, CDF는 *increasing function*입니다.
- $F(-\infty) = \int_{-\infty}^{\infty} f(x) dx = 0, F(\infty) = \int_{-\infty}^{\infty} f(x) dx = E(1) = 1$
- $P(y < X \le z) = P(X \le z) - P(X \le y) = \int_{y}^{z} f(x) dx$

다음은 PDF, CDF의 example입니다.

- *Gamma Distribution*:

$$P(X \le x) = 1 - \sum_{i=0}^{k-1} \frac{e^{-\lambda x} (\lambda x)^i}{i!}$$

$$
\begin{aligned}
\frac{d}{dx} P(X \le x) &= \frac{d}{dx} (1 - \sum_{i=0}^{k-1} \frac{1}{i!} e^{-\lambda x} \lambda^i x^i) \\
&= \sum_{i=0}^{k-1} \frac{1}{i!} (\lambda e^{-\lambda x} \lambda^i x^i - e^{-\lambda x} \lambda^i x^{i-1} i) \\
&= e^{-\lambda x} \sum_{i=1}^{k-1} \biggl( \frac{\lambda^{i+1} x^i}{i!} - \frac{\lambda^i x^{i-1}}{(i-1)!} \biggr) + \lambda e^{-\lambda x} \\
&= \frac{e^{-\lambda x} \lambda^{k} x^{k-1}}{(k-1)!}
\end{aligned}
$$

$$
\begin{aligned}
E(X) &= \int_{0}^{\infty} x f(x) dx \\
&= \int_{0}^{\infty} \frac{e^{-\lambda x} \lambda^k x^k}{(k-1)!} dx \\
&= \frac{k}{\lambda} \int_{0}^{\infty} \frac{e^{-\lambda x} \lambda^{k+1} x^{k}}{k!} dx \\
&= \frac{k}{\lambda} P(0 \le Y < \infty) \text{ } (Y \sim Gamma(k+1, \lambda))\\
&= \frac{k}{\lambda}
\end{aligned}
$$

$$
\begin{aligned}
Var(X) &= \int_{0}^{\infty} x^2 f(x) dx - E(X)^2 \\
&= \int_{0}^{\infty} \frac{e^{-\lambda x} \lambda^k x^{k+1}}{(k-1)!} dx - \frac{k^2}{\lambda^2}\\
&= \frac{k(k+1)}{\lambda^2} \int_{0}^{\infty} \frac{e^{-\lambda x} \lambda^{k+2} x^{k+1}}{(k+1)!} dx - \frac{k^2}{\lambda^2} \\
&= \frac{k(k+1)}{\lambda^2} P(0 \le Y < \infty) - \frac{k^2}{\lambda^2} \text{ } (Y \sim Gamma(k+2, \lambda)) \\
&= \frac{k}{\lambda^2}
\end{aligned}
$$

- *Exponential Distribution*: Exponential Distribution은 Gamma Distribution의 $k=1$ special case이므로, PDF는 $f(x) = \lambda e^{-\lambda x}$, $E(X) = \frac{1}{\lambda}$, $Var(X) = \frac{1}{\lambda^2}$ 입니다.

**Joint Density**: *The function $f(x, y) = \frac{\partial^2}{\partial x \partial y} P(X \le x, Y \le y)$.*

**Joint Expectation for Continuous R.V.**: *$E(g(X, Y)) = \iint g(x, y) f(x, y) dx dy$.*

**Marginal Density**: *Let $f$ be joint density, then $f_X(x) = \int f(x, y) dy$.*

Marginal Density를 활용하여 Linearity of Expectation을 Continuous Random Variable에서도 증명할 수 있습니다.

$$
\begin{aligned}
E(X+Y) &= \int (x+y) f(x, y) dx dy \\
&= \int x f(x, y) dx dy + \int y f(x, y) dx dy \\
&= E(X) + E(Y)
\end{aligned}
$$

**Conditional Distribution for Continuous R.V.**: *$f_{X | Y}(x | y) = \frac{f_{X,Y}(x, y)}{f_Y(y)}$.*

**Conditional Expectation for Continuous r.V.**: *$E(g(X) | Y=y) = \int g(x) f_{X | Y}(x | y) dx$, where $f(x | y)$ is conditional density.*

**Marginal Expectation**: *$E(g(X)) = \int E(g(X) | Y=y) f_Y(y) dy$.*

다음은 예제입니다.

- *어떤 가게가 있습니다. 이 가게는 시간당 $\lambda$명의 손님이 이용합니다. 당신은 이 가게에 첫 번째 손님이 도착하는 시간($=x$)을 확인한 후, 이 가게를 시간당 $\frac{1}{x}$번 방문하기로 합니다. 당신이 이 가게를 처음 방문하기까지 걸리는 시간의 Expectation은 얼마일까요?*

Chapter 2에서도 간단하게 설명드렸지만, 단위 시간당 $\lambda$번 발생하는 이벤트의 첫 발생 시간은 *Exponential Distribution*을 따릅니다. 또한, 당신이 이 가게를 처음 방문하는 시간의 random variable을 $Y$라고 하면, $Y | X=x$ 또한 *Exponential Distribution*을 따릅니다!

$$
\begin{aligned}
E(Y | X=x) &= \int y f_{Y | X}(y | x) dy \\
&= \int_{0}^{\infty} y \frac{1}{x} e^{-\frac{y}{x}} dy \\
&= \frac{1}{x} \int_{0}^{\infty} y e^{-\frac{y}{x}} dy \\
&= \frac{1}{x} \biggl( \Bigl[ y e^{-\frac{y}{x}} (-x) \Bigr]_{0}^{\infty} - \int_{0}^{\infty} -x e^{-\frac{y}{x}} dy \biggr) \\
&= \int_{0}^{\infty} e^{-\frac{y}{x}} dy = x
\\
E(Y) &= \int E(Y | X=x) f_X(x) dx \\
&= \int_{0}^{\infty} x \lambda e^{-\lambda x} dx \\
&= \int_{0}^{\infty} t e^{-t} dt \frac{dx}{dt} \text{ } (t = \lambda x) \\
&= \frac{1}{\lambda} \int_{0}^{\infty} t e^{-t} dt = \frac{1}{\lambda}
\end{aligned}
$$

하지만, $Y$는 Exponential Distribution이 아닙니다. 그 이유는 *Marginal Density*를 구해보면 나옵니다.

$$
f_{X, Y}(x, y) = f_{Y|X}(y|x) f_X(x) = \lambda e^{-\lambda x} \frac{1}{x} e^{-\frac{y}{x}} \\
f_{Y}(y) = \int_{0}^{\infty} f_{X, Y}(x, y) dx = \int_{0}^{\infty} \frac{\lambda}{x} e^{-\lambda x - \frac{y}{x}} dx
$$

또 다른 예제를 살펴볼까요?

- *3명이서 게임을 진행합니다. 1번째 사람이 random number $X \sim Expon(\lambda)$를 만들고, 2번째 사람이 $Y \sim Expon(x)$를 만듭니다. 3번째 사람은 $y$가 주어졌을 때 $x$를 추측해내야 합니다. 어떤 값이 합리적일까요?*

먼저 $f_X(x) = \lambda e^{-\lambda x}, f_{Y|X}(y|x) = x e^{-xy}$ 입니다. 따라서

$$f_{X,Y}(x, y) = f_{Y|X}(y|x) f_X(x) = \lambda x e^{-x(\lambda + y)}$$

$$
\begin{aligned}
f_Y(y) &= \int_{0}^{\infty} f_{X,Y}(x, y) dx = \int_{0}^{\infty} \lambda x e^{-x(\lambda + y)} dx \\
&= \lambda \Bigl[ \frac{1}{-(\lambda + y)} x e^{-x(\lambda + y)} - \frac{1}{(\lambda + y)^2} e^{-x(\lambda + y)} \Bigr]_{0}^{\infty} \\
&= \frac{\lambda}{(\lambda + y)^2}
\end{aligned}
$$

$$
f_{X|Y}(x|y) = \frac{f_{X,Y}(x, y)}{f_Y(y)} = (\lambda + y)^2 x e^{-x(\lambda + y)}
$$

그런데, $f_{X|Y}(x|y)$는 $Gamma(2, \lambda + y)$의 PDF와 동일합니다. 따라서 $E(X|Y=y) = \frac{2}{\lambda + y}$ 입니다! (직접 적분 $\int_{0}^{\infty} (\lambda + y)^2 x^2 e^{-x(\lambda + y)} dx$을 [wolfram alpha](https://www.wolframalpha.com/input/?i=integrate+%28a%2By%29%5E2+x%5E2+e%5E%28-x%28a%2By%29%29+dx+from+0+to+inf)를 통해서 해본 결과, 답이 같았습니다.)

**Independence in Continuous R.V.**: Random variables $X, Y$ are independent if $f_{X|Y}(x|y) = f_X(x)$.

이걸 또 다르게 해석하면, discrete random variables와 마찬가지로 $f_{X,Y}(x, y) = f_X(x) f_Y(y)$ 가 나옵니다.

예제를 살펴보겠습니다. (이 예제는 아직 명확하게 이해하지는 못했는데, 더 자세하게 이해하는 대로 보충 설명을 써넣겠습니다.)

- *버스 정류장에 평균적으로 시간당 $\lambda$명이 도착하고, 시간당 $v$대의 버스가 도착합니다. 사람들의 수와 버스의 수가 independent할 때, 첫 버스에 탑승하는 사람의 수의 Expectation은 얼마일까요?*

$T$를 첫 버스가 도착하는 시간, $N_t$를 $t$ 시간에 버스정류장에서 기다리고 있는 사람의 수, 그리고 $N_T$를 버스가 도착한 당시 버스정류장에서 기다리고 있는 사람의 수라고 해봅시다. 그러면 $T \sim Expon(v), N_t \sim Pois(\lambda t)$입니다.

$$E(N_T | T=t) = E(N_t | T=t) = E(N_t) = \lambda t$$

$$
\begin{aligned}
E(N_T) &= \int E(N_T | T=t) f_T(t) dt = \int \lambda t f_T(t) dt \\
&= \lambda \int t f_T(t) dt = \lambda E(T) = \frac{\lambda}{v}
\end{aligned}
$$

---

지금까지 Continuous Random Variables에 대해 다뤄봤습니다. 점점 난이도가 올라가네요. 다음 챕터에서는 Lifetimes와 Reliability에 대해 다뤄보도록 하겠습니다. 감사합니다.
