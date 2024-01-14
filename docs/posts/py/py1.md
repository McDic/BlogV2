---
date: 2022-06-28
categories:
  - Python
tags:
  - python
  - programming
  - computer-science
title: PY 1. Type Hints
slug: py-1
---

!!! migrated

    *This article is migrated from which I wrote on my old blog.*

안녕하세요. 이번 시리즈에서는 파이썬에 관한 이것저것을 다루고자 합니다. 아주 기초적인 내용은 제외하고, 난이도 등등에 상관없이 다루고 싶은 주제들부터 다루고자 합니다! 이번 포스팅에서는 Python의 유용한 기능 중 하나인 type hint에 관하여 소개하고자 합니다. PEP 484의 내용을 주로 커버하는 포스팅이라고 생각하셔도 됩니다.

버젼은 3.10을 메인으로 하고 있는데.. 부분적으로 outdated된 내용이 있을 수 있습니다. 또한 Python의 typing 모듈이 커버하고 있는 범위가 매우 넓기 때문에, 저는 이 포스팅에서 가능하면 자잘한 것들(Abstract base class 목록이라던가.. 등등)에 대해서는 커버하지 않고자 합니다. 굵직한 것들 위주로 해보려고 담아봤는데도 내용이 상당히 길어졌네요..

<!-- more -->
---

## Static typing vs. Dynamic typing

프로그래밍 언어를 구분하는 기준은 여러 가지가 있는데, 그 중 대표적인 하나를 뽑자면 변수의 타입을 컴파일 타임에 구분하는지, 런타임에 구분하는지 여부가 될 것입니다. 컴파일 타임에 변수의 타입을 고정시키는 언어를 *Statically Typed Language*라고 하고, 런타임에 값들에 변수의 타입을 결정하고 변수명에 타입을 결정시키지 않는 언어를 *Dynamically Typed Language*라고 합니다. 대표적인 예시로는..

- Statically Typed Language: C, C++, Java, Go, Rust
- Dynamically Typed Language: Python, Ruby, Javascript

그리고 저희가 다룰 Python은 Dynamically Typed Language입니다. 예를 들어, 다음과 같은 코드가 가능합니다.

```python
a = 5  # int
a = "c" * a  # str
a = len(a) + 0.0  # float
```

Static Typing과 Dynamic Typing 사이에는 많은 trade-off가 있습니다만, 자세한 사항은 나중에 다른 게시글에서 살펴보도록 하겠습니다.

### Gradual typing by Type hint

