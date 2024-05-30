---
categories:
  - Algorithm and Data Structures
tags:
  - algorithm
  - data-structures
  - computer-science
date:
  original: 2023-09-24
title: ALDS 2. Some Bad CP Code Practices
---

[ICPC 2020 Seoul Regional](https://icpckorea.org/2020-seoul/regional)에서 수상하고 [CF Round 633](https://codeforces.com/blog/entry/75806)을 주최한 이후,
저는 알고리즘 문제를 거의 풀지 않게 되었습니다.
이후로 퀀트업계에 종사하면서 이런저런 코딩을 많이 하게 되었는데, 그 과정에서 이런저런 개발을 하게 되었습니다.
이번에는 알고리즘 대회나 코딩테스트 등에서 나타나는 안 좋은 코드 습관들에 대해 얘기해보고자 합니다.
그 전에, 이 글이 타겟팅하는 독자는 다음과 같습니다.

1. 개발을 직업으로 하고 싶은 사람
2. 알고리즘 문제풀이와 개발 사이에서 코드 스타일이나 컨벤션, 마인드셋 등을 크게 바꾸고 싶지 않은 사람

당신이 알고리즘 문제를 푸는데 작성하는 코드가 더러워다고 상관없다고 생각하는 사람이라면, 저는 그 생각에 별로 관여하고 싶지 않으며 그 생각을 존중합니다.
당신이 그런 코딩 스타일을 실제 세계에서 똑같이 해도 문제가 없다고 생각하지만 않는다면요.

그럼 이제 본격적으로 알아봅시다.

!!! references

    이 글은 [nor의 덧글](https://codeforces.com/blog/entry/120716?#comment-1070923)을 통해 내용이 보강되었습니다.

<!-- more -->
---

## `using namespace std;`

`bits/stdc++.h` 같은 파일을 include한 뒤 `using namespace std;`를 하면 무슨 일이 일어날까요?
엄청나게 많은 양의 함수, 클래스, const 변수들 등 아주 많은 이름이 global namespace에 로드될 것입니다.

![using_namespace](/assets/posts/alds/bad_practices/using_namespace_std.png)

!!! caption

    Intellisense가 global namespace에 로드된 수많은 identifier들을 보여줍니다.

`using namespace std`를 하는 사람들의 심리는 단순합니다.
`std::`라는 5글자를 치기가 싫은 거죠.
이렇게 5글자를 타입을 사용할 때 덜 치는 것이 `using namespace std`를 통해 얻을 수 있는 오직 유일한 장점입니다.
그리고 단점은 `std` namespace에 정의된 어떤 변수나 함수와 같은 이름의 무언가를 global에서 정의할 수 없다는 것입니다.

만약 자주 사용하는 어떤 타입이나 함수에 대한 alias를 만들고 싶다면, `using`, `typedef`, 혹은 [function pointer](https://stackoverflow.com/questions/35654908/explanation-of-function-pointers)를 사용하세요.

---

## Abusing macros

알고리즘 대회에 참가하는 사람들로부터 볼 수 있는 가장 큰 특징은 바로 매크로를 비정상적으로 악용하는 것입니다.
다음과 같은 C++ 코드를 상상해봅시다.

```cpp
#include <algorithm>
#include <vector>
#include <utility>

#define f1 first
#define f2 second

#define N 100005

#define all(x) x.begin(),x.end()

int main(void)
{
    std::pair<int, double> x;
    auto x1 = x.f1;
    auto x2 = x.f2;

    int array[N];

    std::vector<int> wow = {1, 5, 2, 6};
    std::sort(all(wow));
}
```

### Overriding methods or properties

이런 걸 왜 하는지 모르겠습니다.
VSCode, CLion 같은 현대 IDE에서는 이러한 변수, 타입, 매크로 등을 자동완성시켜주는 intellisense가 준비되어 있습니다.

저는 심지어 `#define int long long` 같은 매크로도 많이 봤습니다.
이런 식으로 primitive keyword를 아예 대체해버리는 매크로는 굉장히 위험하고 지양해야 합니다.

### Defining constants

매크로로 상수를 정의하는 것은 굉장히 낡은 방식입니다.
Modern C++에서 상수를 정의하고 싶으면 `constexpr`을 사용하는 것이 더 좋습니다.
매크로는 코드 상에서 string substitution을 진행하는 pre-processing에 관여하는 것에 불과하며,
이는 가끔씩 의도치 않은 컴파일 에러나 로직 에러를 불러오는 결과가 됩니다.

```cpp
#include <iostream>

#define triple(x) x * 3

int main(void)
{
    // THIS OUTPUTS 8 = 5 + 1 * 3
    std::cout << triple(5 + 1) << std::endl;
}
```

![constexpr](/assets/posts/alds/bad_practices/constexpr.png)

!!! caption

    이 그림의 코드에서 `fib(20)`은 런타임에 계산되지 않으며, 컴파일 타임에 계산됩니다.
    VSCode가 intellisense로 `x`의 값을 미리 알려주는 것도 동일한 맥락입니다.

### Abused grammars

`all(x)`는 `x.begin(),x.end()`로 치환되는데, 이것은 코드 상에서 `all(x)`가 사용되는 부분이 실제 전처리 이후에는 완전히 다른 형태의 AST를 생성할 문법을 사용하고 있음을 암시적으로 나타냅니다.
이것은 중대한 버그의 원인이 되며 매우 지양해야 할 방식입니다.

---

## Using internal functions or features

C++는 컴파일러가 여러 개이고, 그 중에서 특히 gcc는 [builtins](https://gcc.gnu.org/onlinedocs/gcc/Other-Builtins.html)처럼 gcc 특화된 기능을 여러가지 제공하고 있습니다.
심지어 현업에서조차 gcc 같은 특정 컴파일러의 특정 버젼에서만 작동하는 기능을 이용해서 성능을 부스트하는 경우도 존재하긴 합니다만, 일반적인 대부분의 경우에서는 그렇게 하지 않습니다.
Dependency 관리가 너무 빡세기 때문입니다.

실제로 C++ 알고리즘 코드들을 보면 gcc에서만 동작하는 코드들이 매우 많습니다.
심지어 어떤 코드들은 특정 버젼의 gcc에서만 동작하기도 합니다.

---

## Not using [`std::array`](https://en.cppreference.com/w/cpp/container/array), [`std::string`](https://en.cppreference.com/w/cpp/string/basic_string) instead of raw arrays

그냥 배열은 단순한 copy가 불가능하고, 포인터와 관련해서 메모리 이슈도 있습니다.
`std::array`, `std::string`은 그러한 쌩배열의 훌륭한 대체제입니다.

---

## Using variable length arrays instead of [`std::vector`](https://en.cppreference.com/w/cpp/container/vector)

다음 코드와 같이 배열의 길이를 변수 기반으로 생성하는 것은 C++ 표준이 아닙니다.
gcc 같은 일부 컴파일러에서만 지원되며, 이러한 것들을 잘못 사용했다가는 각종 난해한 버그의 원인이 됩니다.

```cpp
#include <iostream>

int main() {
    int n;
    std::cin >> n;
    int array[n];
}
```

---

## Not using aggregate initialization/constructors

복잡한 구조체의 경우, [aggregated initialization](https://en.cppreference.com/w/cpp/language/aggregate_initialization)을 하지 않으면 가끔 특정 member를 초기화하는 것을 까먹을 때가 있습니다.

```cpp
// Used aggregate initialization
struct Wow1 {
    Wow1(int a, int b, int c, int d, int e, int f): a(a), b(b), c(c), d(d), e(e), f(f) {};
    int a, b, c, d, e, f;
};

// Initializing each member individually
struct Wow2 {
    Wow2(int a, int b, int c, int d, int e, int f) {
        this->a = a;
        this->b = b;
        this->c = c;
        this->d = d;
        this->e = e;
        this->f = f;
    }
    int a, b, c, d, e, f;
};
```

---

## Implementing everything under single function

모든 것들을 단 하나의 함수 아래에서 구현하는 것은 지옥의 디버깅을 불러옵니다.
프로그램의 복잡도가 늘어나면 이 문제는 크게 대두됩니다.

---

이상으로 알고리즘 대회에 사용되는 많은 코드들에서 쓰이는 여러 특징들에 대해 알아보았습니다.
저도 알고리즘 많이 할 때는 별로 신경 안 쓴 것들이 많았지만,
요즘은 뭐든 코딩할 때 신경을 많이 쓰는 편입니다.
글을 읽어주셔서 감사합니다.
