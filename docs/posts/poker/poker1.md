---
date: 2024-01-15
categories:
  - Poker
tags:
  - poker
  - probability
title: POKER 1. Heads-Up Flop Probabilities
slug: poker-1
---

!!! migrated

    *This article is migrated from which I wrote on my [PokerGosu](https://www.pokergosu.com).*

안녕하세요. 이번 시리즈에서는 [포커](https://en.wikipedia.org/wiki/Poker)에 대해서 다뤄보고자 합니다.
이 시리즈에서 다루는 포커는 [Texas Holdem](https://en.wikipedia.org/wiki/Texas_hold_%27em)이라는 가장 유명한 variant를 말합니다.

이번 게시글에서는 [플랍에 카드가 3장 깔린 상황](https://en.wikipedia.org/wiki/Texas_hold_%27em#Sample_hand)에서
2명의 플레이어가 베팅을 할 때, 어떤 카드가 깔렸고 본인이 어떤 상황인지에 따라, 양 측이 올인했을 때 각자 이길 확률이 얼마인지 계산해보고자 합니다.

!!! references

    확률 계산은 [이 웹사이트](https://www.cardplayer.com/poker-tools/odds-calculator/texas-holdem)를 사용했습니다.

<!-- more -->
---

## Set vs Straight = 1 : 2

![img](/assets/posts/poker/flop_prob/set_vs_straight.png){width=50%}

!!! caption

    셋 입장에서는 풀하우스가 생각보다 잘 만들어진다는 것을 시사합니다.
    참고로 바텀셋이어도 풀하우스나 러너러너 플러쉬로 이겨야 하기 때문에 확률은 거의 변하지 않습니다.
    숏스택이 탑셋이면 한방줄 상대로도 충분히 승부 볼 수 있습니다.

---

## Two over flush draw vs Top pair = 1 : 1

![img](/assets/posts/poker/flop_prob/2overflushdraw_vs_toppair.png){width=50%}
![img](/assets/posts/poker/flop_prob/2overflushdraw_vs_toppair2.png){width=50%}

!!! caption

    안 잡혀 있으면 뽀플이 조금 더 유리하고, 잡혀 있으면 뽀플이 조금 더 불리합니다.
    사실상 플립 싸움이니, 상황에 따라 충분히 승부 볼 수 있습니다.

---

## Two over flush draw vs Two pairs = 1 : 2

![img](/assets/posts/poker/flop_prob/2overflushdraw_vs_twopairs.png){width=50%}

!!! caption

    투페어 상대로는 조금 빡세지만, 베팅 금액에 따라 턴은 보거나 폴드할 수 있을 것 같습니다.
    반대로 투페어 입장에서는 밸류 뽑아내기가 수월할 것입니다.

---

## Straight and flush draw vs Set = 2 : 3 or 4 : 5

![img](/assets/posts/poker/flop_prob/flushandstraightdraw_vs_set.png){width=50%}
![img](/assets/posts/poker/flop_prob/straightflushdraw_vs_set.png){width=50%}

!!! caption

    뽀플 + 양차가 엄청나게 강력하다는 것을 보여줍니다.
    스티양차면 조금 더 강력하지만, 스티 아웃츠는 2개뿐이기 때문에 스티양차와 양차 뽀플이 그렇게 큰 차이가 나지 않습니다.

---

## Straight and flush draw vs Two pairs = 1 : 1

![img](/assets/posts/poker/flop_prob/flushandstraightdraw_vs_twopairs.png){width=50%}
![img](/assets/posts/poker/flop_prob/flushandstraightdraw_vs_twopairs2.png){width=50%}

!!! caption

    원오버면 뽀플 + 양차가 미세하게 더 유리하고, 그게 아니어도 거의 비등비등합니다.

---

## Two overs vs Two unders = 3 : 1

![img](/assets/posts/poker/flop_prob/2over_vs_2under.png){width=50%}

!!! caption

    확률이 투오버에 훨씬 유리하지만, 본인이 칩리더고 상대방의 베팅이 작다면 상황에 따라 콜을 해볼 수는 있을 것 같습니다.

---

## Two overs vs Two unders with flush draw = 4 : 5

![img](/assets/posts/poker/flop_prob/2over_vs_flushdraw.png){width=50%}

!!! caption

    상대방이 투오버 같은데 본인이 뽀플이다? 충분히 승부 볼 수 있습니다.

---

## Trips vs Over pair with flush draw = 7 : 1 or 11 : 1

![img](/assets/posts/poker/flop_prob/triples_vs_overpair.png){width=50%}
![img](/assets/posts/poker/flop_prob/triples_vs_overpair_no_flush.png){width=50%}

!!! caption

    트립스를 상대로 오버페어는 굉장히 절망적인 확률을 갖고 있습니다.
    플랍이 쪼개졌을 때 상대방의 레이즈에 경계합시다.

---

## Over pair vs Under pair = 5 : 4 or 15 : 1

![img](/assets/posts/poker/flop_prob/overpair_vs_underpairwithflushdraw.png){width=50%}
![img](/assets/posts/poker/flop_prob/overpair_vs_underpairwithflushdraw_dominated.png){width=50%}

!!! caption

    언더페어에 뽀플이 섞여 있다면 확률은 잡혀 있는지 아닌지에 따라 극단적으로 달라집니다.
    어느 쪽이 되었든, 오버페어에게 압도적으로 좋은 상황이며, 밸류를 뽑아내기 위해서 어그레시브하게 베팅을 해야 할 것입니다.

---

## Two overs with flush draw vs Low flush = 1 : 2

![img](/assets/posts/poker/flop_prob/twooverflushdraw_vs_underflush.png){width=50%}
![img](/assets/posts/poker/flop_prob/twooverflushdraw_vs_underflush2.png){width=50%}

!!! caption

    같은 모양의 카드가 많이 빠진 상태이기 때문에 플러쉬로 승리할 확률이 조금 줄어듭니다.
    탑페어라도 있으면 그나마 조금은 낫지만 큰 차이는 없습니다.
    베팅 금액에 따라 죽을 수도 있고, 턴 정도는 볼 수도 있을 것 같습니다.

---

## Full house vs Quads (or bigger full house) = 1 : 990++

![img](/assets/posts/poker/flop_prob/overfullhouse_vs_quads.png){width=50%}
![img](/assets/posts/poker/flop_prob/overfullhouse_vs_underfullhouse.png){width=50%}
![img](/assets/posts/poker/flop_prob/underfullhouse_vs_quads.png){width=50%}

!!! caption

    쉽지 않은 스팟입니다.
    본인이 포카드가 아닌 풀하우스라면, 상대방이 언더페어 혹은 블러핑이라는 100%에 가까운 아주 강한 확신이 있어야만 콜을 받을 수 있을 것입니다.
    똑같은 러너러너라도, 러너러너 플러쉬 같은 거랑 러너러너 포카드의 난이도가 현저하게 차이가 나는 것을 알 수 있습니다.

---

## Under full house vs Two overs = 7 : 3 or 50 : 1

![img](/assets/posts/poker/flop_prob/underfullhouse_vs_twoover.png){width=50%}
![img](/assets/posts/poker/flop_prob/underfullhouse_vs_twoover2.png){width=50%}

!!! caption

    투오버 입장에서는 콜하기가 쉽지 않습니다.
    물론 후자의 경우에는 한방 풀하우스가 나타나기 상당히 드문 경우이긴 합니다.

---

## Gutshot draw vs Top pair = 1 : 5 or 2 : 5

![img](/assets/posts/poker/flop_prob/gutshot_vs_toppair.png){width=50%}
![img](/assets/posts/poker/flop_prob/oneovergutshot_vs_toppair.png){width=50%}

!!! caption

    것샷은 별로 좋은 상황이 아닙니다.
    저는 것샷을 거의 믿지 않으며, 뽀플이 걸려있거나 혹은 잃어도 상관 없는 수준의 베팅이 나오지 않는 이상 플랍에 폴드합니다.

---

## Two overs with gutshot draw vs Bottom pair = 2 : 3

![img](/assets/posts/poker/flop_prob/twoovergutshot_vs_bottompair.png){width=50%}

!!! caption

    그래도 투오버인 상태라면 상황이 조금은 더 낫습니다.

---

## Two overs vs One pair = 1 : 3

![img](/assets/posts/poker/flop_prob/twoover_vs_toppair.png){width=50%}
![img](/assets/posts/poker/flop_prob/twoover_vs_bottompair.png){width=50%}

!!! caption

    본인이 논파켓 프리미엄 카드를 갖고 있지만 멀티웨이이고 미들~바텀 카드가 깔렸을 때 어그레시브하게 리드 베팅을 못하는 이유입니다.
    원페어한테 무조건 지고 있다고 생각하고 턴이나 리버를 싸게 봐서 원페어를 맞춰야 할 것입니다.

---

이 글은 계속 업데이트할 것 같습니다.
또 이런저런 스팟 생각나시면 말씀 주세요.
감사합니다.
