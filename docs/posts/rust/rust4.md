---
categories:
  - Rust
tags:
  - rust
  - python
  - programming
  - computer-science
  - poker
title: RUST 4. Implementing Poker Analysis Library (Rust Part)
---

안녕하세요.

이번에는 포커 토너먼트 분석툴을 만들어본 경험을 풀어보려고 합니다.
제 포커 토너먼트 분석툴은 GGNetwork의 Pokercraft에서 다운로드 받을 수 있는 데이터를 분석하는 툴로, 그 툴로 만든 분석파일들은 다음과 같습니다.

- [토너먼트 결과 분석](/assets/raw_html/damavaco_performance_kr.html)
- [핸드 히스토리 분석](/assets/raw_html/damavaco_handhistories_kr.html)

취미 프로젝트 치고는 코딩을 꽤 많이 한 편이라, 글로 풀어보고 싶었습니다.
이 글에서는 그 중 Rust와 연관이 있는 부분만 골라서 풀어보겠습니다.

<!-- more -->
---

## Parallel computing

러스트 모듈에 있는 거의 모든 헤비한 연산들은
[`rayon`](https://github.com/rayon-rs/rayon)의 병렬 컴퓨팅을 활용하도록 구현되었습니다.
이 과정에서 `&mut T` 같은 변수들을 `for_each`의 closure에 캡쳐할 수 없는 등등의 삽질을 겪었네요.

```rust
// Code provided by Google AI

use rayon::prelude::*;

fn main() {
    let mut total = 0;
    let numbers = vec![1, 2, 3, 4, 5];

    // This will result in a compile error
    numbers.par_iter()
           .for_each(|&x| {
               total += x; // ERROR: Cannot capture `total` as mutable
           });
}
```

---

## Bankroll analysis

[뱅크롤 분석](../../alds/7/#monte-carlo-analysis)을 Python 단에서 진행하기에는 연산량이 너무 많았기 때문에 [Rust 모듈](https://github.com/McDic/pokercraft-local/blob/f58b2b59935813a9be3a739b6a6336eae43fc552/pokercraft_local_rust/lib/bankroll.rs#L125-L168)에서 구현했습니다.

---

## All-in equity calculation

포커에서 올인을 하게 되면, 정확한 결과값을 계산하는 방법은 가능한 모든 보드에 대해서 승패를 시뮬레이션을 하는 것입니다.
프리플랍 헤즈업 올인의 경우, 가능한 보드의 개수는 약 171만개입니다.
병렬 컴퓨팅을 활용하긴 하는데, 그렇게 하더라도 여전히 프리플랍 올인을 매번 계산하는 것은 정말 빡세기 때문에, 최소한 HU(헤즈업) 시나리오에 대해서는 cache를 만들기로 했습니다.

HU preflop cache를 만들 때 [suit-symmetric한 시나리오는 제외](https://github.com/McDic/pokercraft-local/blob/f58b2b59935813a9be3a739b6a6336eae43fc552/pokercraft_local_rust/bin/generate_preflop_cache/main.rs#L19-L42)하고 계산하기로 했습니다.
예를 들어서 AsKs vs QsJs의 확률은 AdKd vs QdJd의 확률과 동일합니다.
이런 중복된 시나리오는 제거하는 것입니다.

!!! references

    계산된 cache는 [여기](https://github.com/McDic/pokercraft-local/blob/master/pokercraft_local/hu_preflop_cache.txt.gz)에서 다운받으실 수 있습니다.

    `.gz` 압축을 해제하면 `.txt` 파일이 나오는데,
    매 라인마다 "*핸드1 vs 핸드2 = 핸드1승리횟수 핸드2승리횟수 무승부횟수*"가 써져 있습니다.

---

## Scientific libraries

FFT, Gaussian CDF 역함수 계산 등을 할 때 이미 구현된 라이브러리들을 가져와서 썼습니다.

- [RustFFT](https://github.com/ejmahler/RustFFT): [`LuckCalculator::convolve_real`](https://github.com/McDic/pokercraft-local/blob/f58b2b59935813a9be3a739b6a6336eae43fc552/pokercraft_local_rust/lib/equity.rs#L512-L563)
- [statrs](https://github.com/statrs-dev/statrs): [`LuckCalculator::luck_score`](https://github.com/McDic/pokercraft-local/blob/f58b2b59935813a9be3a739b6a6336eae43fc552/pokercraft_local_rust/lib/equity.rs#L495-L510)

---

## Self utilities

### Iterator wrapper

`Box<dyn Iterator<Item = T>>`는 `rayon::iter::ParallelBridge`를 impl하지 않습니다.
그래서 임의의 [iterator를 래핑하는 struct](https://github.com/McDic/pokercraft-local/blob/f58b2b59935813a9be3a739b6a6336eae43fc552/pokercraft_local_rust/lib/utils.rs#L64-L80)를 구현했습니다.

### Fixed sized combination

[`itertools::combinations`](https://docs.rs/itertools/latest/itertools/trait.Itertools.html#method.combinations)는 iterator element type이 `Vec<T>`입니다.

저는 `rayon`을 통해 실행되는 매 루프에서 작은 allocation이 자주 일어나지 않기를 원했습니다.
그래서 그런 코드를 작성하는 과정에서 [`FixedSizedCombinationIterator<T, K>`](https://github.com/McDic/pokercraft-local/blob/f58b2b59935813a9be3a739b6a6336eae43fc552/pokercraft_local_rust/lib/utils.rs#L1-L62)를 만들었습니다.
이 struct는 iterator element type이 `[T; K]`입니다.

---

다른 파트들은 다음 글에서 읽으실 수 있습니다.

- [파이썬 파트](../../py/5)
- [알고리즘 파트](../../alds/7)

글을 읽어주셔서 감사합니다.
