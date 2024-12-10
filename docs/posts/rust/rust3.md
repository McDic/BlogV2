---
categories:
  - Rust
tags:
  - rust
  - python
  - programming
  - computer-science
  - quant
title: RUST 3. Some Hurdles on Converting Python Codes into Rust Codes
---

우연히 제가 있던 어떤 퀀트 관련 오픈톡방에서 Python 코드를 Rust 코드로 로직을 유지하면서 언어를 변환하는 문제에 관한 질문이 나왔습니다.
Python과 Rust는 여러 관점(typing 등)에서 봤을 때 양쪽 극단에 있는 언어이고 실제로 내부 구조도 많은 차이가 납니다.
Python 코드를 Rust 코드로 변환하는 것은 두 언어의 차이점 때문에 그렇게 만만하게 볼 문제가 아니라고 생각합니다. 자세히 서술해보겠습니다.

<!-- more -->
---

## You cannot make a container of arbitrary objects

만약 당신이 Python 안에서 *"그 어떤 데이터도 들어갈 수 있는"* 버퍼나 리스트, 큐 같은 걸 만들었다고 해봅시다.
퀀트 프로그램을 예로 들면, 거래소 어댑터들로부터 수집된 모든 데이터를 그냥 하나의 Queue 같은 거에 때려넣어서 strategy component에 전달하는게 있겠죠.
하지만 Rust에서 컨테이너는 그 원소들이 일관된 type 혹은 trait(해당 trait이 object-safe한 경우)를 보유하고 있어야 합니다.
그러니까 `list[typing.Any]` 같은 걸 Rust에서는 만들 수 없는 거죠.

만약 당신의 파이썬 코드에서 이런 식으로 컨테이너를 사용하고 있었다면
해당 컨테이너에 들어갈 수 있는 자료형들을 명확하게 정의한 뒤,
여러 개가 들어갈 수 있다면 `enum`이나 `trait` 등으로 묶고
wrapping/unwrapping function를 정의해줘야 합니다.

```python title="Python version"
from typing import Any

def f_a(individual_data: A):
    ...

def f_b(individual_data: B):
    ...

def f(data: list[Any]):
    for element in data:
        if isinstance(element, A):
            f_a(element)
        elif isinstance(element, B):
            f_b(element)
        else:
            pass  # This part should be eliminated on Rust code
```

```rust title="Rust version"
enum AB {
    AType(A),
    BType(B),
}

fn f_a(individual_data: A) -> () {
    // ...
}

fn f_b(individual_data: B) -> () {
    // ...
}

fn f(data: Vec<AB>) -> () {
    for element in data {
        match element {
            AB::AType(element) => f_a(element),
            AB::BType(element) => f_b(element),
        }
    }
}
```

---

## You have to strictly define format of your own data

Python이 생산성이 높다고 다들 말하는 이유 중의 하나는,
Python에서는 데이터의 타입을 loose하게 정의하는 것이 문제가 되지 않기 때문입니다.
다음과 같은 코드를 예로 들겠습니다.

```python
class MyOwnData:
    def __init__(self, max_capacity: int):
        self.max_capacity = max_capacity

    def update(self, new_max_capacity: int, **kwargs):
        if not hasattr(self, "updated_count"):
            self.updated_count = 0
        self.updated_count += 1

        if kwargs.get("add") is True:
            self.max_capacity += new_max_capacity
        else:
            self.max_capacity = new_max_capacity
```

보기만 해도 loose한 코드이지만, 어쨌든 Python에서는 성공적으로 돌아가는 코드입니다.
이 코드에는 다음과 같은 특징이 있습니다.

1. `updated_count` attribute는 오브젝트 생성과정이 아니라 `MyOwnData.update`를 호출한 이후에 생겨난다.
   즉, 런타임에서 `MyOwnData.updated_count`에 대한 엑세스를 시도했을 때 해당 데이터가 없다는 `AttributeError`가 raise될 수 있다.
2. `MyOwnData.update`는 임의의 arbitrary argument를 함수 호출과정에서 허용한다. (`**kwargs`가 그런 문법입니다.)

Rust에서는 이런 것들이 허용되지 않습니다.
`AttributeError` 같은 것들은 emulation이 가능하겠지만 그럴 이유가 별로 없겠죠.
언어를 옮기는 과정에서 이러한 것들은 strict하게 데이터/함수 포맷을 정의해야 합니다.
그리고 당신의 Python 코드가 얼마나 루즈하느냐에 따라서, 그 과정에서 정말 잡다한 많은 것들을 건드려야 할 수도 있습니다.

---

## Lots of boring jobs on exception handling

