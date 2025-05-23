---
categories:
  - Algorithm and Data Structures
tags:
  - math
  - algorithm
  - career
moved_from:
  - THO-9
title: ALDS 3. About Ad-hoc Problems
---

[애드혹 문제](https://usaco.guide/bronze/ad-hoc?lang=cpp)란, 일반적인 방법으로 잘 풀리지 않고 참신한 방식으로 접근해야 풀릴 수 있는 부류의 문제를 말합니다.
좋은 애드혹 문제는 푸는 것은 물론이고 만드는 것 또한 매우 어렵습니다.
이번 게시글에서는 애드혹 문제들에 대한 저의 생각을 써보고자 합니다.

<!-- more -->

---

## Ad-hoc is a time-dependent variable

시간이 경과할수록 사람들의 집단이 가지고 있는 지식의 양은 현저하게 늘어나고 있습니다.
그 결과, 어떤 시대에 그 문제가 애드혹이었다고 하더라도, 시간이 지나면서 해당 문제 혹은 그 풀이에 사용된 논리적 테크닉이 많은 사람들에 의해 다뤄지게 되면서, 해당 아이디어는 더 이상 애드혹이 아니게 되기도 합니다.

알고리즘을 좀만 공부했다면 누구나 아는 Dijkstra가 개발한, non-positive cycle이 없는 weighted graph 상에서 [최단거리를 구하는 알고리즘](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)은, "당시 기준"으로 새로운 부류의 테크닉이었습니다.

비교적 최근의 알고리즘 분야 애드혹의 대표적인 예시는 [IOI 2016 "Ailens" 문제에 출제된 테크닉](https://medium.com/@bluezebragames/dynamic-programming-optimization-the-aliens-trick-9138176287cf)일 것입니다.
이 문제에서 사용된 테크닉은 알고리즘 고수들에게 두고두고 회자되면서 굉장히 유명해졌습니다.
대놓고 "Ailens Trick"이라고 부를 정도입니다.
하지만.. 2044년쯤에는 Ailens Trick의 상대적인 난이도가 지금으로 치면 기초적인 세그먼트 트리 수준까지 내려오지 않을까요?

이런 식으로 "애드혹"이라는 수식이 붙는 기준은 고정적이지 않고, 시대에 따라 사람들의 컨센서스가 바뀜에 따라 변화합니다.
심지어 같은 시대의 사람들 사이에서도 각자의 지식에 따라 "애드혹"이라는 기준이 다릅니다.
이것은 "애드혹"이라는 키워드가 주관적인 의견이 개입될 여지가 많다는 것을 시사합니다.

---

## Is ad-hoc trainable?

애드혹 문제들은 훈련이 가능한 영역에 있을까요?
결론부터 말씀드리면, 사람에 따라 그 훈련 가능한 영역의 범위 및 속도가 다르겠지만, 저는 "YES"라고 생각합니다.

위에서 말씀드린대로 애드혹 문제들은 문제마다 속도가 다를 뿐, 시간이 지남에 따라 점점 더 많은 사람들에 의해 다뤄지게 되고, "애드혹"이 아니게 됩니다.
그러한 새로운 유형의 문제들도 점점 formal하게 접근할 수 있는 방법론이 생기게 되고, 그런 식으로 훈련을 할 여지가 생기게 된다고 생각합니다.

물론 개인에 따라 훈련의 속도가 많이 다를 수 있습니다.
어떤 사람들은 매우 뛰어나서 자기가 직접 그런 formal approach들을 발굴하기도 하고, 어떤 사람들은 그런 방법론들을 빠르게 따라갈 수 있을 것입니다.
하지만 모든 사람들이 그렇진 않겠죠. 매우 느린 시간이 지나서야 그것들을 비로소 이해하는 케이스도 있을 것입니다.

난이도가 아주 높은 문제의 경우, 어떤 사람들은 그런 문제를 푸는 해답을 평생 이해할 일이 없을지도 모릅니다.
하지만 대부분의 사람들에게 있어 현실세계에서 그 정도로 뇌를 쥐어짜는 논리적 접근이 필요한 문제가 나올 일은 거의 없을 것입니다.

### Four square problem

제가 홍콩에 가서 만난 알고리즘 고수 친구들이 2명 있었는데, 이 친구들하고 "Four Square Problem"을 겨뤄본 적이 있었습니다.
이 문제는 자릿수가 4개인 자연수가 주어졌을 때, 해당 수를 자연수 4개의 제곱의 합, 즉 $s = a^2 + b^2 + c^2 + d^2$ 꼴로 풀어내는 문제였습니다.
예를 들어, $2622 = 40^2 + 30^2 + 11^2 + 1^2$ 이런 식으로요.

2명의 친구 중 1명은 자기가 편하게 암산할 수 있는 알고리즘을 직접 개발해서 엄청나게 빠른 속도로 문제를 풀었습니다.
제가 1~2문제 풀 동안 10문제 이상 풀었던 걸로 기억합니다.

이러한 문제를 빨리 푸는 유형은 어려운 암산을 무식하게 뚫어낼 수 있는 타고난 뇌지컬을 가지고 있거나, 아니면 여러가지 불필요한 연산을 줄일 수 있는 암산 테크닉들을 유연하게 적용시킬 수 있는 지능이 필요할 것입니다.
(물론 제가 만난 두 명은 둘 다 가지고 있었습니다.)

이런 문제를 가지고 실제로 겨뤄보니 확실히 뇌지컬이라는 게 사람마다 다르다는 느낌을 받긴 했습니다.
특히 저런 문제들에 집중해서 자기만의 알고리즘을 개발해내고, 또 연산력을 소모하는 행위를 즐기는 사람들이 있다는 것은.. 분명히 일반적인 영역이 아니라고 생각합니다.

---

## Is ad-hoc useful in real life?

실제로 퀀트 회사의 리서치 직무에서는 이런 부류의 수학적 애드혹 문제를 물어보는 경우가 종종 있다고 합니다.
Jane Street Interview 이런 거 구글링해보면 비슷한 부류의 질문이 금방 나옵니다.
그런데, 이런 애드혹 테크닉들이 실제로 직업을 구하는 데 도움이 되는지, 혹은 실무적으로도 도움이 될까요?

저는 애드혹 테크닉 자체는 도움이 크게 되지는 않지만, 그런 애드혹 테크닉들을 거부감 없이 빠르게 받아들여서 활용할 수 있는 "지능"은 일자리를 구하는 거든, 실무적으로든 도움이 된다고 생각합니다.

실제로 세상에는 논리적으로 생각하는 것 자체를 싫어하는 사람이 있고, 숫자들만 봐도 어지러워하는 사람도 있습니다.
그런 사람의 수가 적은 것도 아니고 되게 많습니다.
특히 개발이나 퀀트 업계에서는 그런 사람들보다는 숫자에 거부감이 없는 사람들이 더 유용하지 않을까요?

---

글 읽어주셔서 감사합니다. 좋은 하루 보내세요.
