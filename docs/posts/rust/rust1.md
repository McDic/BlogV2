---
categories:
  - Rust
tags:
  - rust
  - programming
  - computer-science
title: RUST 1. Rust's Disadvantages in My Opinion
---

안녕하세요. 이번 시리즈에서는 Rust에 관한 이것저것을 다루고자 합니다.
시리즈의 첫 글로는 좀 민망한 주제일 수 있지만, 제가 생각하는 러스트의 단점에 대해 얘기해보고자 합니다.

Rust 관련 커뮤니티를 돌아다니다보면 Rust가 모든 방면에서 만능인 언어라고 생각하는 사람이 많습니다.
어떤 국내 카톡방에서는 Rust가 대한민국에서 개발자 취업을 하는 빠른 길이라고 주장하시는 분도 계셨고..
최근 회사에서는 회사의 모든 스택들.. Rust가 생산성이 좋기 때문에 심지어 프론트엔드까지 Rust로 만들어야 한다고 주장하는 인턴분도 계셨습니다.

정작 그런 분들하고 자세히 Rust를 얘기하다보면 Rust로 개발하는 과정에서 나타나는 병목들을 잘 모르시더군요.
저라고 뭐 만능 프로그래머는 아니지만, Rust로 개발하다가 불편함이 느껴진 부분이 종종 있었습니다.
이 글에서는 그런 부분들에 대해서 소개하고자 합니다.

!!! warning

    미래에 가끔 또 생각나는 단점들이 있으면 글을 업데이트할 수 있습니다.

<!-- more -->
---

## Async trait is not [object safe](https://doc.rust-lang.org/beta/reference/items/traits.html#object-safety)