Rust에서는 프로그램(혹은 쓰레드)을 강제로 종료시키는 [`panic`](https://doc.rust-lang.org/std/macro.panic.html)을 제외하면 *"Error을 raise한다"* 라는 semantic 개념이 언어에 존재하지 않습니다.
Rust에서는 exception들 또한 함수 리턴값의 일부일 뿐이며, 이것은 기존 코드 내에서 error handling을 적은 라인수의 코드로 커버하던 부분이 있었다면 logic migration을 꽤 골치아프게 만듭니다.

특히 퀀트 프로그램 같이 error를 strict하게 분류할 필요성이 있는 프로그램의 경우, 더더욱 작업이 많이 들어갑니다.
저는 일단 [`anyhow`](https://docs.rs/anyhow/latest/anyhow/) 같은 crate를 이용해서 빠르게 에러를 propagate하는 코드를 만든 뒤, 나중에 [`thiserror`](https://docs.rs/thiserror/latest/thiserror/) 같은 crate로 갈아타시는 것을 추천합니다.

!!! references

    Shakacode Blog: [`anyhow` vs `thiserror`](https://www.shakacode.com/blog/thiserror-anyhow-or-how-i-handle-errors-in-rust-apps/)

```python title="Python version"
def f_inner(x: int) -> float:
    if x > 0:
        return 1.0 / x
    else:
        raise ValueError("x should be positive")

def f_outer(start: int, end: int) -> list[float]:
    result: list[float] = []
    for i in range(start, end+1):
        try:
            result.append(f_inner(i))
        except ValueError as err:
            print("Failed at i=%d: %s" % (i, err))
    return result
```

```rust title="Rust version"
fn f_inner(x: i32) -> Result<f64, &'static str> {
    if x > 0 {
        Ok(1.0 / (x as f64))
    } else {
        Err("x should be positive")
    }
}

fn f_outer(start: i32, end: i32) -> Vec<f64> {
    let mut result: Vec<f64> = Vec::new();
    for i in start..=end {
        match f_inner(i) {
            Ok(x) => result.push(x),
            Err(reason) => println!("Failed at i={}: {}", i, reason)
        }
    }
    result
}
```

---

## Decorator becomes tricky

Python에서 편의를 위해 사용하던 일부 패턴이 Rust에서 그대로 사용하기에는 어려운 경우도 있습니다.
가장 대표적인 예시로 [decorator](https://stackoverflow.com/questions/739654/how-do-i-make-function-decorators-and-chain-them-together/1594484#1594484)가 있을 것입니다.

```python title="Python version"
from typing import Callable, ParamSpec, TypeVar

P = ParamSpec("P")
Ret = TypeVar("Ret")

def args_debug(f: Callable[P, Ret]) -> Callable[P, Ret]:
    def decorated(*args: P.args, **kwargs: P.kwargs) -> Ret:
        print("received args: %s, %s" % (args, kwargs))
        return f(*args, **kwargs)
    return decorated

@args_debug
def add(x, y):
    return x+y
```

위의 Python 코드에서 `add(1, 2)`를 실행하면 `received args: (1, 2), {}` 라는 메시지가 콘솔 창에 뜰 것입니다.
`@args_debug`로 인해 `add = args_debug(add)`가 된 것입니다.
Python에서는 함수 또한 궁극적으로 객체이고, 런타임 상에서 함수를 실시간으로 대체하는게 가능하기 때문에 쉽게 적용할 수 있는 패턴입니다.

하지만 Rust에서는 general한 decorator를 구현하는 것이 굉장히 까다롭습니다.
일단 한번 정의한 함수는 바꿀 수 없습니다. 어떤 함수 body 안에서 해당 함수를 wrapping한 다른 함수 객체를 생성하는 것은 가능합니다만..
그런 식으로 하더라도 typing hint를 주는 과정에서 [`Fn` trait](https://doc.rust-lang.org/std/ops/trait.Fn.html) 같은 복잡한 것들을 도입해야 하고,
만약 decorator에 들어갈 함수들의 parameter 타입이 strict하게 고정된 게 아니라면 `Fn`을 generic parameter랑 같이 써야 합니다.

그리고 이마저도 parameter의 개수가 동적이면 거의 불가능에 가까워집니다.
그렇다고 이걸 위해서 전용 [Procedural Macro](https://doc.rust-lang.org/reference/procedural-macros.html)를 만드는 것을 한다면 그것은 배보다 배꼽이 더 큰 일이 될 것입니다.

```rust title="Rust version of naive decorator"
use std::ops::Fn;

fn args_debug<F1>(f: F1) -> impl Fn(i32, i32) -> i32 where
    F1: Fn(i32, i32) -> i32,
{
    move |a: i32, b: i32| {
        println!("received args: a={}, b={}", a, b);
        f(a, b)
    }
}

fn add(a: i32, b: i32) -> i32 {
    a+b
}

fn main() {
    args_debug(add)(1, 2);
}
```

---

## You often have to make your own wrapper

Python의 standard library에는 정말 별의별 유틸리티들이 다 있습니다.
그리고 당신이 당연하게 쓰는 Python 라이브러리에서 구현된 무언가가 Rust에는 구현되지 않은 경우에,
당신은 해당 유틸리티를 직접적으로 구현하거나 third party library를 써야 합니다.
대표적인 예시로 Python에서는 [`datetime`](https://docs.python.org/3/library/datetime.html)이라는 날짜/시간 관련 라이브러리가 기본적으로 제공되지만,
Rust에서는 [`chrono`](https://docs.rs/chrono/latest/chrono/) 같은 라이브러리를 쓰는 것이 사실상 표준입니다.

퀀트 프로그램을 예로 들면, [Binance Vision](https://data.binance.vision/)으로부터 다운받은 `.zip` 파일들을 프로그램에서 직접 unzip하고 CSV파일을 읽어서 각 row를 파싱해서 커스텀한 객체를 만들어 yield하는 프로그램을 만든다고 하면,
Python에서는 [`zipfile`](https://docs.python.org/3/library/zipfile.html)이라는 `.zip` 관련 유틸리티를 제공해주는 standard library가 있고,
[`csv`](https://docs.python.org/3/library/csv.html)라는 CSV reader/writer 관련 유틸리티를 제공해주는 standard library도 있습니다.
그냥 이것들을 가져다 쓰면 됩니다.
하지만 Rust에서는 이것들이 기본으로 제공되지 않고 누군가가 구현해놓은 것들을 가져다 써야 합니다.

[`csv.DictReader`](https://docs.python.org/3/library/csv.html#csv.DictReader)의 경우 class construction에 *"임의의 `str` iterable"* 을 전달받습니다.
그리고 당신이 Python에서 이런 type-erased된 객체를 아주 넓게 사용하고 있었을수록, 컴파일러가 아주 strict한 Rust에 이러한 기능을 도입하는 것에는 시간이 더 걸립니다.
아마도 Rust 컴파일러가 당신의 Python 코드의 일부 로직을 거부할 것이고, 그 거부된 코드들의 타입 시스템이나 기타 등등을 수정하는 데에 적지 않은 시간이 걸릴 것이기 때문입니다.
예를 들어 `csv.DictReader` 같은 걸 구현하기 위해서 Rust에서는 `dyn Iterator<Item=String>` 같은 타입을 도입해야 할 수도 있습니다.

외부 라이브러리를 사용할 경우, 3rd party 도입에 보수적인 회사일수록 이런 식으로 하나하나 기능을 도입하는 것은 일종의 비용이 드는 barrier가 됩니다.
이것은 수많은 C++을 사용하는 회사들을 곧바로 싹 다 Rust 산업계로 옮길 수 없는 이유이기도 합니다.

---

## Some features like [`AsyncIterator`](https://doc.rust-lang.org/std/async_iter/trait.AsyncIterator.html) is still unstable

Python에서 비동기 I/O 프로그램을 만드는 것은 아주 흔한 일입니다.
그리고 그 과정에서 [`collections.abc.AsyncIterator`](https://docs.python.org/3/library/collections.abc.html#collections.abc.AsyncIterator) 같은 추상적인 컨셉 또한 흔하게 채용해서 사용할 것입니다.
하지만 Rust에서는 언어 차원에서의 비동기 프로그래밍 관련 서포트가 완벽하게 성숙되지 않았습니다.
대표적으로 [`AsyncIterator` (trait)](https://doc.rust-lang.org/std/async_iter/trait.AsyncIterator.html)은 아직 nightly에서만 사용이 가능합니다.
퀀트 프로그램의 경우 exchange adapter들이 거래소랑 지속적으로 통신해서 데이터를 받아올 건데, 그것들을 graceful하게 구현할 수 있는 `AsyncIterator` 같은 feature들이 stable로 옮겨지는 것이 매우 반가울 것입니다.

이뿐만이 아닙니다. Rust에서는 `async fn`을 가지는 `trait`이 [`object-safe`](https://doc.rust-lang.org/reference/items/traits.html#object-safety)하지 않습니다.
비동기 함수를 가지고 있는 trait을 dyn casting하는 것이 금지된다는 거죠. 이건 타격이 좀 큽니다.
물론 이 건에 대해서는 [`async_trait`](https://docs.rs/async-trait/latest/async_trait/)이라는 crate가 현재 커버를 쳐주고 있긴 합니다.

이런 식으로 `Rust`에서는 stable한 코드 안에서 Python에서는 쉽게 구현할 수 있던 어떤 일련의 컨셉을,
Rust 언어 차원에서의 서포트 부족 내지는 한계 때문에 구현하기가 힘들거나 혹은 빙빙 돌아야 하는 귀찮은 케이스들이 종종 존재합니다.

---

이상으로 Python 코드를 Rust로 옮기는 과정에서 나타날 수 있는 장애물들에 대해 알아보았습니다.
글을 읽어주셔서 감사합니다.
