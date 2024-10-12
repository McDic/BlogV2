---
categories:
  - Python
tags:
  - python
  - programming
  - computer-science
  - web
title: PY 3. API Rate Limiter
---

안녕하세요. 이번 글에서는 API Limiter에 대해서 다뤄보려고 합니다.
Python에 특화된 주제는 아닌데, 그냥 구현을 Python으로 하다보니 Python 시리즈에 글을 쓰게 되었습니다.
만약 나중에 이 글을 넣기 적합한 다른 시리즈가 나온다면 그쪽으로 글을 옮길 수도 있습니다.

<!-- more -->
---

## API limiter

API Limiter는 API를 제공하는 서비스에서 무분별한 스팸 요청을 막기 위해 만드는 장치입니다.
시간당 API 요청 개수에 제한을 거는 대표적인 서비스로는 코인거래소 Binance가 있으며, [Binance Spot Exchange API Docs](https://developers.binance.com/docs/binance-spot-api-docs/web-socket-api#connection-limits) 등에서 자세한 사항을 확인하실 수 있습니다.

---

## Basic parameters

API 제한을 만드는 데 들어가는 요소들은 크게 다음과 같은 것들이 있습니다.

- Interval: API 제한 시간. 예를 들어 어떤 API는 1시간 당 요청 횟수로 제한을 책정하고 경우에 따라 1분 당 요청 횟수를 사용하는 곳도 있습니다.
- Capacity: `Interval`만큼의 제한 시간 동안 몇 번의 요청을 보낼 수 있는지를 의미합니다.

예를 들어, 1분 당 30번의 요청까지만 허용하는 API의 Interval은 3분, Capacity는 30번인 셈입니다.

그리고 이 제한은 한 API에 대해 여러 번 중첩되어 기록될 수 있습니다.
예를 들어 1시간 당 3600번의 요청 상한을 두고 동시에 1분 당 600번의 요청 상한을 둘 수 있습니다.
이것은 rate limit이 한 API에 2중으로 걸려있는 것에 불과하며, 개별적인 제한에 대한 구현만 진행하면 큰 어려움 없이 복잡한 제한도 구현할 수 있습니다.

---

## Implementation methods

어떤 API의 시간 당 요청 횟수를 측정하는 기준도 정의하기 나름입니다.
저는 다음 방법들을 제시합니다. 어느 쪽이 무조건 옳다라는 정답은 없습니다.
서비스의 특성이나 API의 민감도에 따라 다른 기준을 정의할 수 있을 것입니다.

### Simple resetting

기준이 되는 시간마다 API 요청 횟수를 초기화시키는 방식입니다.
아마 가장 간단한 구현방식이자 동시에 제일 적은 리소스를 사용하는 방식일 겁니다.
이 구현이 간단한 이유는 가장 마지막에 요청이 들어온 시각과 카운팅 횟수에 대한 정보만 알면 알고리즘이 작동하기 때문입니다.
하지만 이 방식의 잠재적인 단점은 API 요청 횟수가 초기화될 무렵 즈음에 컴퓨팅 및 I/O 부하가 잠깐 일어날 수 있다는 것입니다.
(트래픽이 엄청 크지 않은 이상 이게 유의미한 문제점이 될 지는 모르겠지만요..)

![simple_limit](/assets/posts/py/api_limiter/simple_limit.png)

!!! caption

    알고리즘을 시각화한 이미지입니다.
    일정한 시간 간격 안에서만 API request 횟수가 유효하며,
    어떤 사이클을 지나고 새로운 사이클에 진입할 경우 API request 횟수는 초기화됩니다.

```python
from datetime import datetime, timedelta


class RateLimiterCycled:
    """
    Rate limiter using the simple resetting method.
    """

    def __init__(self, interval: timedelta, capacity: int):
        self._interval = interval
        self._capacity = capacity
        self._last_requested: datetime = datetime.min
        self._count: int = 0

    def is_new_cycle(self, timestamp: datetime) -> bool:
        """
        Check if this timestamp is from a new cycle.
        """
        since_new_cycle = timedelta(
            seconds=timestamp.timestamp() % self._interval.total_seconds(),
        )
        return timestamp - since_new_cycle > self._last_requested

    def request(self, timestamp: datetime) -> bool:
        """
        Register a request and return whether it is allowed or not.
        """
        # Fail if the timestamp is not in order(same timestamp is allowed)
        if self._last_requested > timestamp:
            return False

        # Fail if overflowed on same cycle
        is_new_cycle = self.is_new_cycle(timestamp)
        if not is_new_cycle and self._count >= self._capacity:
            return False

        # Update last requested timestamp and count then return success
        self._last_requested = timestamp
        if is_new_cycle:
            self._count = 0
        self._count += 1
        return True
```

### Sliding window

일정한 단위시간 기준이 아닌, 그 어떤 연속적인 `interval`을 고르더라도 그 안에 `capacity` 개수 이상의 request가 없음을 보장하고 싶다면,
[Sliding window](https://stackoverflow.com/questions/8269916/what-is-sliding-window-algorithm-examples) 알고리즘을 사용하여 이를 해결할 수 있습니다.
구현 방식은 조금 복잡합니다.
왜냐하면 연속적으로 들어온 요청들의 timestamp 정보들을 전부 저장하고 오래된 timestamp들을 순차적으로 삭제할 수 있어야 하기 때문입니다.
이는 [deque](https://en.wikipedia.org/wiki/Double-ended_queue) 등을 사용하여 효율적으로 구현할 수 있습니다.

![window_limit](/assets/posts/py/api_limiter/window_limit.png)

!!! caption

    알고리즘을 시각화한 이미지입니다.
    개별 request마다 정보가 기억되는 일종의 "유통기한"이 다릅니다.
    이 알고리즘을 구현할 경우 timeline 상에서 그 어떤 연속적인 `interval`을 고르더라도 `capacity` 개수 이상의 request가 없음이 보장될 수 있습니다.

```python
from collections import deque
from datetime import datetime, timedelta


class RateLimiterContinuous:
    """
    Rate limiter that guarantees no overflow on any continuous time interval.
    """

    def __init__(self, interval: timedelta, capacity: int) -> None:
        self._request_timestamps: deque[datetime] = deque()
        self._capacity: int = capacity
        self._interval: timedelta = interval

    def get_last_request_timestamp(self) -> datetime:
        """
        Return the timestamp of the last request.
        """
        return (
            self._request_timestamps[-1]
            if self._request_timestamps
            else datetime.min
        )

    def request(self, timestamp: datetime) -> bool:
        """
        Register a request and return whether it is allowed or not.
        """
        # Fail if the timestamp is not in order(same timestamp is allowed)
        if self.get_last_request_timestamp() > timestamp:
            return False

        # Remove old expired timestamps
        while (
            self._request_timestamps
            and self._request_timestamps[0] < timestamp - self._interval
        ):
            self._request_timestamps.popleft()

        # Fail if the queue is still full
        if len(self._request_timestamps) >= self._capacity:
            return False

        # Add the request timestamp and return success
        self._request_timestamps.append(timestamp)
        return True
```

---

## Notes on lazy evaluation

위 구현들은 매 정각마다 실시간으로 횟수가 업데이트 되는 개념이 아닌,
요청이 들어올 때마다 뒤늦게 시간/횟수 관련 정보를 업데이트하는 것을 보실 수 있습니다.
실제로 요청이 자주 이루어지지 않는 API들의 정보까지 실시간으로 업데이트할 필요가 없습니다.
API request가 들어오면 그때 기존의 expired된 request timestamp들을 처리하더라도 계산량의 총량에는 변화가 없기 때문입니다.

---

지금까지 API limiter를 구현하는 방법들에 대해 알아보았습니다.
정말 오랜만에 블로그 글을 썼네요.. 글을 읽어주셔서 감사합니다.
