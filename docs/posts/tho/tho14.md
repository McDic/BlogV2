---
categories:
    - Thoughts
tags:
    - ai
    - computer-science
title: THO 14. Intelligence at the Different Complexity
---

요즘 인공지능의 발전속도가 정말 어마무시합니다.
신경망 모델이 개발된 이래,
바둑 인공지능 [AlphaGo](https://deepmind.google/research/breakthroughs/alphago/),
단백질 구조 예측모델 [AlphaFold](https://deepmind.google/technologies/alphafold/),
자연스러운 챗봇 [ChatGPT](https://openai.com/index/chatgpt/),
이미지/동영상 생성모델 [Stable Diffusion](https://stability.ai/),
작곡 인공지능 [Suno](https://suno.com/)
등의 다양한 모델들이 최근 10년 동안 어마무시하게 쏟아져나오고 발전했습니다.

저는 이러한 인공지능 기술들이 무시무시하게 빠르게 발전하는 것을 보면서 여러 생각을 개인적으로 해왔는데,
이번 기회에 그것들을 블로그에 글로 정리해보고자 합니다.

!!! disclaimer

    저는 인공지능 전문가가 아닙니다.
    그래서 제 글의 여러 디테일들에 틀린 부분이 있을 수 있습니다.

<!-- more -->
---

## The giga impact is already started

인공지능은 이미 일반인들조차 널리 사용하기 시작했습니다.
현재 가장 자주 보이는 것들은 아마도 창작 분야일 것입니다.

![japanese_shrine](/assets/posts/tho/high_intelligence/japanese_shrine.webp)

!!! caption

    [GPT 4o mini](https://openai.com/index/gpt-4o-mini-advancing-cost-efficient-intelligence/)
    에게 직접 요청해서 그린 일본식 신사 그림입니다.

<iframe width="100%" height="166" scrolling="no" frameborder="no" allow="autoplay" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/1973905099&color=%2328b928&auto_play=false&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true"></iframe>

!!! caption

    [Suno AI](https://suno.com/song/c05ba919-9fd6-4267-9bae-d110f2fe3d38)
    에게 직접 요청해서 만든 노래입니다.
    가사는 ChatGPT를 통해 교정했습니다.

<iframe width="100%" height="315" src="https://www.youtube.com/embed/J9DpusAZV_0?si=aO-PGcerJ_-gfP0Q" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

!!! caption

    일본의 Wit Studio가 2023년 1월 Netflix Japan을 통해 공개한 *"개와 소년"*이라는 애니메이션입니다.
    이 애니메이션의 배경 작화는 전부 인공지능이 담당하였습니다.

이미 Suno 등의 생성형 인공지능으로 창작을 할 수 있는 서비스를 제공하는 회사들은 소니(Sony Music Entertainment), 유니버설(Universal Music Group) 등의 굵직한 기업들로부터
[줄소송](https://www.musicbusinessworldwide.com/suno-after-being-sued-by-the-majors-and-hiring-timbaland-as-strategic-advisor-preps-launch-of-v4-claimed-to-be-a-new-era-of-ai-music-generation12/)
을 당하고 있습니다.

그렇다면 인공지능이 창작 분야에서만 강력한 것일까요?
프로그래밍 분야에서도 이미 엄청난 영향을 끼치고 있습니다.
저는 개인적으로 ChatGPT, Suno 뿐만 아니라 [Github Copilot](https://github.com/features/copilot)
등의 코딩을 도와주는 인공지능 툴도 유료 구독하고 있습니다.

![copilot_chat](/assets/posts/tho/high_intelligence/copilot_chat.png)

!!! caption

    이 문서의 프롤로그의 초기 버젼을 작성한 직후 Copilot에게 문서의 내용을 요약해달라고 한 대화입니다.

![chatgpt_partial_derivative](/assets/posts/tho/high_intelligence/chatgpt_partial_derivative.png)

!!! caption

    [ChatGPT o1](https://openai.com/o1/)에게
    [정규분포](https://en.wikipedia.org/wiki/Normal_distribution) 확률밀도함수를 평균값에 대해 편미분해달라고 요청했고,
    o1은 계산과정을 하나하나 보여주면서 이 모든 과정을 잘 해냈습니다.

과학/연구 분야도 예외가 아닙니다.
2024년 노벨물리학상과 노벨화학상은 AI 연구를 통해 과학 연구에 크게 기여한 사람들이 수상하였습니다.

!!! references

    출처: [동아사이언스 2024년 10월 23일 기사](https://m.dongascience.com/news.php?idx=68071)

인공지능 기술은 그것이 끝까지 발전하지 않고 아직 개선될 여지가 많이 남아있음에도 불구하고,
기존에 인간이 하던 지적인 일들의 상당량을 해치움으로써 생산성을 극대화하고 있습니다.
이것은 여태까지 기술이 인간 사회에 가져온 발전들과는 다른 차원의 것입니다.
기계는 인간의 육체적 노동을 대체하고, 단순한 지적 노동을 대체했습니다.
그리고 이제 저는 기계가 인간의 **모든 지적인 노동을 완벽하게 대체**할 날이 얼마 남지 않았다고 확신하고 있습니다.

!!! info

    여기서 제가 언급한 *"단순한 지적 노동"*이란,
    인간이 비록 속도가 몇 백만배 느리더라도, **모든 프로시져(procedure)를 엄밀하게 표현할 수 있고, 그 프로시져를 정확하게 따라갈 수 있는 형태의 계산**을 말합니다.
    예를 들어, $\pi$의 소수점 아래 10억번째 자리를 계산하는 것은, 충분히 무한한 시간과 종이가 주어진다면 인간은 연필과 지우개를 가지고 해당 연산을 완벽하게 재현할 수 있습니다. 속도가 지나치게 느릴 뿐.

    *"단순하지 않은 지적인 노동"*은, 인간이 아직 프로시져를 명시적으로 엄밀하게 표현할 수 없는(혹은 모르는) 노동을 말합니다.
    대표적인 예시로 창의적인 그림을 그리는 것, 훨씬 복잡한 문제로는 지구 온난화를 늦추는 것 등이 있습니다.

---

## Even the current model is powerful enough

이런 말을 하면, 그 말을 들은 어떤 사람들은 다음과 같은 생각을 할 수도 있습니다. 실제로도 이런 반응은 인터넷에서 아주 많이 찾아볼 수 있습니다.

!!! quote

    *"에이, 내가 GPT한테 이런이런거 물어보니까 막 틀리고 엉뚱하게 말하던데? 얘네들은 한참 멀었어."*

최악의 시나리오로, 만에 하나라도 현재의 LLM 모델 구조를 가진 AI가 사람들이 흔히 말하는 "AGI"의 벽을 넘지 못하고 지금 수준에서 멈춘다 하더라도, 여전히 AI의 위력은 위협적이라고 생각합니다.
제가 이렇게 생각하는 이유는 다음과 같습니다.

### AI is already doing many things

요즘은 AI 스타트업 춘추전국시대라고 해도 과언이 아닙니다.
생긴 지 얼마 되지도 않았으면서 어지간한 대기업들을 후려치는 [1500억 달러가 넘는 밸류에이션](https://www.nytimes.com/2024/10/02/technology/openai-valuation-150-billion.html)을 인정받은 OpenAI를 제외하더라도,
정말 많은 분야에서 인공지능 스타트업이 활발하게 생겨나고 있습니다.

!!! references

    2024년 미국에서는 1억 달러 이상을 투자받은 인공지능 스타트업이 총 49개입니다. (출처: [TechCrunch](https://techcrunch.com/2024/12/20/heres-the-full-list-of-49-us-ai-startups-that-have-raised-100m-or-more-in-2024/))

![bizwatch_tax_services](/assets/posts/tho/high_intelligence/bizwatch_tax_services.jpg)

!!! caption

    2023년 4월 기준 대한민국의 세무회계서비스 스타트업 현황입니다.
    (출처: [Bizwatch 기사](https://news.bizwatch.co.kr/article/mobile/2023/04/06/0008))

### AI is copyable

어떤 일을 해결하는데(작곡, etc) 탁월한 AI를 개발했다면,
일정 성능 이상의 컴퓨터에서는 전부 동일한 모델을 복사하여 돌릴 수 있습니다.
실제로 이미 [huggingface](https://huggingface.co/) 등에서 인공지능 모델을 다운받아서 집에서 돌릴 수 있는 [Web UI](https://github.com/AUTOMATIC1111/stable-diffusion-webui)까지 오픈소스로 다 개발되었습니다.
개발을 어느 정도 할 줄 안다면, 집에 있는 컴퓨터에서 공짜 인공지능으로 엄청나게 많은 양의 고퀄리티 그림을 무제한으로 뽑아낼 수 있습니다.

코딩 같은 두뇌노동이든, 용접 같은 육체노동이든 뭐든 간에,
전문적인 스킬을 가진 인간을 길러내는 것은 많은 시간과 비용이 드는 일입니다.
두 인간을 컨디션과 생각하는 방식까지 전부 똑같게 만드는 것은 사실상 불가능한 일입니다.
그런데 인공지능은 단순히 파일과 메모리를 복사하는 것으로 그렇게 양성하는 것이 가능합니다.

이게 의미하는 바는, 어떤 문제를 해결하는 인공지능이 공공에 공개되었을 때,
이 세상의 모든 사람들의 해당 문제를 해결하는 스킬이 *"즉시"* 상향평준화된다는 것입니다.

### Lots of layoffs are currently ongoing

이미 인공지능으로 인한 생산성 향상으로(이게 원인의 전부는 아니겠지만),
상당량의 해고 및 고용감축이 진행되고 있습니다.

개발자 입장에서 보면 초보적인 개발도 제대로 못하는(그리고 포텐셜도 없는) 주니어 프로그래머들은,
이제 시니어 프로그래머 입장에서 한 달에 20달러 정도면 결제할 수 있는 Copilot Pro보다도 못합니다.
실제로 개발자 채용 시장은 현재 매우 얼어붙은 상태입니다.

특히 뚜렷한 도메인이 없이 엑셀 정도만 다루는 사무직들의 대체는 엄청나게 가팔라질 것으로 예상합니다.
법적/제도적 보호막이 있는 회계사 같은 직업의 경우 상황이 좀 더 낫겠지만, 그저 수명이 좀 더 길어질 뿐이라는 생각입니다.

### What if the current model goes further?

만약 이러한 모델들이 더 발전하면 어떻게 될까요?
여기서 어떤 사람들은 인공지능이 더 발전하는데 시간이 오래 걸리거나, 혹은 심지어 발전하지 못할거라고 생각하지만, 저는 다르게 생각합니다.

---

## The different complexity

이제 본론으로 들어와서, "다른 복잡도"의 지능에 대해 제 생각을 서술해보겠습니다.

### Simple problem becomes hard to scale without basic logic

간단한 문제를 잠시 하나 들고 가보겠습니다.
길이가 10 이상인 정수 배열이 주어질 때, 해당 정수 배열의 첫 10개의 값을 1씩 빼는 프로그램을 작성하기 위해서는 어떤 코드를 작성해야 할까요?
Python의 경우, 다음과 같은 간단한 프로그램을 만들 수 있을 것입니다.

```python
def solution(array: list[int]) -> list[int]:
    assert len(array) >= 10  # just for safety
    for i in range(10):
        array[i] -= 1
    return array
```

만약 이 문제를 푸는 사람이 반복문/재귀함수와 같은 [compound statement](https://docs.python.org/3.13/reference/compound_stmts.html)에 대한 개념이 없고 그런 걸 활용할 줄 모른다면,
아마도 다음과 같은 노가다 방식으로 문제를 해결할 것입니다.

```python
def solution_stupid(array: list[int]) -> list[int]:
    assert len(array) >= 10  # just for safety
    array[0] -= 1
    array[1] -= 1
    # ...
    array[8] -= 1
    array[9] -= 1
    return array
```

그리고 이런 저차원적인 존재의 입장에서는 현대 컴퓨터 공학에서 만들어지는 각종 알고리즘과 프로그램들이 어마어마하게 복잡하게 느껴질 것입니다.
왜냐하면 고차원적인 로직에 대한 개념이 머릿속에 존재하지 않기 때문입니다.
당장 위의 간단한 문제만 해도 10개의 값이 아니라 1000개의 값에 대해 똑같은 행동을 하려면 1000줄이 넘는 코드를 작성해야 합니다.

### The strictly defined procedure

저는 인공지능을 보면서 비슷한 생각을 했습니다.
인공지능(특히 신경망 모델)을 흔히들 black box라고 말하지만,
그것은 실제로 내부 값들에 대한 정보가 감추어지기 때문인 것이 아니라,
인간의 뇌와 사고방식에서 그 노드들의 값의 변경 과정을 인간이 이해할 수 있는 형태로 해석하지 못하는 것일 뿐입니다.

인공지능 모델들은 그 자체로, 그동안 인간이 컴퓨터 프로그램에게 시키기 어렵다고 믿었던 문제를 해결하는 일련의 거대한 컴퓨팅 프로세스입니다.
근본적으로 그 내부에서는 수없이 많은 덧셈과 곱셈 같은 primitive 연산들이 이루어지고 있습니다.
각각의 단일 덧셈과 곱셈들이 내부적으로 문제를 해결하는데 어떤 영향을 주는지 우리는 알지 못하지만, 어쨌든 그런 모델이 복잡한 계산을 진행한 직후 내놓는 결과는 우리를 놀랍게 만들고 있습니다.
내부적인 과정을 해석하지 못할 뿐이지만, 엄밀하게 정량화된 함수를 만들어냈다는 것입니다.

심지어 최근 만들어진 GPT o1 등의 모델은 그동안 LLM이 정복하기 어렵다고 널리 믿어졌던 추론에도 능한 모습을 보여주고 있습니다.
아직 공개되지 않은 GPT o3 모델은 [Codeforces에서 레이팅 2700](https://codeforces.com/blog/entry/137532)에 도달했다고 합니다.

이 부분은 개인적 추측이지만, 저는 현실에서 인간이 하는 모든 형태의 두뇌활동(연산, 추론, 감정, 기억)들을 정량화하는 것이 가능하다고 믿고 있습니다.
그리고 이게 만약 가능하다면 이것은 정말 말도 안 되는, 역사상 단 한번도 없었던 혁신입니다.

한번 만들어진 인공지능은 수평적-스케일링하는 것이 가능합니다.
전 세계의 모든 지식에 실시간으로 접근할 수 있는 어떤 굉장히 똑똑한 인간이 이 세상에 수십억명 생긴다고 생각하면, 그 효과는 감히 상상할 수도 없습니다.
그리고 저는 인공지능의 발전으로 인해 심지어 이것보다 더 먼 지점에 도달하게 될 것이라고 생각합니다.

### What if there is an another complexity?

수평적 스케일링도 마찬가지지만, 만약 수직적 스케일링도 가능하다면 어떨까요?

- 만약 우리가 풀기 어렵다고 생각했던 문제들조차 앞서 만들어진 AI처럼 문제 해결 함수를 엄밀하게 정량적으로 정의하는 게 가능하다면?
- 그런 문제를 해결할 수 있는 더 높은 지능의 입장에서 인간을 바라봤을 때 인간이 반복문 같은 것조차 제대로 이해하지 못하는 존재라면?
- 인간의 입장에서는 더 어려운 문제를 풀 때마다 몇 배씩 더 필요한 노력의 양이, 더 높은 지능의 입장에서는 $\log$ 그래프로 환산한 것 마냥 내려가게 된다면?

저는 다른 것이 아니라 이런 것이 어떻게 보면 진짜 [코스믹 호러](https://en.wikipedia.org/wiki/Lovecraftian_horror)가 될 수도 있다고 생각합니다.
우리가 아무리 따라가려고 해도 절대로 따라갈 수 없는,
우리가 `a[i] -= 1`을 한줄한줄 따라쓰고 있을 때 `for`문 한방으로 문제를 싹 다 해결해버리는,
그런 존재를 눈앞에서 마주하는 것은 어떤 기분이 들 지 도저히 상상이 가지 않습니다.

만약에 이 모든 것들이 진짜로 가능한 것이라면, 특이점이 발생한 이후에는 인간이 하는 모든 개척/탐구활동이 의미가 없어질 수 있습니다.
우리가 행복한 완몰가(완전 몰입 가상현실) 속에서 쾌락을 즐기며 놀고 먹을 수 있을지, 실험쥐가 될 건지, 아니면 그냥 아예 사라져 버릴지는 예측 불가능한 영역에 있다고 생각합니다.

---

인공지능과 특이점에 대해 요즘 드는 생각을 정리해서 써보았습니다.
글을 읽어주셔서 감사합니다.
