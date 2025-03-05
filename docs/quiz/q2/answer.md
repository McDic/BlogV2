---
title: QUIZ 2. 4 Plane Dividers
---

First, the maximum number of areas you can separate with $3$ planes are $8$, by placing all planes orthogonally.

![three_planes](/assets/quizzes/q2/three_planes.png)

!!! caption

    Modeling provided by [figuro.io](https://figuro.io/Designer)

Note that the entire topology is not different even if you tweak some angles unless you place two planes in parallel, as shown below.

![three_planes](/assets/quizzes/q2/three_planes_tweaked.png)

However you cannot put $4$ planes in $3$-dimensional space orthogonally.
(This can be proved by linear algebra.)
So now your goal is how to add one more plane to divide these $8$ already separated areas as much as you can.

This might be non-intuitive at the first.
Now let me give two very strong observations.

1. If the new cube passes $n$ of the $8$ areas, the number of new areas will be $2n + (8-n) = n+8$.
2. The maximum possible $n$ is $7$.

Why the first observation is correct?
Because any plane would divide any convex area into $2$ areas, and all of $8$ already separated areas are convex.

Why the second observation is correct?
If the new plane is able to divide all of $8$ areas, then this means you can pick up $8$ points from the plane, where each point has positive/negative x/y/z coordinate.

Any convex space that contains these $8$ points essentially create $3$ dimensional space.
Because if you put any $3$ different points to create a plane, there should be a completely opposite sign triples that can't be included on that created plane.
I believe there is a mathematically strict proof using dot product(which defines a plane in multi-dimensional space) or matrix dimension, but I am not covering that here.

However, dividing $7$ areas is possible, as shown below.

![four_planes](/assets/quizzes/q2/four_planes.png)

Therefore, the answer is $15$.
Generalizing this, I believe the answer for $n$-dimensional space with $n+1$ of $(n-1)$-dimensional hyperplanes are $2^{n+1} - 1$.