어떤 trait `A`가 object safe하다는 것은, 해당 `A`를 구현하는 임의의 구조체를 `dyn` keyword로 casting하는 것이 가능하다는 것을 의미합니다. 이것을 [`Trait object`](https://doc.rust-lang.org/beta/reference/types/trait-object.html)라고 합니다.

현재 `async fn`을 가지는 trait은 object safe하지 않습니다.
왜냐하면 `async fn`은 해당 함수를 호출했을 때 암시적으로 [`impl Future`](https://doc.rust-lang.org/std/future/trait.Future.html)를 반환하기 때문이며, `impl Future`은 opaque type으로 취급되기 때문입니다.

`async fn in trait`이 unstable한 상태에서 stable한 feature로 바뀐 지 얼마 되지 않긴 했지만, 비동기 프로그래밍 관련 trait을 직접 `dyn` casting하고 싶을 때 그걸 못하는 것은 때때로 불편한 상황을 마주하게 됩니다.

그나마 다행인 것은 `async fn in trait`이 stable해지기 전부터 유명했던 [`async_trait`](https://crates.io/crates/async-trait)이라는 crate가 관련 기능을 간접적으로 제공해준다는 것입니다.

---

## Lack of negative trait bounds

Rust에서는 generic 상에서 어떤 type parameter가 가지는 제약을 걸고 싶을 때 trait bound를 사용합니다. 다음 코드처럼요.

```rust
trait SomeTrait {}

fn f<T, const S: usize>(value: T) -> [T; S] where T: SomeTrait {
    todo!()
}
```

하지만 이런 식으로 특정 trait을 피하는 제약을 거는 것은 안 됩니다.

```rust
// COMPILE ERROR
// negative bounds are not supported
trait SomeTrait {}

fn f<T, const S: usize>(value: T) -> [T; S] where T: !SomeTrait {
    todo!()
}
```

이와 관련해서 아직 unstable한 feature로 [negative impl](https://www.reddit.com/r/rust/comments/15wf3qv/why_doesnt_rust_have_negative_trait_bounds/)이 있지만, Stable Rust에는 아직 해당 기능을 사용할 수 없습니다.

C++에서는 [`std::enable_if`](https://en.cppreference.com/w/cpp/types/enable_if) 또는 [`concept`](https://en.cppreference.com/w/cpp/language/constraints)이 있고, 임의의 boolean을 사용할 수 있기 때문에 이러한 negative trait bound 같은 semantic을 구현하는 것이 아주 자유롭습니다.

물론 Rust에서 아직 이런 기능을 제공하지 않는 배경에는 많은 이론적 복잡함이 있겠지만, 어쨌든 사용자 입장에서는 꽤 불편한 부분이긴 합니다.

---

## Orphan rule is sometimes not comfortable

Orphan rule은 어떤 foreign struct의 foreign trait impl을 본인의 crate에서 만들 수 없게 하는 Rust의 규칙입니다.
이 규칙이 있는 이유는, orphan rule이 없으면 여러 crate 상에서 dependency가 생길 때 같은 trait에 대한 서로 다른 impl들이 충돌하여 컴파일 에러를 낼 수 있기 때문입니다.

!!! references

    읽어보면 [좋은 레딧 글](https://www.reddit.com/r/rust/comments/b4a4fu/what_are_the_technical_reasons_for_the_orphan_rule/)을 하나 소개해드립니다.

그러나 orphan rule이 항상 반가운 것은 아닙니다.
둘 이상의 external crate을 사용하는데 한 crate의 struct을 다른 crate의 trait에 대해 구현하고 싶을 때 가끔 난감한 상황이 옵니다.
물론 이를 위해 "wrapping trait"을 작성할 수 있으나, 좀 번거롭습니다.

---

## Const generics evaluation is not supported yet

Rust에서 generic으로 쓸 수 있는 것은 type generic 뿐만 아니라 const generic도 있습니다.
하지만 const generic 값을 함수나 구조체 안에서 단순히 활용하는 것 이외에 어떤 제약이나 다른 type hint을 생성해내는 것은 불가능합니다.

```rust
// COMPILE ERROR
// generic parameters may not be used in const operations
fn f<const N: usize>() -> [u8; N + 1] {
    [0; N + 1]
}
```

!!! references

    Rust compiler team의 proposal 중 하나인 ["Const well-formedness and const equality"](https://hackmd.io/OZG_XiLFRs2Xmw5s39jRzA?view#Const-equality)에서 발췌한 코드입니다.

그래서 이런 코드도 안 됩니다.

```rust
// COMPILE ERROR
// expected one of `,`, `.`, `>`, `?`, or an operator, found `)`
fn f<const L: usize>() -> () where L < 100 {
    todo!()
}
```

이것 또한 C++에서는 위에서 언급한 [`concept`](https://en.cppreference.com/w/cpp/language/constraints) 등으로 쉽게 구현이 가능하지만, Rust에서는 아직 불가능합니다.

---

## [Procedural macros](https://doc.rust-lang.org/reference/procedural-macros.html) should be in a separated crate

Proc macro란 Rust 상의 token stream(`TokenStream`)을 또 다른 token stream으로 바꿔주는 함수를 제공함으로써 작동하는 매크로를 말합니다.
사실상 어떤 AST를 다른 AST로 바꿔주는 기능을 하는 셈입니다.
실제로 몇몇 복잡한 proc macro는 사실상 Rust 상에 존재하는 또 다른 언어처럼 작동합니다.

Proc macro를 제공하는 crate은 항상 독립적이어야 합니다.
이런 crate의 대표적인 예시로 [`rust_decimal`](https://docs.rs/rust_decimal/latest/rust_decimal/)의 macro를 제공하는 [`rust_decimal_macros`](https://docs.rs/rust_decimal_macros/latest/rust_decimal_macros/)가 있습니다.
이는 어떤 기능을 제공하는 crate가 유저들에게 개발 편의성을 위해 proc macro를 제공하려면 또 다른 제 2의 crate를 별도로 만들어서 배포해야 한다는 것입니다.

별로 크리티컬한 문제점은 아니라고 생각하지만 왜 이런 제약이 있는지 저는 잘 모르겠습니다.

---

## Some limitations on famous libraries

- Python과 Rust을 이어주는 것으로 유명한 라이브러리 [`PyO3`](https://pyo3.rs)에서는 generic parameter function을 Python interface에 노출시키는 것이 불가능합니다.

    !!! references

        [PyO3 Limitations](https://pyo3.rs/v0.21.2/class#no-generic-parameters)

- 가장 유명한 Rust ORM 라이브러리 중 하나인 [`diesel`](https://diesel.rs)에서는 async connection을 공식적으로 지원하지 않습니다.
    [`diesel-async`](https://crates.io/crates/diesel-async)라는 crate가 diesel 제작자에 의해 만들어지긴 했으나 아직 공식적으로 organization repo로 편입되지는 않았습니다.

Rust는 나름 젊은 언어이기 때문에 아직 라이브러리 생태계가 C++이나 Python만큼 방대하지 않으며, 유명한 오픈소스 라이브러리들도 종종 한계점이 있는 부분들이 있습니다.

---

이외에도 컴파일러의 strictness 때문에 유연한 개발이 필요한 회사 초기 프로토타입에 적합하지 않은 경우가 있다던가, 여러 문제점이 있을 것입니다.

저는 Rust를 좋아하지만, 언어 그 자체와 사랑에 빠지는 것을 경계하는 편입니다.
Rust 언어 생태계에는 무슨 이유에서인지 러스트가 만능이라는 식으로, 제대로 러스트를 이해하려고 하지도 않은 채 언어와 사랑에 빠진 힙스터들이 많습니다.
하지만 언어를 좋아하더라도 장단점은 분명히 인지하고 사용해야 한다고 생각합니다.

글을 읽어주셔서 감사합니다.