그런데, 파이썬 3.5부터 *Type Hint*라는 기능이 새로 생겼습니다. [PEP 483](https://peps.python.org/pep-0483/), [PEP 484](https://peps.python.org/pep-0484/)에서 소개된 이 기능은 파이썬에서 *[Gradual typing](https://wphomes.soic.indiana.edu/jsiek/what-is-gradual-typing/)* 을 가능하게 합니다. Gradual typing을 간단하게 요약하자면, Static typing과 Dynamic typing 사이에서 사용자가 원하는 상황에 따라 언어를 바꾸지 않고 자유롭게 타이핑을 선택하는 것을 말합니다. 자세한 사항은 해당 링크를 참조해주세요. 여기서 또 중요한 것은 PEP 484에서는 파이썬이 Dynamically typed language로 계속 남을 것이며, **type hint를 의무화하지 않을 것**이라고 합니다!

## Types vs. Classes

사람들이 오해할 수 있는 것이 `class`가 곧 타입이라는 것인데요, 이는 사실이 아닙니다! 좀 더 정확하게 말하자면, class는 type의 subset입니다. 즉 모든 class는 type이지만, class가 아닌 것들 중에서도 type이 있습니다. 예를 들면 다음과 같은 것들이 있습니다.

- `Any`
- `Union[int, str]`

그 외 Conceptual하게는 `Callable[[int], str]` 같은 것들도 subtyping이 되지 않아야 될 것 같은데, 실제로 해보니 런타임에서 돌아가네요.

```python
import typing

class A(typing.Callable[[int], str]):
    def __init__(self) -> None:
        print("A")

    def __call__(self, *args, **kwds):
        return 1

if __name__ == "__main__":
    A()
```

## Base Syntax

기본적인 syntax는 매우 간단합니다.

- 변수에 type hint를 부여하고 싶을 때는 다음과 같이 씁니다.

    ```python
    a: int = 2
    b: None = None
    ```

    어떤 변수가 `None`임을 명시하고 싶을 때 `type(None)`을 쓰지 않고 `None`이라고 명시하더라도 static type checker가 알아서 판단해주도록 spec이 정의되어 있습니다.

- 함수에 type hint를 부여하고 싶을 때는 다음과 같이 씁니다. 이때, parameter type과 return type 중 어느 하나를 명시하지 않아도 상관없습니다. 파라미터 중에 일부만 type hint를 명시해줘도 됩니다! 또한, 함수가 값을 리턴하지 않을 경우 return type에 None을 명시하면 됩니다.

    ```python
    def f(x: str, y) -> int:
        return len(x) + 1

    def g() -> None:
        pass
    ```

## Any

`typing.Any`는 특별한 타입입니다. Any를 요약하면 "아무 타입이나 OK"입니다. 조금 더 정확하게 설명하면, Any는 모든 타입하고 *consistent*하며 반대로 모든 타입도 Any와 *consistent*합니다. 이 consistent하다는 게 무슨 뜻인지 잠깐 짚고 넘어가보도록 하겠습니다.

### is-consistent-with

*is-consistent-with*는 PEP 483에서 새로 정의한 두 타입 사이의 관계입니다. 이 관계는 *is-subtype-of* (예: `bool` is subtype of `int`.)와 비슷하지만, 이 관계는 `typing.Any`가 중간자로 있을 때 *non-transitive*하다는 데 있습니다. (어떤 관계 `R`이 transitive하다는 것은, `R(A, B) && R(B, C) => R(A, C)`라는 의미입니다.) is-subtype-of는 다음 3가지 규칙에 의해 정의됩니다.

1. `t1` is subtype of `t2` 라면, `t1` is consistent with `t2` 입니다.
2. `Any` is consistent with every type. (하지만 `Any`는 모든 타입의 subtype이 아닙니다.)
3. Every type is consistent with `Any`. (하지만 모든 타입은 `Any`의 subtype이 아닙니다.)

`object` 타입과 `Any` 타입이 확실하게 차이가 나는 지점은 `object`는 대부분의 타입과 consistent하지 않다는 점입니다. (반대로 대부분의 타입은 `object`와 consistent합니다.) `Any`는 파이썬 type hierarchy에서 top과 bottom에 동시에 위치한 이상하지만 특별한 존재라고 생각하셔도 됩니다.

그럼 이 `is-consistent-with`라는 개념은 언제 쓰이냐면, 어떤 `value`와 `variable`에 대해 *`type(value)` is consistent with `type(variable)`* 할 때, `variable = value` 꼴의 assignment가 가능합니다. 예를 들어보겠습니다.

```python
from typing import Any

class L1: pass
class L2(L1): pass

a = L1()  # a: L1
a = L2()  # a: L2, L2 is consistent with L1 because L2 is subtype of L1

b = L2()  # b: L2
b = L1()  # b: L1, L1 is not consistent with L2, fails type check

def some_any() -> Any:
    pass

c = some_any()  # c: any
a = c  # a: L1, Any is consistent with all types

d = some_any()
d = L1()  # d: Any, all types are consistent with Any
```

### Implicit Any

일반적으로 Type hint가 없는 변수는 모두 Any로 취급됩니다. Any와 어떤 variable이 연산한 결과도 Any이며, Any의 어떤 메소드를 실행한 결과도 Any입니다. 또한 input parameter가 모두 type hint가 적용되어 있는 함수라 하더라도, 리턴값에 대한 type hint가 없고 static type checker가 리턴값에 대한 타입 추론을 하지 못한다면 리턴값 또한 Any로 취급합니다.

## Type Alias

Type alias 또한 일종의 변수입니다.

```python
URL = str

def wow(url: URL) -> None:
    pass
```

Type hint에 들어갈 수 있는 타입이라면 그 어떤 것도 Type alias 값이 될 수 있습니다.

## Generic

`typing.Generic`이란, 어떤 오브젝트를 여러 개 가지고 있는 컨테이너 같은 객체들로부터 그 안에 든 오브젝트들을 정적 추론하기 위해 생긴 개념이라고 보시면 됩니다. 대표적인 예시를 들어보겠습니다.

```python
import typing

class Human:
    def __init__(self, age: int = 0) -> None:
        self.age: int = age

def aging(humans: typing.Iterable[Human]) -> None:
    for human in humans:
        human.age += 1
```

위 예시 코드에 intellisense를 돌리면 static type checker가 `for`문 안의 `human`의 타입을 `Human`이라고 인식하는 것을 알 수 있습니다. 이렇듯 subscription(대괄호 인덱싱)을 사용하여 Generic을 이용할 수 있으며, 더 나아가 다음 예시와 같이 `TypeVar`를 사용하여 Generic을 파라미터화 하는 것도 가능합니다. 그리고 이 파라미터의 개수는 여러 개가 될 수도 있습니다. (하지만 같은 `TypeVar`을 2번 이상 사용해서는 안 됩니다.) TypeVar에 대한 소개는 밑에서 자세히 다뤄보겠습니다.

```python
import typing

T = typing.TypeVar("T", int, float)

def multiplicate_all(numbers: list[T]) -> T:
    start: T = 1
    for number in numbers:
        start *= number
    return start

def multiplicate_mapping(numbers: dict[str, T]) -> tuple[str, T]:
    start: T = 1
    concatenated_name: str = ""
    for name, number in numbers.items():
        start *= number
        concatenated_name += name
    return concatenated_name, start
```

물론, 유저가 직접 Generic type을 정의할 수도 있습니다. 그럴 경우에는 `typing.Generic`을 상속받아서 씁니다.

```python
import typing

T = typing.TypeVar("T")

class SomeContainer(typing.Generic[T]):
    def __init__(self, element: T, length: int):
        self.container: list[T] = [element for _ in range(length)]

    def get_first(self) -> T:
        return self.container[0]

    def append(self, new_element: T) -> None:
        self.container.append(new_element)

def wow_two_containers(
    int_container: SomeContainer[int],
    float_container: SomeContainer[float]
) -> None:
    pass
```

Parameter 없이 Generic을 사용할 경우 해당 Generic의 parameter에 `typing.Any`가 들어간다고 간주합니다.

```python
import typing

def f(x: typing.Iterable):  # typing.Iterable[typing.Any]
    pass
```

Generic type alias를 정의하는 것 또한 가능합니다.

```python
import typing

T = typing.TypeVar("T", int, float)

Vector = typing.Iterable[tuple[T, T]]

def inner_product(vec: Vector[T]) -> T:
    return sum(x*y for x, y in vec)
```

## TypeVar

`typing.TypeVar`는 말 그대로 *Type Variable*입니다. Static type checker를 위해 존재하는 개념이며, Generic type의 parameter 개념으로 사용됩니다. 예를 들어보겠습니다.

```python
import typing

T = typing.TypeVar("T")

def return_itself(x: T) -> T:
    return x

a = return_itself(5)  # a: int
b = return_itself(())  # b: tuple
c = return_itself("")  # c: str
```

여기서 `return_itself`는 `T`를 parameter로 받는 generic function이며, 파라미터 x의 type에 따라 return type이 달라집니다. 이렇듯 TypeVar와 Generic이 합쳐지면 상당히 강력한 typing을 해낼 수 있습니다.

### Scoping rule for TypeVar

TypeVar도 일반적인 scoping rule을 따르지만, 몇 가지 특수한 케이스가 존재합니다.

1. 같은 코드 블럭의 다른 generic 함수/클래스들에 쓰인 동일한 TypeVar들은 서로 독립적입니다.

    ```python
    import typing

    T = typing.TypeVar("T")

    def f1(x: T) -> T: ...
    def f2(x: T) -> T: ...

    x = f1(1)  # x: int; T is inferred to be int
    y = f2('a')  # y: str; T is inferred to be str
    ```

2. TypeVar가 parameter로 쓰인 generic class의 내부 블럭에서는 해당 TypeVar가 항상 동일합니다.

    ```python
    import typing

    T = typing.TypeVar("T")

    class C(typing.Generic[T]):
        def wow(self, x: T) -> T: ...
        def huh(self, x: T) -> T: ...

    c: C[int] = C()
    c.wow(1)  # OK
    c.wow('a')  # Error
    ```

3. 2번에서 generic class에 쓰이지 않은 새로운 TypeVar가 내부 블럭의 함수/클래스 정의에 쓰였을 경우 해당 메소드 또는 함수를 generic 함수로 만듭니다.

    ```python
    import typing

    T1 = typing.TypeVar("T1")
    T2 = typing.TypeVar("T2")

    class C(typing.Generic[T1]):
        def method(self, x: T1, y: T2) -> T2:
            ...

    c: C[int] = C()
    d = c.method(1, "abc")  # d is inferred to be str
    ```

4. 특정 클래스나 함수에 엮이지 않은 TypeVar(*Unbound type variable*)는 generic function 또는 class body에서 등장하지 않아야 합니다. (3번 규칙에 해당하는 메소드 정의 등 제외)

    ```python
    import typing

    T1 = typing.TypeVar("T1")
    T2 = typing.TypeVar("T2")

    def f(x: T1) -> None:
        y: list[T2] = []  # Error

    class C(typing.Generic[T1]):
        some_attribute: set[T2] = set()  # Error
    ```

5. 어떤 TypeVar를 사용하는 클래스가 똑같은 TypeVar를 사용하는 클래스/함수 내에 nested되어 있으면 안 됩니다.

    ```python
    import typing

    T = typing.TypeVar("T")

    def f(x: T) -> None:
        class C(typing.Generic[T]):  # Error
            pass

    class L1(typing.Generic[T]):
        class L2(typing.Generic[T]):  # Error
            pass
    ```

### Upper bound

TypeVar를 만들 때, `bound=<type>`을 parameter로 넘겨서 해당 TypeVar의 upper bound type을 특정할 수 있습니다. 예를 들면..

```python
import typing

T = typing.TypeVar("T", bound=typing.Sized)

def longer(x: T, y: T) -> T:
    return x if len(x) > len(y) else y
```

여기서 주의할 점은, TypeVar는 bound와 constraint를 동시에 가질 수 없다는 것입니다. 예를 들어, 다음 코드는 에러를 뱉습니다.

```python
import typing

T = typing.TypeVar("T", object, bound=str)  # Error
```

### Covariance, Contravariance

이 부분은 [wikipedia](https://en.wikipedia.org/wiki/Covariance_and_contravariance_%28computer_science%29#Formal_definition)와 [PEP 484](https://peps.python.org/pep-0484/#covariance-and-contravariance) 참고했음을 알려드립니다. 저는 이걸 처음 볼 때 개념이 상당히 헷갈렸습니다.

Generic class `I`에 대하여,

- `A <= B`를 "A is subtype of B"라고 정의합니다.
- 임의의 `A, B`에 대해 `A <= B` 이면 `I<A> <= I<B>` 일때, `I<T>`는 T에 대해 covariant합니다.
- 임의의 `A, B`에 대해 `A <= B` 이면 `I<A> >= I<B>` 일때, `I<T>`는 T에 대해 contravariant합니다.
- Covariant와 contravariant를 동시에 만족하면 bivariant합니다.
- Covariant와 contravariant를 동시에 불만족하면 invariant합니다.

예를 들면..

- `typing.Union`은 항상 모든 parameter type에 대해 covariant합니다. 모든 `k`에 대해 `t[k] < u[k]` 일 때, `Union[t1, t2, ...]`는 `Union[u1, u2, ...]`의 subtype이기 때문입니다.
- `frozenset` 또한 parameter type에 대해 covariant합니다. 예를 들어, `int`는 `object`의 subclass이고, (PEP 483에 따르면) `frozenset[int]`의 모든 값들의 집합은 `frozenset[object]`의 모든 값들의 집합의 부분집합이면서 동시에 `frozenset[int]`의 모든 메소드들의 집합 또한 `frozenset[object]`의 모든 메소드들의 집합의 부분집합이기 때문이라는데.. 이 부분은 아직 잘 이해를 못해서 나중에 좀 더 찾아보겠습니다.
- `list`는 invariant합니다. 예를 들어 `list[int]`의 모든 값들의 집합은 `list[object]`의 모든 값들의 부분집합이지만, `list[int].append(object)` 같은 건 불가능합니다.
- `typing.Callable`은 파라미터 타입에 대해 contravariant합니다.
  - `Callable`은 리턴 타입에 대해서는 covariant합니다. 예를 들어, `Callable[[], int]`는 `Callable[[], object]`의 subtype입니다.
  - 그런데, `Callable[[object], None]`은 `Callable[[int], None]`의 subtype입니다! 직관적으로 이해가 안 와닿을 수 있어서 예시 코드를 추가해보았습니다.

  ```python
  import typing

  def sum_of_f(numbers: list[int], f: typing.Callable[[int], float]) -> float:
      return sum(f(number) for number in numbers)
  ```

  여기서 `f`에 `typing.Callable[[object], float]`를 넣더라도 아무 이상이 없습니다. object를 넣어서 돌아갈 함수는 float를 넣어서도 돌아가기 때문입니다.

TypeVar에 covariance랑 contravariance를 적용시키는 방법은 간단합니다. `covariant=True`, `contravariant=True`를 넣어주면 됩니다.

```python
import typing

T = typing.TypeVar("T")  # Invariant
T_co = typing.TypeVar("T_co", covariant=True)  # Covariant
T_contra = typing.TypeVar("T_contra", contravariant=True)  # Contravariant

class CovariantClass(typing.Generic[T_co]):
    ...

class ContravariantClass(typing.Generic[T_contra]):
    ...
```

여기서 주의하셔야 할 점은, covariant와 contravariant는 TypeVar의 속성이 아니라 해당 TypeVar를 사용하는 Generic class의 속성이라는 점입니다! 저도 맨 처음에는 이걸 무지 헷갈렸네요..

### Many builtins are generic

`list`, `tuple`, `set`, `dict`, `collections.abc.Iterable`, `collections.deque`, `collections.abc.Generator`, ... 정말 많은 타입이 `[]`를 지원합니다!

## Callable

`typing.Callable`은 call(ex: `f(a, b)`)이 가능한 객체를 말합니다. Callable의 subscription은 2가지 요소로 이루어지며, parameter와 return value로 이루어집니다. 여기서 parameter는 list이거나, 혹은 `...`입니다. 예를 들면..

```python
import typing

def f(x: int, y: int) -> str:
    return str(x+y)

g1: typing.Callable[[int, int], str] = f
g2: typing.Callable[..., typing.Any] = f
```

### ParamSpec

`typing.ParamSpec`은 함수의 parameter에 관한 변수로, type variable의 특수한 케이스입니다. 사용 방법은 TypeVar와 매우 유사합니다.

```python
import typing

P = typing.ParamSpec("P")
```

ParamSpec은 어떤 Callable의 parameter 정보를 그대로 끌어다가 다른 Callable의 TypeVar로 사용할 때 씁니다. 예를 들면 다음과 같습니다.

```python
import typing

T = typing.TypeVar("T")
P = typing.ParamSpec("P")

def decorator(func: typing.Callable[P, T]) -> typing.Callable[P, T]:
    def inner_func(*args: P.args, **kwargs: P.kwargs) -> T:
        print("Starting..")
        result: T = func(*args, **kwargs)
        print("Finishing..")
        return result
    return inner_func

@decorator
def add(x: int, y: int) -> int:
    return x + y
```

여기서 굳이 ParamSpec을 쓰고, `typing.Callable[..., T]`와 같은 해결방법을 쓰지 않는 이유는 다음과 같습니다.

1. `args`, `kwargs`의 타입이 Any가 되기 때문에 type checker가 `inner_function`의 타입을 제대로 추론할 수 없게 됩니다.
2. `cast()` 또는 `# type: ignore` 등의 부가적인 조치를 취해주어야 합니다.

### Concatenate

`typing.Concatenate`는 `Callable`과 `ParamSpec`에 같이 쓰이며, parameter를 한 Callable에서 또 다른 Callable로 옮기면서 동시에 특정 파라미터를 제거하거나 추가할 때 쓰입니다. 사용법은 `Concatenate[Arg1Type, Arg2Type, ..., ParamSpecVariable]` 형태로 씁니다. 예를 들면..

```python
import typing

P = typing.ParamSpec("P")
T = typing.TypeVar("T")

def decorator(f: typing.Callable[typing.Concatenate[int, P], T]) -> typing.Callable[P, T]:
    def inner_func(*args: P.args, **kwargs: P.kwargs) -> T:
        return f(1, *args, **kwargs)
    return inner_func

@decorator
def f(x: int, y: float) -> int:
    return len(str(x + y))

print(f(0.5))
```

## Protocol

`typing.Procotol`은 Structural subtyping을 위해 만들어진 녀석입니다. 예시는 다음과 같습니다.

```python
import typing

class Polygon(typing.Protocol):
    def area(self) -> float:
        ...

class Line:
    def area(self) -> float:
        return 0.0

def f(shape: Polygon) -> float:
    return shape.area()

f(Line())  # Passes type check
```

여기서 잠깐, Structural subtyping에 대해 조금 알아보고 가도록 하겠습니다.

### Nominal subtyping vs. Structural subtyping

[PEP 484](https://peps.python.org/pep-0484/)에서 소개된 static type system은 *nominal subtyping*이라는 방식을 사용했습니다. [Nominal type system](https://en.wikipedia.org/wiki/Nominal_type_system)이란, 데이터 타입의 호환성과 일치함이 type name의 정의(subtype, etc)에 의해 결정되는 타입 시스템을 말합니다. 하지만 이 방식은 (Python 공식 문서에 따르면) unpythonic하고, dynamic typing이 적용된 파이썬 코드에서 일반적으로 사용할만한 방식은 아니라고 합니다. 이에 대해 [PEP 544](https://peps.python.org/pep-0544/#wiki-structural)에서 제시한 해법은 [Structural type system](https://en.wikipedia.org/wiki/Structural_type_system)을 사용하는 것인데요. 이것은 바로 데이터 타입의 호환성과 일치함이 두 타입의 실제 구조(변수, 메소드 구조 등)에 의해 결정되는 타입 시스템을 말합니다. 예를 들어보겠습니다.

```python
import typing

class BucketPEP484(typing.Sized, typing.Iterable[int]):
    pass

class BucketPEP544:
    def __len__(self) -> int: ...
    def __iter__(self) -> typing.Iterator[int]: ...

def get_from_iterable(items: typing.Iterable[int]) -> int: ...

get_from_iterable(BucketPEP484())
get_from_iterable(BucketPEP544())
```

Nominal subtyping에서는 `BucketPEP544()`가 type check를 통과하지 못하지만, Structural subtyping에서는 `BucketPEP544()`가 type check를 통과합니다! 사실 runtime 상에서는 이미 structural subtyping이 적용되고 있었는데(`isinstance(BucketPEP544(), typing.Iterable)`이 `True`를 리턴합니다.), PEP 544는 이것을 static time에도 적용되도록 확장시켰습니다.

### Protocol with generic

Protocol 클래스 또한 Generic을 적용시킬 수 있습니다. 예를 들어 다음과 같은 게 가능합니다.

```python
import typing

T = typing.TypeVar("T")

class Polygon(typing.Protocol[T]):
    def area(self) -> T:
        ...
```

## Union

`typing.Union`은 *하나 이상*의 타입의 합집합을 나타냅니다. `Union[X, Y, Z]`로 쓰거나, 아니면 `X | Y | Z`로 씁니다. 예를 들면..

```python
from typing import Union

x = Union[int, str, float, complex, list[str]]
```

Union에는 몇 가지 규칙이 있는데요. 다음과 같습니다.

1. Union의 union은 평탄화(flattened)됩니다.
2. 단 하나의 parameter만 있는 Union은 그 타입과 동일합니다.
3. 불필요한 parameter는 정리됩니다.
4. Parameter의 순서는 고려되지 않습니다.
5. Union은 subclass를 만들 수 없고, 또한 instantiate할 수 없습니다.

```python
from typing import Union

Union[Union[int, str], float] == Union[int, str, float]
Union[int] == int
Union[int, str, int] == Union[int, str] == Union[str, int]
```

### Optional

Optional type을 위해 나온 것으로, `typing.Optional[T]`는 `typing.Union[T, None]`과 동일합니다.

## Literal

[PEP 586](https://peps.python.org/pep-0586/)에서 소개된 `typing.Literal`은 type checker가 특정 변수가 특정 literal을 가졌는지를 테스트할 수 있게 하기 위해서 만들어진 개념입니다. 사용방법은 `typing.Literal[x1, x2, ...]`입니다. (x는 literal 값)

```python
import typing

def always_return_one(*args: typing.Any, **kwargs: typing.Any) -> typing.Literal[1]:
    ...

def custom_open(file: str, mode: typing.Literal["r", "rb", "w", "wb"] = "r") -> str:
    ...

custom_open("some_file_path", "r")  # OK
custom_open("some_file_path", "x")  # Error
custom_open("some_file_path", input())  # Error
```

두 번째 에러에서 보실 수 있듯이, 어떤 값으로 나올지 확정되지 않는 변수는 Literal이랑 호환되지 않습니다. 또한, Literal[...]는 subclassing을 하는 것이 불가능합니다.

## ClassVar

`typing.ClassVar`은 class variable을 마킹하기 위한 타이핑으로, 어떤 클래스의 인스턴스에서 해당 변수를 설정하려고 하면 static type checker가 오류를 뱉습니다. 사용법은 `typing.ClassVar[type]`으로 씁니다.

```python
import typing

class C:
    x: typing.ClassVar[int] = 1

c = C()
c.x = 2  # Error
C.x = 2  # OK
```

## Final

`typing.Final`은 해당 변수가 한번 assignment를 받은 이후 더 이상 assignment를 받거나 서브클래스에서 값이 변경되지 않도록 마킹하는 타이핑입니다. `typing.Final[type]`으로 씁니다.

```python
import typing

ONE = typing.Final[int] = 1
ONE += 1  # Error

class L1:
    x: typing.Final[float] = 0.1234

class L2(L1):
    x = 0.5678  # Error
```

## Annotated

[PEP 593](https://peps.python.org/pep-0593/)에서 소개된 `typing.Annotated`는 콘텍스트 의존적인 메타데이터를 type에 장식하고자 하는 용도로 나왔습니다.. 정도까지만 이해했습니다. 구체적으로 어떤 상황에서 유용할 지가 머릿속으로 그려지지 않았고(전부 이해되지 않은 게 큰 것 같습니다.) 나중에 더 잘 알게 되면 이 문단을 다시 재작성하도록 하겠습니다.

## TypeGuard

[PEP 647](https://peps.python.org/pep-0647/)에서 소개된 `typing.TypeGuard`는 *conditional type narrowing*을 도와주는 것을 목적으로 만들어졌습니다. 예를 들어보겠습니다.

```python
def is_str_list(val: list[object]) -> bool:
    return all(isinstance(x, str) for x in val)

def print_if_str_list(val: list[object]) -> None:
    if is_str_list(val):
        print(" ".join(val))  # Error
```

위 코드는 static type checker가 에러를 뱉습니다. 런타임 입장에서 봤을 때 로직에 전혀 문제가 없는 코드이지만, if문을 통과했다고 해서 static type checker가 `val`의 type을 `list[str]`로 추론하지 않기 때문입니다. `TypeGuard`는 이런 문제점을 해결하고자 시작되었습니다. `TypeGuard[type]`은 함수의 리턴값에 쓰이고, 해당 함수는 실제 `bool`을 리턴해야 합니다. 만약 참일 경우, if문 또는 assert문 뒤 해당 함수의 첫 번째 파라미터로 들어갔던 값은 `type`으로 추론되게 됩니다. 위 예시를 정상적으로 작동하도록 고쳐보겠습니다.

```python
import typing

def is_str_list(val: list[object]) -> typing.TypeGuard[list[str]]:
    return all(isinstance(x, str) for x in val)

def print_if_str_list(val: list[object]) -> None:
    if is_str_list(val):
        print(" ".join(val))
```

Typescript에도 [type predicates](https://www.typescriptlang.org/docs/handbook/2/narrowing.html#using-type-predicates)라는 동일한 기능이 있습니다. 여기서는 unique syntax가 쓰이는데, Python은 하위호환성을 지키게 하기 위해 특별한 syntax를 도입하지 않고 이렇게 별개의 오브젝트를 만들었습니다.

또한, `def foo(x: TypeA) -> TypeGuard[TypeB]` 에서 `TypeB`가 `TypeA`의 하위 클래스일 필요가 없습니다. 몇몇 타입들은 contravariant하거나 또는 invariant하기 때문입니다! 그래서 TypeGuard를 제대로 사용하는 것은 유저의 책임으로 남겨놓았다고 하네요.

## TypedDict

[PEP 589](https://peps.python.org/pep-0589/)에서 소개된 `typing.TypedDict`는 key들의 종류가 고정된 dict를 표현하기 위해 만들어진 특별한 자료형입니다. `TypedDict`를 사용하면 해당 dict에는 특정 종류의 키만 정확하게 해당 타입으로 있어야 합니다. (다만, 런타임에서는 그냥 순수 dict로 돌아갑니다.) `dataclass`와 비슷하다고 생각할 수도 있겠네요. 예를 들어, 다음과 같이 씁니다.

```python
import typing

class Human(typing.TypedDict):
    name: str
    birth_year: int

# Functional usage
# Human = typing.TypedDict("Human", {"name": str, "birth_year": int})

author: Human = {"name": "author", "birth_year": 1998}  # OK
no_name: Human = {"birth_year": 2000}  # Error; No 'name'
human_with_gender: Human = {"name": "human", "birth_year": 2022, "male": True}  # Error; Extra key
```

또한, TypedDict는 또 다른 TypedDict를 1개 *이상* 상속 받을 수 있으나, 다른 클래스로부터는 상속받지 못합니다. (특히 Generic도 포함됩니다.)

```python
import typing

class X(TypedDict):
    x: int

class Y(TypedDict):
    y: float

class Z: pass

class XY(X, Y): pass  # OK

class XZ(X, Z): pass  # raises TypeError
```

그 외 있어도 되고 없어도 되는 키를 추가하는 방법이 있습니다만(상속과 `total=False` 옵션으로 할 수 있습니다), 넘어가겠습니다!

## Special functions and decorators

### cast

`typing.cast(type, value)`는 `value`를 `type`로 cast한 결과를 리턴합니다. 예를 들어..

```python
import typing

a: int = 2
b: str = typing.cast(str, 2)
```

런타임에서는 실제로 아무것도 안하고 그냥 값을 그대로 리턴하는 역할을 합니다. 저는 개인적으로 `# type: ignore` 같은 주석이나 `typing.cast` 같은 함수를 최대한 지양해야 한다고 생각합니다. Statically typed system을 쓰는 파트만큼은 타입 시스템이 이런 강제적인 캐스팅 없이 잘 돌아가게끔 설계해야 제대로 타입 시스템을 잘 사용하고 있다고 생각하기 떄문입니다.

### @overload

`typing.overload` 데코레이터는 함수 또는 메소드가 여러 가지 타입의 인풋에 대해 서로 다른 리턴값을 추론할 수 있도록 도와주는 역할을 합니다. 예를 들어..

```python
import typing

@typing.overload
def f(x: int) -> int:
    ...

@typing.overload
def f(x: str) -> str:
    ...

@typing.overload
def f(x: None) -> int:
    ...

def f(x: typing.Union[int, str, None]) -> typing.Union[int, str]:
    if x is None:
        return 0
    elif isinstance(x, str):
        return x + "a"
    else:
        return abs(x)
```

이렇게 하면 mypy 같은 툴들이 `f` 안에 어떤 타입의 값이 들어갔는지에 따라 다른 output type을 추론합니다.

### @final

`typing.Final`과 유사하지만, 클래스의 메소드 또는 클래스를 위한 데코레이터입니다. `typing.final`을 데코레이트 받은 클래스는 다른 클래스의 부모 클래스가 될 수 없으며, 데코레이트 받은 메소드는 자식 클래스에서 내용이 바뀔 수 없습니다.

```python
import typing

class Base1:
    @typing.final
    def f(self) -> None:
        ...

class Child1(Base1):
    def f(self) -> None:  # Error
        ...

@final
class Base2:
    pass

class Child2(Base2):  # Error
    pass
```

---

이 외에도 다른 자잘한 내용들이 많지만, 넘어가겠습니다! 이로써 Python의 type hint에 대해 이것저것 알아보았습니다. 제가 개인적으로 강타입의 팬이라, 앞으로도 더 좋은 기능들이 많이 추가되었으면 하는 바람입니다. 이상으로 읽어주셔서 감사합니다.
