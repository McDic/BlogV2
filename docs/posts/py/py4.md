---
categories:
  - Python
tags:
  - python
  - programming
  - computer-science
title: PY 4. Some Concepts to Learn After Basics
---

안녕하세요.
Python과 관련하여 기본적인 문법과 자료형
(`for`, `while`, `if`, `else`, `def`, `int`, `float`, `str`, `class`, ...)
들의 기초적인 사용법을 배운 이후 좀 더 어려운 topic에 관해서

!!! quote

    *"뭘 공부해야 할까요?"*

라는 질문을 여기저기서 많이 봐서, 한번 시간 날 때 정리해보았습니다.

!!! info

    뭔가 빼먹은 좋은 주제가 나중에 생각나거나 누군가로부터 제보를 받는다면 그것도 추가하겠습니다.

!!! warning

    이 게시글은 그 모든 개념을 직접적으로 담은 문서가 아니고, 개념들의 컨셉 정도만 소개하는 글입니다.

<!-- more -->
---

## Generator function

기초 지식보다는 좀 멀지만, 많은 사람들이 매우 자주 애용하는 기능 중에서 대표적인 것이 generator function이라고 생각합니다.

### Basic usage

함수 안에 `yield`를 추가하는 순간, 그 함수는 일반적인 함수가 아닌 **"Generator Function"**이 됩니다.

```python title="range_forever_1.py"
import typing

def range_forever(start: int = 0) -> typing.Generator[int, None, None]:
    while True:
        yield start
        start += 1

if __name__ == "__main__":
    for num in range_forever():
        print("num =", num)
```

Generator function의 리턴값은 generator(이자 동시에 iterator)이며, 이 값은 for문 등에서 쓰일 수 있습니다.
위 코드의 실행결과는 다음과 같이 됩니다.

``` title="Result of range_forever_1.py"
num =  0
num =  1
num =  2
num =  3
num =  4
num =  5
... (무한 반복됨)
```

### Bidirectional communication with `send`

Generator function은 단순히 값을 밖으로 표출하는 것뿐만이 아니고 값을 받아들이는 것으로 외부와 양방향 통신이 가능하며,
이는 `yield value` 구문의 리턴값을 받아오는 것을 통해 가능합니다.

```python title="range_forever_2.py"
import typing

def range_forever(start: int = 0) -> typing.Generator[int, str | None, None]:
    while True:
        message = yield start
        if message:
            print(f'Oh yeah, received message: "{message}"')
        else:
            print("No received message..")
        start += 1

if __name__ == "__main__":
    generator = range_forever()
    print(generator.send(None))  # Must send `None` value at first to trigger
    print(generator.send("Hello, range_forever"))
    print(next(generator))  # Same as `generator.send(None)`
    print(generator.send("Good bye"))
```

이 `SendType`과 `YieldType` 간의 상호작용 순서는 사람에 따라 비직관적으로 다가올 수 있어서 예제를 직접 만들어보는 것이 이해가 빠를 것이라 생각합니다.
위 코드의 실행결과는 다음과 같이 됩니다.

``` title="Result of range_forever_2.py"
0
Oh yeah, received message: "Hello, range_forever"
1
No received message..
2
Oh yeah, received message: "Good bye"
3
```

### How `StopIteration` works

심지어 generator function 안에서 return 값을 추가하는 것도 가능하다는 사실을 알고 계신가요?
이 리턴값은 `next`를 통해 다음 값을 받아올 때 발생하는 `StopIteration` exception의 내부 값이 됩니다.

```python title="range_forever_3.py"
import typing

def range_forever(start: int = 0) -> typing.Generator[int, None, str]:
    while True:
        yield start
        if start == 42:
            return "So beautiful number.."
        start += 1

if __name__ == "__main__":
    generator = range_forever(40)
    try:
        while True:
            print("num =", next(generator))
    except StopIteration as err:
        print("Stopped:", err.value)
```

위 코드에서 generator에서 return된 값이 반복문이 멈춤으로써 발생한 `StopIteration`의 내부 값으로 전달된 것을 보실 수 있습니다.
위 코드의 실행결과는 다음과 같이 됩니다.

