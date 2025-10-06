---
categories:
  - Python
tags:
  - python
  - programming
  - computer-science
  - poker
title: PY 5. Implementing Poker Analysis Library (Python Part)
---

안녕하세요.

이번에는 포커 토너먼트 분석툴을 만들어본 경험을 풀어보려고 합니다.
제 포커 토너먼트 분석툴은 GGNetwork의 Pokercraft에서 다운로드 받을 수 있는 데이터를 분석하는 툴로, 그 툴로 만든 분석파일들은 다음과 같습니다.

- [토너먼트 결과 분석](/assets/raw_html/damavaco_performance_kr.html)
- [핸드 히스토리 분석](/assets/raw_html/damavaco_handhistories_kr.html)

취미 프로젝트 치고는 코딩을 꽤 많이 한 편이라, 글로 풀어보고 싶었습니다.
이 글에서는 그 중 Python과 연관이 있는 부분만 골라서 풀어보겠습니다.

<!-- more -->
---

## [`Plotly`](https://plotly.com/python/) - Graphing tool

제가 과거 퀀트 회사들에 근무할 때 썼던 이후로 파이썬에서 차트를 그린다고 하면 거의 항상 [`Plotly`](https://plotly.com/python/)를 사용하는 것 같습니다.
Plotly는 다양한 차트를 HTML에 그려주는 것을 지원하며, [`pandas`](https://pandas.pydata.org/), [`numpy`](https://numpy.org/) 등의 유명한 과학/수치 라이브러리하고도 유연하게 같이 사용될 수 있어 편합니다.

??? caption "Pictures"

    ![linecharts](/assets/posts/py/poker_analysis/plotly_linecharts.png)

    !!! caption

        Plotly를 통해 그린 Line chart들입니다.

    ![heatmaps](/assets/posts/py/poker_analysis/plotly_heatmaps.png)

    !!! caption

        Plotly를 통해 그린 Heatmap과 Marginal distribution입니다.

    ![barcharts](/assets/posts/py/poker_analysis/plotly_barcharts.png)

    !!! caption

        Plotly를 통해 그린 Bar chart입니다.

    ![piecharts](/assets/posts/py/poker_analysis/plotly_piecharts.png)

    !!! caption

        Plotly를 통해 그린 Pie chart들입니다.

    이외 다양한 차트들이 분석 결과 html 파일에 있습니다.

---

## [`PyO3`](https://pyo3.rs/) and [`maturin`](https://maturin.rs/) - Using Rust in Python

Python은 성능 크리티컬한 코드를 돌리는 것에는 부적합합니다.
그래서 Rust로 성능 크리티컬한 모듈들을 작성하고, 그것을 `PyO3`와 `maturin`을 통해서 [Python 인터페이스로 export](https://github.com/McDic/pokercraft-local/blob/f58b2b59935813a9be3a739b6a6336eae43fc552/pyproject.toml#L50-L57)했습니다.

Rust 파트에 대한 글은 [여기](../../rust/4)를 참조해주세요.

---

## [`tkinter`](https://docs.python.org/3/library/tkinter.html) - GUI

[`tkinter`](https://docs.python.org/3/library/tkinter.html)는 Tcl/Tk GUI의 Python wrapper이자 standard library입니다.
프론트엔드쪽 스킬은 제가 좀 부족해서 그냥 빠르게 땜빵할 수 있는 GUI를 만들기로 했습니다.
언젠가 나중에 웹으로 UI를 바꿀 수도 있지만, 수고가 상당히 많이 들어가는 영역이기 때문에 쉽게 시작하진 못할 거 같네요.

!!! references

    [pokercraft_local/gui.py](https://github.com/McDic/pokercraft-local/blob/master/pokercraft_local/gui.py)

---

## Self utilities

### Alternatives to [`functools.cache`](https://docs.python.org/3/library/functools.html#functools.cache)

[`functools.cache`](https://docs.python.org/3/library/functools.html#functools.cache)는 어떤 함수가 파라미터에 따른 결과값을 캐시에 저장하도록 하여, 똑같은 파라미터로 호출을 여러 번 하였을때 동일한 연산을 여러 번 시행하지 않도록 하는 decorator입니다.

하지만 클래스의 메소드에 사용될 때 `self`까지 같이 캐시에 넣는다는 단점이 있습니다.
`Self` 타입이 `__hash__`를 지원하지 않으면 문제가 생기므로, 저는 이것을 [`id(self)`를 해시하도록 대체하는 `decorator`](https://github.com/McDic/pokercraft-local/blob/f58b2b59935813a9be3a739b6a6336eae43fc552/pokercraft_local/utils.py#L38-L62)를 만들었습니다.

---

다른 파트들은 다음 글에서 읽으실 수 있습니다.

- [알고리즘 파트](../../alds/7)
- [러스트 파트](../../rust/4)

글을 읽어주셔서 감사합니다.
