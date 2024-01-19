---
categories:
  - Python
tags:
  - python
  - programming
  - computer-science
title: PY 2. Some Frequently Used Python Tools by Me
---

안녕하세요. 이번 글에서는 제가 Python 언어를 사용하는 개발 프로젝트를 만들 때 자주 사용하는 툴 및 라이브러리들을 소개합니다.

!!! info

    아래 라이브러리들의 목록은 언제든지 수정될 수 있습니다.

<!-- more -->
---

## Linting

### [mypy](https://mypy.readthedocs.io/en/stable/)

Python Foundation에서 공식적으로 관리되고 있는 Python static typing 툴입니다.

```bash
pip install mypy
python -m mypy --ignore-missing-imports YOUR_CODE.py
```

저는 static typing을 해주는 것이 복잡한 구조의 소프트웨어에게 많은 이득을 가져다준다고 생각하기 때문에,
[Python이 dynamic lang 언어를 지향함에도 불구하고](https://peps.python.org/pep-0484/#non-goals), 가능한 static typing을 적극적으로 활용하려고 노력하는 편입니다.

`mypy`의 alternative으로는 Microsoft에서 개발중인 [pyright](https://github.com/microsoft/pyright)이 있습니다.

### [flake8](https://flake8.pycqa.org/en/latest/)

제가 사용하는 또 다른 linting 툴입니다.
전에 재직했던 회사들 중 하나에서 사용하기 시작한 게 개인프로젝트에서도 습관이 되었는데, 괜찮은 툴인 것 같습니다.

```bash
pip install flake8
python -m flake8 --max-line-length=88 --extend-ignore=F401,F403 YOUR_CODE.py
```

제가 `mypy` 말고도 이 linting 툴 또한 사용하는 이유는, `flake8`은 type checking 이외에 [다양한 오류](https://flake8.pycqa.org/en/latest/user/error-codes.html)들을 사전에 발견해주기 때문입니다.

---

## Formatting

저는 이 섹션에 있는 거의 대부분의 툴들을 모든 개인프로젝트에서 일괄적으로 적용하고 있습니다.

### [autopep8](https://github.com/hhatto/autopep8)

지금은 거의 안 쓰긴 합니다만, 한때 애용했던 formatting tool입니다.

```bash
pip install autopep8
python -m autopep8 --in-place -a -a YOUR_CODE.py
```

[VSCode](https://marketplace.visualstudio.com/items?itemName=ms-python.autopep8) 등 다른 에디터에서의 플러그인들도 있으니, 자동으로 formatting 되도록 적용하시는 것도 좋습니다.

### [black](https://github.com/psf/black)

제가 제일 많이 쓰는 formatter입니다.

```bash
pip install black
python -m black --line-length=88 YOUR_CODE.py
```

`black` 또한 [VSCode](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter) 플러그인이 있습니다.

### [isort](https://pycqa.github.io/isort/)

같은 그룹 내 import들을 alphabetical order로 정리하고 싶을 때 유용한 라이브러리입니다.

```bash
pip install isort
python -m isort --profile=black YOUR_CODE.py
```

`isort`도 [VSCode](https://marketplace.visualstudio.com/items?itemName=ms-python.isort) 플러그인이 있습니다.

---

## Distributing

파이썬 라이브러리를 [PyPI](https://pypi.org/)에 배포하여 사용자들이 [pip](https://pip.pypa.io/en/stable/)로 다운로드할 수 있게 하려면 [Distribution Package](https://packaging.python.org/en/latest/glossary/#term-Distribution-Package)라는 것을 만들어야 하는데,
이것은 별도의 빌드 시스템을 필요로 합니다.

### [setuptools](https://github.com/pypa/setuptools)

가장 흔히 사용하는 빌드 시스템이기도 하고, 저도 굳이 다른 걸 써야겠다는 느낌을 받고 있지는 않아서 사용하고 있습니다.

```bash
pip install setuptools
```

그리고 `pyproject.toml`에 다음과 같은 내용을 써두면 됩니다.

```toml title="pyproject.toml"
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"
```

자세한 사항은 [setuptools quickstart](https://setuptools.pypa.io/en/latest/userguide/quickstart.html)를 참고해주세요.

### [twine](https://twine.readthedocs.io/en/stable/)

[setuptools](#setuptools)로 빌드된 시스템을 PyPI에 업로드하는 것은 여러 방법이 있는데, 저는 편하게 twine을 사용하고 있습니다.

```bash
pip install twine
```

[Github Actions](https://github.com/features/actions), [Github Secrets](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions)와 같이 쓰면 편합니다.
다음 `.yml` 파일은 저의 repo 중 하나에서 특정 태그가 생길 때마다 해당 태그에서 `PyPI`에 라이브러리를 자동으로 푸쉬하는 액션을 만든 것입니다.

```yaml title=".github/workflows/twine.yml"
name: PyPI Upload

on:
  push:
    tags:
      - v[0-9]+\.[0-9]+\.[0-9]+

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: "pip"
          cache-dependency-path: "requirements*.txt"
      - run: pip install -r requirements-dev.txt
      - name: Build dist
        run: |
          python -m build
      - name: Upload to PyPI via Twine
        env:
          TWINE_PASSWORD: ${{ secrets.PYPI_TOKEN }}
        run: |
          twine upload --verbose -u '__token__' dist/*
```

---

## Virtual Environment

### [pyenv](https://github.com/pyenv/pyenv)

저는 [virtual environment](https://docs.python.org/3/tutorial/venv.html)를 [direnv](https://direnv.net/)랑 `pyenv`로 관리합니다.
`direnv`랑 `pyenv`를 설치하고 [shell hook](https://direnv.net/docs/hook.html)을 하셨다면, `.envrc`에 다음 사항들만 입력하시면 됩니다.

```bash
curl -sfL https://direnv.net/install.sh | bash
curl https://pyenv.run | bash
```

```bash title="~/.bashrc"
# ...
eval "$(direnv hook bash)"
export PYENV_ROOT="$HOME/.pyenv"
command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
# ...
```

```bash title=".envrc"
# ...
layout pyenv 3.X.Y
# ...
```

이제 폴더를 이동할 때마다 귀찮게 `source .venv/bin/activate` 같은 명령어를 칠 필요가 없습니다.

---

## Cross Language

Python은 [native C API](https://docs.python.org/3/c-api/index.html)를 지원하지만, 다른 언어에서 Python을 부르려면 꽤 복잡한 작업을 거쳐야 합니다.
[SWIG](https://www.swig.org/) 같은 걸 써도 되지만, 이쪽은 "interface file" 이라는 것도 작성해줘야 하고, 하여간 뭐가 고생해야 할 게 많습니다.

### [PyO3](https://pyo3.rs/)

Rust의 경우, `PyO3`라는 훌륭한 대안이 있습니다.
[rust-cpython](https://github.com/dgrunwald/rust-cpython), [CFFI](https://cffi.readthedocs.io/en/latest/) 같은 다른 대안들도 있지만, 저는 지금은 `PyO3`가 제일 좋아보입니다.

```bash
pip install maturin
```

Python, Rust로 소스코드를 짜고, [Cargo.toml](https://pyo3.rs/v0.20.2/getting_started#cargotoml)이랑 [pyproject.toml](https://pyo3.rs/v0.20.2/getting_started#pyprojecttoml)만 PyO3가 지정해준 포맷으로 잘 작성해주면,
[maturin](https://www.maturin.rs/)으로 빌드가 잘 작동하게 됩니다.
그리고 이렇게 만들어진 라이브러리는 원한다면 PyPI에 자유롭게 공유할 수 있습니다.

---

읽어주셔서 감사합니다.
혹시 이 글에 포함시킬만한 좋은 툴이 생각나셨다면 덧글로 제안 주셔도 됩니다.
