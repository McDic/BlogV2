---
title: QUIZ 3. Cool Quadratics
---

There is a very important fact to solve this.
**You can create up to $2$ intersections between two cool quadratics,**
because subtraction of two quadratics is also a polynomial with max degree $2$,
therefore there should be at max $2$ intersections between two cool quadratics.

Now let's use mathematical induction approach for this.
Suppose you already drawn $n-1$ cool quadratics on the plane.
And you are going to draw new cool quadratics on the plane,
then you can make up to $2n-2$ intersections on the plane.

Essentially, there should be $2n-1$ newly created areas by new line, regardless of which intersections they create(unless there are duplicated intersections),
because each line segment (either between two intersection or open-ended) will create $1$ new area.

![three_convex](/assets/quizzes/q3/three_convex_lines.png)

!!! caption

    The third cool quadratic(green line) is added to the example from the question page.
    It makes $4$ new intersections and create $5$ new areas.

    !!! formula

        The green line is drawn by $f(x) = -(5x-9)^2 + 8$, which is also a cool quadratic.

Therefore, if answer is $a_n$ for $n$ cool quadratics, then $a_n = a_{n-1} + 2n-1$ and $a_1 = 2$, which means

$$a_n = 1 + \sum_{i=1}^{n} (2i-1) = 1 + n(n+1) - n = n^2 + 1$$
