---
categories:
  - Rust
tags:
  - rust
  - programming
  - computer-science
  - quant
title: RUST 2. Type Hints for Async Closures
---

최근에 자동매매 프로그램을 Rust로 코딩해보면서 몇몇 점들에 부딪혔었는데, 그 삽질 과정을 블로그에 남겨보고자 합니다.
바로 직전에 잠깐 있었던 회사에서 Rust로 코딩했을 때도 있었던 문제였으며(그 회사는 당시 legacy platform에서 이 문제를 피하기 위해 naive한 디자인을 선택했습니다),
굳이 퀀트가 아니더라도 Rust로 서로 다른 네트워킹 프로토콜을 한 컨테이너에 보유하는 것을 런타임에 가능하게 하고자 하는 모든 분들이 아마 어떤 식으로든 마주했을 문제라고 생각합니다.

!!! info

    지금 자동매매 프로그램을 짜는 것은 진지하게 트레이딩을 해보자는 것보다는 개발에 대한 감을 잃지 않고 유지하고자 하는 것에 더 가깝습니다.
    만약 자동매매 프로그램을 계속 오랫동안 짜게 될 경우, 이러한 글들을 위한 "QUANT" 시리즈를 따로 만들고 그런 글들을 해당 시리즈에 넣을 가능성이 있습니다.

<!-- more -->
---

## The goal

!!! abstract

    **서로 다른 "같은 인터페이스의 async 기능들"을 제공하는 struct들을 한 container에서 묶어서 관리하고 싶습니다.**

자동매매 프로그램에서 파이썬으로 비슷한 방식의 코드들을 들어봅시다.

```python
from dataclasses import dataclass
from typing import AsyncGenerator

@dataclass
class Trade: ...

@dataclass
class OrderRequest: ...

@dataclass
class OrderResponse: ...

class Adapter:
    def __init__(self): ...
    async def send_new_order(self, request: OrderRequest) -> OrderResponse: ...
    async def get_trades_forever(self) -> AsyncGenerator[Trade, None]: ...

class TradingPlatform:
    adapters: dict[str, Adapter]
    ...
```

대충 이런 느낌일 겁니다.
전략에서는 어떤 거래소로 어떤 주문요청을 보낼 지를 알려주면, 해당 거래소의 adapter를 불러내서 해당 요청을 쏴주는거죠.
여기서 `Adapter`는 일련의 "set of async functionalities"를 제공합니다.
주문을 보내고 응답을 받고, 웹소켓으로 이런저런 데이터를 주기적으로 받고.. 하는 식이죠.

!!! warning

    모든 트레이딩 프로그램이 무조건적으로 이러한 디자인을 따라야 한다는 것은 아닙니다.

하지만 이러한 디자인을 컴파일 언어에서 구현하는 것은, 특히 Rust에서 구현하는 것은 꽤 빡셉니다.
왜 그럴까요?

---

## Trait with async method is not object safe