``` title="Result of range_forever_3.py"
num = 40
num = 41
num = 42
Stopped: So beautiful number..
```

### `yield from`

`from`을 모듈 import하는 거 말고도 다른데서 쓰는 것이 가능하다는 것을 알고 계셨나요?
`yield from x`는 `for s in x: yield s` 랑 똑같은 기능을 합니다.
그래서 다음과 같이 list flattening 같은 것을 매우 간편하게 구현할 수 있습니다.

```python title="yield_from.py"
import typing

def flatten_iter(x: list) -> typing.Iterator[int]:
    for element in x:
        if isinstance(element, list):
            yield from flatten_iter(element)
        else:
            yield element

if __name__ == "__main__":
    print(list(flatten_iter([1, 2, [3, [[4, 5], 6]], [7, 8], 9])))
```

``` title="Result of yield_from.py"
[1, 2, 3, 4, 5, 6, 7, 8, 9]
```

자세한 사항은 [Python Wiki - Generators](https://wiki.python.org/moin/Generators)를 참고해주세요.

---

## Magic methods

Python의 객체들이 가지고 있는 특별한 method들이 있습니다.
이름이 `__` (언더바 2개)로 시작하고 끝나는 메소드들이 그러한 것들입니다.

### Operator overloading

C++에서도 `operator` 문법으로 가능한 연산자 오버로딩이 Python에서도 가능합니다.
다음 코드는 덧셈, 뺄셈, $-1$배 상수 곱셈(negation), 그리고 내적이 가능한 벡터를 간단하게 구현한 것입니다.

```python title="math_vector.py"
import typing
from typing import Self

class Vector:
    def __init__(self, contents: typing.Iterable[int]) -> None:
        self.contents: list[int] = list(contents)

    def __str__(self) -> str:
        """
        `str(self)` calls this
        """
        return f"Vec({', '.join(str(x) for x in self.contents)})"

    def __iter__(self) -> typing.Iterator[int]:
        """
        Used in `for` and `while`
        """
        return iter(self.contents)

    def __add__(self, another: Self) -> Self:
        """
        Returns `self + another`
        """
        return type(self)(a1 + a2 for a1, a2 in zip(self, another, strict=True))

    def __neg__(self) -> Self:
        """
        Returns `-self`
        """
        return type(self)(-a for a in self)

    def __sub__(self, another: Self) -> Self:
        """
        Returns `self - another`
        """
        return self + (-another)

    def __mul__(self, another: Self) -> int:
        """
        Returns `self * another` (Dot product)
        """
        return sum(a1 * a2 for a1, a2 in zip(self, another, strict=True))

if __name__ == "__main__":
    v1 = Vector([1, 2, 3, 4])
    v2 = Vector([2, 3, 2, 4])
    print("v1 =", v1)
    print("v2 =", v2)
    print("-v1 =", -v1)
    print("v1+v2 =", v1 + v2)
    print("v1-v2 =", v1 - v2)
    print("v1*v2 =", v1 * v2)
```

`v1 + v2` 같은 코드들이 실제로는 `v1.__add__(v2)`를 호출하는 셈입니다.
위 코드의 실행 결과는 다음과 같이 됩니다.

``` title="Result of math_vector.py"
v1 = Vec(1, 2, 3, 4)
v2 = Vec(2, 3, 2, 4)
-v1 = Vec(-1, -2, -3, -4)
v1+v2 = Vec(3, 5, 5, 8)
v1-v2 = Vec(-1, -1, 1, 0)
v1*v2 = 30
```

이런 식으로 덧셈, 뺄셈, 곱셈, 나눗셈, 지수(power) 연산, 비트 연산 등등 거의 모든 연산자들에 대한 오버로딩이 가능합니다.
오버로딩이 불가능한 연산자로는 `and`, `or`, `not` 같은 것들이 있습니다.

### Built-in functions that calls magic method

빌트인 클래스, 함수들, 심지어는 문법 중에서도 이러한 magic method를 통해 커스텀한 결과를 내보낼 수 있습니다. 대표적으로 `hash`(`__hash__`), `str`(`__str__`), `for`(`__iter__`), `repr`(`__repr__`) 등등이 있습니다.

```python title="misc_magic_methods.py"
class WowClass:
    def __init__(self, data: str) -> None:
        self.data = data

    def __len__(self) -> int:
        """
        `len(self)` calls this
        """
        return len(self.data)

    def __iter__(self):
        """
        `iter(self)` calls this;
        Will be used in iterations like `for` clause.
        """
        return iter(self.data)

    def __hash__(self) -> int:
        """
        `hash(self)` calls this.
        Let's hash for just first character only instead.
        """
        return hash(self.data[0] if self.data else "")

    def __int__(self) -> int:
        """
        `int(self)` calls this
        """
        return len(self)  # This will do `self.__len__()`

if __name__ == "__main__":
    wow_hello = WowClass("hello yeah")
    wow_world = WowClass("holy world")
    print("Length of wow_hello =", len(wow_hello))
    print("Length of wow_world =", len(wow_world))
    assert hash(wow_hello) == hash(wow_world)
    for ch1, ch2 in zip(wow_hello, wow_world):
        print("%s  %s" % (ch1, ch2))
```

``` title="Result of misc_magic_methods.py"
Length of wow_hello = 10
Length of wow_world = 10
h  h
e  o
l  l
l  y
o
   w
y  o
e  r
a  l
h  d
```

### Context manager

`open` 함수의 결과값을 변수에 바로 안 집어넣고 `with`를 통해서 가져오는 이유가 `with`문 밖을 빠져나갈 때 자동으로 파일을 닫아주기 위함인데,
이것을 **"Context Manager"**라고 하며 이것 또한 magic method들과 관련이 있습니다.

```python title="context_manager.py"
class EnterExit:
    def __init__(self) -> None:
        pass

    def __enter__(self) -> str:
        print("Entering context!")
        return "bruh"

    def __exit__(self, typ, val, tb) -> None:
        print("Exiting context!")

if __name__ == "__main__":
    with EnterExit() as ctx:
        print("EnterExit().__enter__() returned", ctx)
```

``` title="Result of context_manager.py"
Entering context!
EnterExit().__enter__() returned bruh
Exiting context!
```

자세한 사항으로는 공식 웹사이트나 혹은 다음과 같이 잘 정리된 페이지들을 참고해주세요.

- [Magic Methods](https://rszalski.github.io/magicmethods/)
- [Context Managers](https://book.pythontips.com/en/latest/context_managers.html)

---

## Type hints

Python은 dynamic type language지만, 타입 힌트를 지원합니다.
이거 관련해서는 [PY-1](../1)에서 다루기도 했고 양이 굉장히 방대해서 여기에 일일이 적지는 않겠습니다.
다음과 같은 문서들을 참조해주세요.

- [PEP 484](https://peps.python.org/pep-0484/)
- [`typing` (공식 type hinting 관련 모듈)](https://docs.python.org/3/library/typing.html)
- [Stub files(`.pyi` 등등)](https://mypy.readthedocs.io/en/stable/stubs.html)

---

## Anonymous functions (`lambda`)

Python에서도 여타 언어들처럼 익명 함수를 정의하기 위한 방법을 제공합니다.
바로 `lambda`라는 키워드를 이용하는 것입니다.

```python title="lambdas.py"
add = lambda x, y, z: x + y + z
print(add(7, 3, 2))  # 7 + 3 + 2 = ?

some_numbers = ["apple", "banana", "grape"]
# Sort by reversed words alphabetically
some_numbers.sort(key=lambda x: x[::-1])
print(some_numbers)
```

``` title="Result of lambdas.py"
12
['banana', 'apple', 'grape']
```

---

## Comprehensions

Python에서 아마 코드를 간결하게 만들어주는 가장 유용한 기능 중 하나로 comprehension을 들 수 있겠습니다.
Comprehension은 `list`, `set`, `dict` 등등을 아주 간편하게 생성할 수 있는 방법을 제공해줍니다.

```python title="comprehensions.py"
all_words = ("apple", "banana", "grape")

# List comprehension; Collect remainders(by 5) of even integers on [0, 20)
print([x % 5 for x in range(20) if x % 2 == 0])

# Set comprehension; Does the same, but collects unique results
print({x % 5 for x in range(20) if x % 2 == 0})

# Dict comprehension; Link length of each word from data
print({word: len(word) for word in all_words})

# Generator comprehension; Sort reversed version of all words
print(sorted(word[::-1] for word in all_words))
```

``` title="Result of comprehensions.py"
[0, 2, 4, 1, 3, 0, 2, 4, 1, 3]
{0, 1, 2, 3, 4}
{'apple': 5, 'banana': 6, 'grape': 5}
['ananab', 'elppa', 'eparg']
```

---

## Decorators

Decorator는 일종의 higher order function으로, 함수를 그 자체로 값으로 받아 또 다른 함수를 생성시키는 함수입니다.
저는 Python의 이 기능을 굉장히 좋아하는데, 잘 사용하면 코드량이 정말 많이 압축되기 때문입니다.

```python title="quadratic.py"
import typing
from typing import Callable

P = typing.ParamSpec("P")
R = typing.TypeVar("R")

def args_debug(f: Callable[P, R]) -> Callable[P, R]:
    def inner_func(*args: P.args, **kwargs: P.kwargs) -> R:
        print("Got args = %s, kwargs = %s" % (args, kwargs))
        return f(*args, **kwargs)
    return inner_func

def double_combo(f: Callable[[R], R]) -> Callable[[R], R]:
    def inner_func(val: R) -> R:
        return f(f(val))
    return inner_func

@args_debug    # Outer decorator applies last
@double_combo  # Inner decorator applies first
def fast_increasing(x: int) -> int:
    return x ** 2

# Same effect as..
# fast_increasing = args_debug(double_combo(fast_increasing))

if __name__ == "__main__":
    print(fast_increasing(3))  # Prints (3**2)**2
```

``` title="Result of quadratic.py"
Got args = (3,), kwargs = {}
81
```

자세한 사항은 [Higher order functions and decorators](https://medium.com/python-supply/higher-order-functions-and-decorators-d6bb31a5c78d) 등등을 참조해주세요.

---

## MRO (Method resolution order)

Python에서 클래스 다중상속을 하게 되면, 가끔가다가 두 부모 클래스들에 똑같은 이름을 가진 다른 작업을 하는 메소드가 정의되어 있을 수 있습니다.

```python title="family.py"
class GrandParent:
    def __init__(self) -> None:
        pass

    def hello(self) -> str:
        return "\tHello from grandparent!"

class Father(GrandParent):
    def hello(self) -> str:
        return super().hello() + "\n\t<- Hello from father!"

class Mother(GrandParent):
    def hello(self) -> str:
        return super().hello() + "\n\t<- Hello from mother!"

class Me(Father, Mother):
    def hello(self) -> str:
        return super().hello() + "\n\t<- Hello from me!"

if __name__ == "__main__":
    print("GrandParent:\n", GrandParent().hello())
    print("Father:\n", Father().hello())
    print("Mother:\n", Mother().hello())
    print("Me:\n", Me().hello())
```

``` title="Result of family.py"
GrandParent:
 	Hello from grandparent!
Father:
 	Hello from grandparent!
	<- Hello from father!
Mother:
 	Hello from grandparent!
	<- Hello from mother!
Me:
 	Hello from grandparent!
	<- Hello from mother!
	<- Hello from father!
	<- Hello from me!
```

이런 식으로 Python에서 어떤 부모 클래스의 메소드를 먼저 호출할 지를 결정하는 데 쓰이는 방법을 **"MRO (Method Resolution Order)"** 라고 합니다.
자세한 사항은 [MRO docs](https://docs.python.org/3/howto/mro.html) 같은 페이지들을 참고해주세요.

---

## Asynchronous stuffs

Python 3.4인가? 어느 순간부터 비동기 관련 서포트가 프로그래밍 언어 차원에서 추가되었습니다.
`asyncio`는 동시성 코드를 작성하기 위한 Python의 standard 라이브러리입니다.
`async def`, `await`, `async for`, `async with` 같은 문법들이 이런 비동기 코드에서 쓰이게 됩니다.

```python title="concurrent_tasks.py"
import asyncio
import time

async def interpret_chars(s: str, delay: float, tab_level: int):
    for i, ch in enumerate(s):
        print("\t" * tab_level, end="")
        print(f'"{s}"[{i}] = {ch}')
        await asyncio.sleep(delay)

async def main():
    coros = [
        interpret_chars("apple", 1.0, 0),
        interpret_chars("banana", 0.75, 1),
        interpret_chars("watermelon", 0.3, 2),
    ]
    await asyncio.gather(*coros)

if __name__ == "__main__":
    started = time.time()
    asyncio.run(main())
    finished = time.time()
    print("Total %.2f seconds used" % (finished - started,))
```

아래 결과는 매 시행마다 조금씩 달라질 수 있다는 점을 유의해주시기 바랍니다.
하지만 총 실행시간은 거의 항상 5초에 가까울 것입니다.

``` title="Result of concurrent_tasks.py"
"apple"[0] = a
	"banana"[0] = b
		"watermelon"[0] = w
		"watermelon"[1] = a
		"watermelon"[2] = t
	"banana"[1] = a
		"watermelon"[3] = e
"apple"[1] = p
		"watermelon"[4] = r
	"banana"[2] = n
		"watermelon"[5] = m
		"watermelon"[6] = e
"apple"[2] = p
		"watermelon"[7] = l
	"banana"[3] = a
		"watermelon"[8] = o
		"watermelon"[9] = n
	"banana"[4] = n
"apple"[3] = l
	"banana"[5] = a
"apple"[4] = e
Total 5.01 seconds used
```

이것도 한 문서 안에 정리하기에는 내용이 너무 많아서..
다음 문서들로 대체하도록 하겠습니다.

- [`asyncio` (공식 라이브러리)](https://docs.python.org/3/library/asyncio.html)
- [Understanding Coroutines & Tasks in Depth](https://medium.com/python-features/understanding-coroutines-tasks-in-depth-in-python-af2a4c0e1073)

---

## `for ... else`

`for`문 뒤에 `else`를 넣을 수 있다는 사실을 알고 계셨나요?
`for`문 바로 뒤에 나오는 `else`를 트리거하기 위해서는, 해당 `for`문 안에서 `break`가 동작하지 않고 끝까지 루프를 돌고 끝나야 합니다.

```python title="forelse.py"
def test_any_empty(*strings: str) -> bool:
    for s in strings:
        if not s.strip():
            break
    else:
        return False
    return True

if __name__ == "__main__":
    print(test_any_empty("apple", "banana", "  ", "grape"))
    print(test_any_empty("wow", "fantastic"))
```

``` title="Result of forelse.py"
True
False
```

---

## Descriptor

Python 코드를 좀 짜다보면 `@property`를 아마 한번쯤은 사용해보았거나 아니면 들어보기라도 하셨을 겁니다.
Descriptor는 object가 lookup, storage, deletion을 커스터마이징할 수 있게 해주는 수단입니다.

```python title="simple_descriptor.py"
class AgeDescriptor:
    def __get__(self, obj: "Person", objtype=None) -> int:
        this_age = obj._age
        print("Accessing this person's age:", this_age)
        return this_age

    def __set__(self, obj: "Person", value: int) -> None:
        print("Setting this person's age to:", value)
        if value % 2 == 0:
            raise ValueError("Cannot set age to be even number")
        obj._age = value

class Person:
    age = AgeDescriptor()

    def __init__(self, age: int) -> None:
        self.age = age  # Calls `__set__`

    def time_pass(self, years: int) -> None:
        print(years, "years passed..")
        self.age += years  # Calls `__get__` and `__set__`

if __name__ == "__main__":
    somebody = Person(21)
    somebody.time_pass(4)
    somebody.time_pass(3)
```

``` title="Result of simple_descriptor.py"
Setting this person's age to: 21
4 years passed..
Accessing this person's age: 21
Setting this person's age to: 25
3 years passed..
Accessing this person's age: 25
Setting this person's age to: 28
ERROR!
Traceback (most recent call last):
  ... (omitted)
ValueError: Cannot set age to be even number
```

보다 자세한 사항은 [Python HOWTO: Descriptor Guide](https://docs.python.org/3/howto/descriptor.html) 등을 참고해주세요.

---

## Scope of variables

일반적으로 Python에서 어떤 함수에서 그 함수 밖에 있는 변수에다가 다른 값을 할당하려고 하면, 그 변수가 덮어씌워지는게 아니고 local에 새로운 변수가 생깁니다.

### `global`

하지만 `global` 키워드를 사용하여 최상위 scope에 있는 변수의 값들을 직접적으로 할당할 수 있습니다.

```python title="global.py"
global_int: int = 0

def global_set(new_value: int) -> None:
    global global_int
    print("Globally setting to", new_value, "...")
    global_int = new_value

def useless_set(new_value: int) -> None:
    print("Uselessly setting to", new_value, "...")
    global_int = new_value

def print_status():
    print("Currently, global int is", global_int)

if __name__ == "__main__":
    print_status()
    useless_set(5)
    print_status()
    global_set(7)
    print_status()
```

```title="Result of global.py"
Currently, global int is 0
Uselessly setting to 5 ...
Currently, global int is 0
Globally setting to 7 ...
Currently, global int is 7
```

### `nonlocal`

마찬가지로, `nonlocal` 키워드를 사용하여 최상위 scope는 아니지만 여전히 함수 밖에 있는 변수를 건드릴 수 있습니다.
함수 밖에 있는 변수가 함수의 closure가 되는 셈입니다.

```python title="nonlocal.py"
from typing import Callable

def nonlocal_setter() -> Callable[[], int]:
    nonlocal_int: int = 0

    def increase() -> int:
        nonlocal nonlocal_int
        nonlocal_int = nonlocal_int + 1
        return nonlocal_int

    return increase

if __name__ == "__main__":
    setter = nonlocal_setter()
    for _ in range(5):
        print("Now nonlocal int is", setter())
```

``` title="Result of nonlocal.py"
Now nonlocal int is 1
Now nonlocal int is 2
Now nonlocal int is 3
Now nonlocal int is 4
Now nonlocal int is 5
```

또 이런 키워드들과 관련된 것들로는 `globals`, `locals` 빌트인 함수가 있습니다.
자세한 사항은 다음 링크들을 참조해주세요.

- [PEP 3104](https://peps.python.org/pep-3104/)
- [Python wiki: The `global` statement](https://docs.python.org/3/reference/simple_stmts.html#global)
- [Python wiki: The `nonlocal` statement](https://docs.python.org/3/reference/simple_stmts.html#nonlocal)
- [`globals()` vs `locals()` vs `vars()`](https://stackoverflow.com/questions/7969949/whats-the-difference-between-globals-locals-and-vars)

---

## Global interpreter lock (GIL)

[GIL](https://en.wikipedia.org/wiki/Global_interpreter_lock)이란, interpreter가 memory allocation, reference counting 같은 코어한 동작들에 대해서 동시에 한 스레드만을 작동하게 해서 메모리 상의 race condition을 쉬운 구현으로 피하는 방법입니다.
Python에는 GIL이 적용되어 있습니다.
이것은 파이썬 같은 언어에서 싱글스레드로는 CPU-intensive한 작업들을 동시에 여러 개를 돌릴 수 없는 이유이기도 합니다.
3.13부터 [No-GIL build](https://peps.python.org/pep-0703/)가 실험적으로 적용되지만, 아직 갈 길이 멉니다.

---

이외에도 metaclass, `Enum`, `dataclass` 등등도 있고, 그 외에도 제가 미처 생각하지 못한 정말 다양한 것들이 많을 것 같은데..
아마 이론 공부만 하다보면 그 방대한 양에 질려버릴 수 있습니다.
제가 추천하는 것은 실전 프로젝트와 이론 공부를 병행해서 진행하는 것입니다.
그러면 이런 언어적 feature들을 어떻게 써먹을지 고민하면서 하게 되니까 덜 지루하거든요.

글을 읽어주셔서 감사합니다.