Rust에서 저런 공통적인 인터페이스를 가지는 무언가를 개발한다면 십중팔구 [trait](https://doc.rust-lang.org/book/ch10-02-traits.html)을 사용할 것입니다.
`Adapter`는 trait이 되고, 각종 거래소를 위한 individual implementation이 `Adapter`를 impl하는 struct가 되겠죠.
따라서 아마 위 파이썬 코드를 러스트로 변환하게 된다면 (rough하게) 다음과 같은 느낌이 들 겁니다.

```rust
struct OrderRequest {}
struct OrderResponse {}

trait Adapter:
    async fn send_new_order(&self, request: OrderRequest) -> OrderResponse;
```

!!! info

    Rust에서 [`AsyncIterator`](https://doc.rust-lang.org/std/async_iter/trait.AsyncIterator.html)는 아직 unstable합니다.
    그래서 Stable Rust에서 Python의 `AsyncGenerator[Trade, None]`과 같은 type hint를 주려면 별도의 wrapper struct 같은 걸 만들던지 하여간 뭔가 복잡하게 해야 하는데,
    그건 지금 글에서 다루는 내용을 벗어나므로 `get_trades_forever`를 `Adapter`의 method 목록에서 제거했습니다.

하지만 `async fn`을 가지고 있는 trait은 [object-safe](https://doc.rust-lang.org/reference/items/traits.html#object-safety)하지 않습니다.
왜냐하면 `T`를 return하는 `async fn`은 암시적으로 `impl Future<Output = T>`를 return하기 때문이며, `impl Future`는 opaque type이기 때문입니다.
어떤 trait이 object-safe하지 않다는 것은, 해당 trait을 `dyn` casting 할 수 없다는 뜻이며, 다음과 같은 코드를 컴파일하는 것이 불가능하다는 것을 의미합니다.

```rust
// COMPILE ERROR
// error[E0038]: the trait `NotObjectSafeTrait` cannot be made into an object

trait NotObjectSafeTrait {
    async fn incremented(&self, number: i32) -> i32;
}

async fn wow(something: Box<dyn NotObjectSafeTrait>, number: i32) -> i32 {
    something.incremented(number).await
}
```

그래서 저는 이 지점에서 고민을 하다가 생각했습니다.

!!! quote

    그렇다면 `async fn` 그 자체를 return하면 되는 것이 아닌가?

그리고 저는 이것을 시도해보기로 했고, 고생길의 시작에 올랐습니다.

---

## Type hints for async closure is hard

하지만 `impl Future`를 return하는 어떤 closure에 대한 type hint를 주는 것은 상당히 빡셌습니다.
다음과 같은 Rust 코드를 생각해봅시다. 저 `???`에는 어떤 타입을 넣어야 할까요?

```rust
fn wow(message: String) -> ??? {
    |destination: String| async move { format!("{}: {}", destination, message) }
}
```

먼저 모든 closure는 기본적으로 anonymous type을 가지고 있습니다.
Rust에서 그 어떤 closure도 해당 객체의 "정확한" 타입을 explicit하게 코드 상에서 명시하는 것은 불가능합니다.
하지만 모든 closure는 `Fn` trait을 구현하니까, `???`에다가 `impl Fn(...) -> ...`을 넣으면 되지 않을까요?
`impl Trait`을 trait method의 return type으로 넣으면 object safety가 깨지는 것은 둘째 치고, 또 다른 문제가 있습니다.

### `impl Fn(...) -> impl Trait` is not stable yet

async block(위 코드 상의 `async move {...}`에 해당하는 부분)은 기본적으로 [`std::future::Future`](https://doc.rust-lang.org/std/future/trait.Future.html)를 impl하는 anonymous struct입니다.
이것은 해당 block의 type을 `impl Future<Output = ...>`로 표현해야 함을 의미합니다.
그러면 위 코드의 `fn wow`는 다음과 같이 되는데요.
하지만 다음 코드는 컴파일 에러를 발생시킵니다.

```rust
// COMPILE ERROR
// error[E0562]: `impl Trait` is not allowed in the return type of `Fn` trait bounds

use std::future::Future;

fn wow(message: String) -> impl Fn(String) -> impl Future<Output = String> {
    |destination: String| async move { format!("{}: {}", destination, message) }
}
```

관련 사항은 [rust-lang/rust#93582](https://github.com/rust-lang/rust/pull/93582)에서도 논의된 바 있습니다.
현재 `impl trait in fn trait`은 `#![feature(impl_trait_in_fn_trait_return)]`를 활성화시킨 상태에서만 가능하며, Stable Rust에서는 지원되지 않습니다.
따라서 async closure에 대한 type hint를 주기 위해서는 다음 코드와 같이 별도의 wrapper trait을 만들어야 하죠.

```rust
use std::future::Future;

trait AsyncFn3<A, B, C>: Fn(A, B, C) -> <Self as AsyncFn3<A, B, C>>::Future {
    type Future: Future<Output = Self::Out>;

    type Out;
}

impl<A, B, C, Fut, F> AsyncFn3<A, B, C> for F
where
    F: Fn(A, B, C) -> Fut,
    Fut: Future,
{
    type Future = Fut;

    type Out = Fut::Output;
}

fn async_closure() -> impl AsyncFn3<i32, i32, i32, Out = u32> {
    |a, b, c| async move { (a + b + c) as u32 }
}
```

!!! references

    [rust-lang/rust#93582](https://github.com/rust-lang/rust/pull/93582)의 작성자의 [예시 코드](https://github.com/rust-lang/rust/pull/93582#issue-1121860543)를 가져온 것입니다.

---

## Decided to use `Box`

그래서 위 코드를 참조한 wrapper struct를 만들다가, 계속 컴파일 오류의 늪에 빠지고..
도저히 답이 안 보여서 Rust User Forum에 [질문글](https://users.rust-lang.org/t/having-trouble-on-making-async-callable-wrapper/112668/7)을 올렸습니다.
디자인을 바꿀까 `Box`를 사용할까 고민을 많이 했는데, 일단은 `Box<dyn Fn(..) -> Box<dyn Future<Output = ..>>>`를 쓰기로 했습니다.
그 결과가 다음 코드입니다.

```rust
/// BAM is an abbreviated name of "BoxedAsyncMethod".
/// It represents an async method that gets one
/// parameter and returns a boxed async future.
pub type BAM<'se, T, R> = Box<dyn Fn(T) -> Box<dyn Future<Output = R> + 'se> + 'se>;

/// Similar to `Into<BAM<..>>`.
pub trait IntoBAM<'se, T, R> {
    /// Convert this object into `BAM`.
    fn into_bam(self) -> BAM<'se, T, R>;
}

impl<'se, T, R, C, Fut> IntoBAM<'se, T, R> for C
where
    C: Fn(T) -> Fut + 'se,
    Fut: Future<Output = R> + 'se,
{
    fn into_bam(self) -> BAM<'se, T, R> {
        Box::new(move |parameter: T| Box::new(self(parameter)))
    }
}

// ...

pub trait Protocol {
    fn new_order_sender<'se, 'des>(
        &'se self, destination: &'des String,
    ) -> BAM<'se, String, String> where 'des: 'se;
}
```

이제 `Protocol`은 object safe하며, async closure를 return할 때 통째로 괄호로 감싼 후 `.into_bam()`만 해주면 됩니다.
하지만 이 디자인에 대해서 지금 생각날만한 문제점 몇 가지가 있습니다.

첫 번째는 actor를 자주 생성할수록 heap allocation이 더 높은 빈도로 나타난다는 것입니다.
작은 Heap allocation이 자주 일어나는 것은 소프트웨어의 performance에 큰 영향을 미친다는 점을 감안할 때, 극한의 퍼포먼스가 필요한 상황이 (있을 지는 모르겠으나) 생기면 개별 actor를 메시지를 보낼 때마다 생성하지 않고 1번만 생성하여 재활용해야 할 수도 있을 것 같습니다.

두 번째는 아주 명확하진 않은데 closure가 캡쳐하는 변수와 라이프타임, `&mut` 유무에 따라 해당 trait의 인터페이스가 더 복잡해질 수 있을 것 같습니다.
당장 `Protocol::new_send_order`만 봐도 `destination`을 closure 안에 안전하게 캡쳐하기 위해 `'des: 'se`라는 제약을 부여하였습니다.
이건 더 개발해봐야 알 것 같습니다.

!!! info

    두 번째 문제점에 의해 복잡해진 인터페이스는 당장 첫 번째 문제점에서 이야기한 잠재적 해법인 "개별 actor를 캐싱한다"와 정면으로 충돌합니다.
    프로그램의 시작부터 종료까지 거의 살아있는 actor보다 오래 사는 lifetime은 `'static`이거나 그에 준하는 수준밖에 없을 것이며,
    이는 그러한 캐싱된 actor들에 넣는 보조 parameter들의 범위에 제약이 크게 들어간다는 것을 의미합니다.

---

지금까지 저의 Rust 삽질 일기였습니다.
읽어주셔서 감사합니다.
