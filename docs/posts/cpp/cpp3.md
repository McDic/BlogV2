---
date: 2023-02-11
categories:
  - C++
tags:
  - cpp
  - programming
  - computer-science
title: CPP 3. Templates
slug: cpp-3
---

안녕하세요. C++ 시리즈의 3번째 게시글입니다! 이번에는 Generic을 위한 개념인 `template`에 대해 알아보도록 하겠습니다.
Template는 개념이 너무 방대하고, 서로가 상호참조하는 개념도 많아서, 순서대로 아래로 스크롤하면서 읽으시는 것보다는 필요한 개념을 트래킹해가면서 읽으시는 것을 추천합니다.

<!-- more -->
---

## Template

[Generic programming](https://en.wikipedia.org/wiki/Generic_programming)이란, 어떤 행동을 하는 코드가 작성되었을 때 그 코드에서 필요한 변수, 함수 등의 행동보다 타입을 나중에 결정하는 프로그래밍 패러다임을 말합니다.
C++에선 이것이 `template`를 통해 가능한데요. 예를 들어 다음과 같습니다.

```cpp
template <class T> int convert_to_int(T instance);
```

여기서 `convert_to_int` 함수는 복수의 타입 `T`에 대해서 `T` 타입을 가지는 객체를 하나 받아 `int`를 리턴해주는 함수가 됩니다.

C++에서 `template`를 통해서 generic하게 만들 수 있는 요소들은 다음과 같습니다.

- 함수 ([function template](https://en.cppreference.com/w/cpp/language/function_template))
- 클래스 ([class template](https://en.cppreference.com/w/cpp/language/class_template))
- alias ([alias template](https://en.cppreference.com/w/cpp/language/type_alias))
- 변수 ([variable template](https://en.cppreference.com/w/cpp/language/variable_template))

그 외 [concept template](https://en.cppreference.com/w/cpp/language/constraints)도 있지만, 이거는 C++20에서 다루는 내용이기 때문에 생략하도록 하겠습니다.

---

## Function Templates

`template`를 사용하면 Generic한 타입의 파라미터 또는 리턴 타입을 가지는 함수를 만들 수 있습니다.
Template 함수를 정의하는 syntax는 다음과 같습니다.

```
template <...> return_type function_name (...);
```

다음은 template function 정의의 예시입니다.

```cpp
#include <iostream>
#include <string>

template <class T> void swap(T &obj1, T &obj2) {
    T temp = obj1;
    obj1 = obj2;
    obj2 = temp;
}

int main(void) {
    int a = 1, b = 2;
    double c = 3.4, d = 5.6;
    std::string e = "ee", f = "ff";
    swap(a, b); // swap<int>
    swap(c, d); // swap<double>
    swap(e, f); // swap<std::string>
    std::cout << a << b << c << d << e << f << std::endl;
}
```

### Template can't do everything

`template`이 generic한 함수를 만들어줬다고 해서 실제로 불가능한 연산까지 올바르게 만들어주는 것은 아닙니다. 예를 들어보겠습니다.

```cpp
#include <string>

template <class T> T add_one(T obj) {
    return obj + 1;
}

int main(void) {
    // Number arithmetic
    add_one(1);
    add_one(-2.34);

    // It's ok because of pointer arithmetic..
    add_one("const char*");

    // Compile Error!
    // add_one(std::string("dd"));
}
```

위 코드에서 `int`, `double`, 그리고 `const char*` 타입은 `int`와의 덧셈 연산이 지원되기 때문에 상관없지만, `std::string`은 `+ 1`이 안 되기 때문에 컴파일러가 *instantiation*을 만드는 과정에서 에러가 발생합니다.
(instantiation에 관해서는 후술하겠습니다.)

### Template argument deduction

Function template를 instantiate하기 위해서는 모든 template argument를 컴파일러가 알아야 하지만, 프로그래머가 반드시 이를 명시적으로 지정해줄 필요는 없습니다.
다음 코드처럼 일부 템플릿 파라미터만 지정해주더라도(또는 아예 지정하지 않더라도), 컴파일러는 지정되지 않은 템플릿 파라미터를 알아서 추정해낼 수 있다면 그 추정한 타입 또는 값을 템플릿 파라미터로 사용합니다.

```cpp
#include <string>
#include <utility>

template <class T1, class T2, class T3>
std::pair<T1, T2> pairize(T3 x) {
    return {(T1)x, (T2)x};
}

int main(void) {
    // pairize<float, double, int>
    std::pair<float, double> a = pairize<float, double>(-1);
    // pairize<std::string, std::string, const char*>
    auto [b1, b2] = pairize<std::string, std::string>("abc");
    // pairize<int, long double, float>
    std::pair<int, long double> (*c) (float) = pairize;
}
```

또한 이 deduction은 다음 코드와 같이 operator overloading에 대해서도 적용됩니다.

```cpp
#include <iostream>

int main(void) {
    // std::ostream &std::operator<<<std::char_traits<char>>(std::ostream &__out, const char *__s)
    std::cout << "Hello ";
    // std::ostream &std::ostream::operator<<(int __n)
    std::cout << 1;
    // std::ostream &std::ostream::operator<<(double __f)
    std::cout << 2.3;
    // std::ostream &std::ostream::operator<<(std::ostream &(*__pf)(std::ostream &))
    std::cout << std::endl;
}
```

Constructor를 호출할 때도 마찬가지입니다.

```cpp
#include <functional>
#include <tuple>
#include <utility>

int main(void) {
    std::pair p(2, 34.5); // std::pair<int, double>
    std::tuple t(1, 2.34, "abc"); // std::tuple<int, double, const char*>
    std::less less; // std::less<void>
}
```

Template function을 호출할 때 deduction이 일어나는 과정은 상당히 복잡합니다. [C++ Reference](https://en.cppreference.com/w/cpp/language/template_argument_deduction#Deduction_from_a_function_call) 페이지에 잘 설명되어 있는데, 깊게 파보실 분은 한번쯤 읽어보셔도 좋을 것 같습니다.

### Template argument substitution

만약 모든 template argument가 명시적으로 지정되었다면, 그 안에 들어가는 파라미터들은 함수/클래스 내부에서 해당 타입으로 고정이 됩니다.
저는 파라미터들에 대해서 implicit type casting이 일어난다고 이해했습니다.

경우에 따라 substitution이 실패하는 경우가 있는데, 그것이 컴파일 에러로 이어지지는 않습니다.
이를 [SFINAE (Substitution Failure Is Not An Error)](https://en.cppreference.com/w/cpp/language/sfinae) 라고 합니다.
만약 명시적으로 지정되었거나 또는 deduced된 템플릿 파라미터를 substitution 하는 게 실패하면, 해당 specialization이 버려지는 규칙을 의미합니다.

다음 코드와 같이, top-level CV qualifier의 제거는 해당 함수의 파라미터 타입에 영향을 미치지 않습니다.
(다만, [GCC Bug 85428](https://gcc.gnu.org/bugzilla/show_bug.cgi?id=85428)에 의해 gcc 12 미만에서 컴파일 되지 않습니다!)

```cpp
template <class T> void f(T t) {}
template <class T> void g(const T t) {}
template <class T> void h(T t, T* tp) {}

int main(void) {
    static_assert(main == main); // OK

    constexpr auto fint = f<int>; // void(int), t: int
    constexpr auto fconstint = f<const int>; // void(int), t: const int
    static_assert(fint != fconstint); // FAILS DUE TO BUG

    constexpr auto gint = g<int>; // void(int), t: const int
    constexpr auto gconstint = g<const int>; // void(int), t: const int
    static_assert(gint != gconstint); // FAILS DUE TO BUG

    constexpr auto hint = h<int>; // void(int, int*)
    constexpr auto hconstint = h<const int>; // void(int, const int*)
}
```

### Function template overloading

Function template은 오버로딩 될 수 있습니다.

일반 함수는 항상(리턴 타입과 파라미터 타입이 모두 같더라도!) template function과 구분됩니다. (always distinct)
동일한 이름의 일반 함수가 정의되어 있는 경우, 동일한 타입의 템플릿 함수를 호출하고 싶다면 explicit하게 template parameter를 정의해줘야 합니다.

```cpp
#include <iostream>

template <class T> T f(T x) { return x; }
int f(int x) { return x+1; }

int main(void) {
    // Prints "1 2"
    std::cout << f<int>(1) << ' ' << f(1) << std::endl;
}
```

다음 코드와 같이 파라미터 타입을 모두 명시적으로 지정하더라도 return 타입이 ambiguous해서 컴파일러가 deduce하지 못하는 경우가 있습니다.
이럴 경우 리턴 타입까지 모두 명시해줘야 합니다.
하지만, 파라미터 타입도 같고 리턴 타입까지 같은 경우, [ODL Rule](https://en.cppreference.com/w/cpp/language/definition#One_Definition_Rule)에 의해서 정의를 2번 이상 할 수 없습니다.

```cpp
template <int I> struct A {
    const static int member = I;
};

template <int I, int J> A<I+J> f(A<I>, A<J>) { return A<I+J>(); }
// template <int K, int L> A<K+L> f(A<K>, A<L>) { return A<K+L>(); } // Compile Error!
template <int I, int J> A<I-J> f(A<I>, A<J>) { return A<I-J>(); }

int main(void) {
    // auto f23 = f<2, 3>; // Compile Error!
    A<5> (*f2p3)(A<2>, A<3>) = f<2, 3>;
    A<5> (*f1p4)(A<1>, A<4>) = f<1, 4>;
    A<-1> (*f2m3)(A<2>, A<3>) = f<2, 3>;
}
```

두 function templates는 다음 조건을 모두 만족할 때 *equivalent*하다고 표현합니다.

- 동일한 scope 내에서 declared 되어 있을 때
- 동일한 함수 이름을 가질 때
- 동일한 template parameter list를 가질 때(ex: `<int, double, A<int>>`)
- template parameter 관련해서 사용되는 expression들의 리턴 타입과 파라미터 리스트가 모두 동일할 때

Template parameter에 사용되는 두 expression은 다음 조건을 모두 만족할 때 *functionally equivalent*하다고 표현합니다.

- 두 expression이 equivalent하지 않을 때
- 동일한 템플릿 파라미터에 대해서 두 expression을 실행한 값이 같을 때

만약 다음 코드와 같이 프로그램이 functionally equivalent하지만 equivalent하지 않은 function template를 포함하고 있다면, 해당 프로그램은 *ill-formed* 되었다고 간주됩니다.

```cpp
template <int I> class A {};

template <int I> void f(A<I>, A<I+10>); // #1
template <int I> void f(A<I>, A<I+10>) {} // Equivalent to #1
template <int I> void f(A<I>, A<I+1+2+3+4>) {} // #2; Functionally equivalent to #1

int main(void) {
    // f(A<1>{}, A<11>{}); // Compile Error!
}
```

### Partial Ordering

> 주의: 아직 해당 사항이 function specialization에 대해 작동하는 건지, function overloading에 대해 작동하는 건지, 아니면 둘 다인지 아직 이해를 못했습니다. 
> 문서에는 specialization쪽에 대해서 써져 있어서 specialization에 대해 작동한다고 되어 있는 것 같긴 한데, 그럼 둘이 exclusive mutual한 개념이 아닌 건가? 라는 생각도 들고.. 아무튼 좀 더 정리되면 정확하게 정리해보겠습니다.

C++에서 여러 function template specialization에 대해서 어떤 함수를 사용할지 선택하는 과정을 [Partial Ordering](https://learn.microsoft.com/en-us/cpp/cpp/partial-ordering-of-function-templates-cpp?view=msvc-170)이라고 합니다.

1. 두 function template을 각각 `T1`, `T2`라고 합시다.
2. `T1`에 적용할 수 있는 파라미터 타입을 `T2`에 대입해보고, 반대로도 해봅니다.
3. 2번의 과정이 한쪽만 성공한다면, more specialized 우열이 결정됩니다. (만약 양쪽이 성공한다면, 그 함수를 콜하려고 할 때 ambiguous call이 되어버립니다.)

다음 코드는 C++ Reference에 의하면 컴파일이 되어야 할 것 같은데, 안 되네요.. (gcc 7, 10, 11 다 안 됩니다)

```cpp
#include <iostream>

struct A {};

template <class T> struct B {
    template <class R> int operator* (R&) { return 0; }
}; // More specialized

template <class T, class R> int operator* (T&, R&) { return 1; }

int main() {
    A a;
    B<A> ba;
    std::cout << ba * a << std::endl;
}
```

두 template specialization `A`, `B`에 대해 일부 조건을 만족하면 *A is more specialized than B* 라고 하는데, 그런 조건들의 목록은 다음과 같습니다.

- `T*`은 `T`보다 더 specialized 하고, `const T`는 `T`보다 더 specialized 하고, `const T*`는 `T*`보다 더 specialized 합니다.
    ```cpp
    #include <iostream>

    template <class T> const char* f(T) { return "f(T)"; }
    template <class T> const char* f(T*) { return "f(T*)"; }
    template <class T> const char* f(const T*) { return "f(const T*)"; }

    int main(void) {
        const int* x;
        std::cout << f(x) << std::endl;
    }
    ```
- Reference 타입의 경우 pointer와는 다르게 동작합니다. `T`와 `T&`, `T`와 `T&&`는 ambiguous합니다.
    ```cpp
    #include <iostream>

    template <class T> const char* f(T) { return "f(T)"; }
    template <class T> const char* f(T&) { return "f(T&)"; }
    template <class T> const char* f(T&&) { return "f(T&&)"; }

    int main(void) {
        // std::cout << f(1.0) << std::endl; // Ambiguous between T and T&&
        double x;
        // std::cout << f(x) << std::endl; // Ambiguous between T and T&
    }
    ```
- 명시적으로 지정된 타입과 템플릿으로 deduce된 타입이 동일해서 두 템플릿이 겹치는 경우가 있습니다. 이 경우는 ambiguous합니다.
    ```cpp
    #include <iostream>

    template <class T> const char* f(T, T) { return "f(T, T)"; }
    template <class T> const char* f(T, int) { return "f(T, int)"; }

    int main(void) {
        // const char* (*func)(int, int) = f<int>; // Compile Error!
    }
    ```
- 함수 콜 컨텍스트(call context)는 오직 explicit call arguments에 의해서만 좌우됩니다. 따라서 Default function parameter, function parameter packs, ellipsis parameter 등은 명시하지 않는 이상 무시됩니다.
    ```cpp
    template <class T> void f(T) {}
    template <class T> void f(T, int i=2) {}
    template <class T> void f(T, ...) {}

    int main(void) {
        f(1, 2, 3); // OK
        // f(1); // Compile Error!
    }
    ```

### Function overload is not a function specialization

Function overload는 non-template와 primary-template에 의해서만 결정되며, 그 과정에서 function specialization은 무시됩니다.
다음 코드는 그 예시입니다.

```cpp
#include <iostream>

template <class T> void f(T) { // #1 Primary
    std::cout << "f<T>(T)\n";
}
template <> void f(int*) { // #1 specialization
    std::cout << "f<int>(int*)\n";
}
template <class T> void f(T*) { // #2 Primary (overload)
    std::cout << "f<T>(T*)\n";
}

int main(void) {
    int *x = new int;
    f(x); // Calls #2 Primary
    delete x;
}
```

---

## Class Templates

Template class를 정의하는 syntax는 다음과 같습니다.

```
template <...> class_name;
```

예를 들면 다음과 같습니다.

```cpp
#include <iostream>

template <class T> class A {
private:
    T member;
public:
    A() = delete;
    A(T x): member(x) {}
    T get() { return member; }

    template <class X> struct Local {
        static X convert(T wow) {
            return X(wow);
        }
    };
};

int main(void) {
    std::cout << A(3).get() << '\n' 
              << A(1.23).get() << '\n'
              << A("bbb").get() << '\n' 
              << A<int>::Local<double>::convert(1.2) << '\n';
}
```

상속도 자유롭게 할 수 있습니다.
경우에 따라 primary template을 그대로 상속받던가, 특정 instantiation만 지정해서 상속받을 수 있습니다.

```cpp
template <class T> struct L1 { T member; };
template <class T> struct L2: L1<T> { T member2; };
template <class T> struct L2fromInt32: L1<int> {};

int main(void) {
    L1<double> {};
    L2<long long> {};
    L2fromInt32<const char*> {};
}
```

### Specializations can have different configurations

다음 코드와 같이, template class에 대해 specialization을 만들 경우 해당 template class의 primary template에 있는 모든 것을 전부 재정의해줘야 합니다. 이 부분은 좀 불편한 것 같네요.

```cpp
#include <iostream>

template <class T> struct A {
    const static int x = 1;
};

template <> struct A<int> {
    constexpr static double y = 2.3;
};

int main(void) {
    std::cout << A<double>::x << '\n';
    // std::cout << A<double>::y << '\n'; // Compile Error!
    // std::cout << A<int>::x << '\n'; // Compile Error!
    std::cout << A<int>::y << '\n';
}
```

### Class Template Argument Deduction (CTAD)

Function template 뿐만 아니라, class template에 대해서도 template argument deduction이 작용합니다.
이를 [CTAD](https://en.cppreference.com/w/cpp/language/class_template_argument_deduction)라고 합니다.

#### Implicit CTAD

프로그래머가 특별히 지정해주지 않아도, 이미 정의되어 있는 생성자 또는 자동으로 생성되는 copy/move constructor를 통해 deduce되는 것을 *implicit CTAD*라고 합니다.

```cpp
template <class T> struct A {
    A(T, T) {}
};

int main(void) {
    A a = A{1.0, 2.0};
    auto a2 = A(a);
    auto a_ptr = new A{1, 2};
    delete a_ptr;
}
```

#### User-defined CTAD

다음과 같은 syntax를 사용하여 직접 CTAD를 정의할 수 있습니다.

```
template_name (...) -> template_id;
```

물론 이 syntax 앞에 `template <...>` 를 붙여서 CTAD를 generic하게 정의하는 것 또한 가능합니다.
또한, `explicit`이 `template_name` 앞에 optional하게 붙을 수 있는데요.
이 경우 기존 클래스 constructor에 [`explicit`](https://en.cppreference.com/w/cpp/language/explicit)이 붙는 효과와 동일한 효과가 작용합니다. (Copy initialization이 허용되지 않습니다)
다음 코드는 CTAD를 직접 정의하는 예시입니다.

```cpp
#include <string>

template <class T1, class T2> struct Employee {
    T1 name; T2 salary;
    Employee(T1 &name_): name(name_), salary(0) {}
    Employee(T1 &&name_): name(name_), salary(0) {}
    Employee(T1 name_, T2 salary_): name(name_), salary(salary_) {}
};

explicit Employee(const char*, int) -> Employee<std::string, double>;
// template <class T> explicit Employee(T) -> Employee<T, double>;
template <class T> Employee(T&) -> Employee<T, double>;

int main(void) {
    
    // <std::string, double> instead of <const char*, int>
    auto e1 = Employee("McDic", 1234); 
    // Employee e1b = {"McDic", 1234}; // Compile Error! (explicit)

    // <T, double> where T = const char[6]
    auto e2 = Employee("McDic");
    Employee e2b = "McDic"; // OK, non-explicit
    
    char name = 'M';
    auto e3 = Employee(name);
    // auto e4 = Employee('M'); // Compile Error! (Can't deduce T2)
}
```

---

## Alias Templates

`using`, `typedef`를 활용하여 template type에 대한 alias를 활용할 수 있습니다.

```cpp
template <class T> struct Lout {
    struct Lin1 { T member; };
    template <class U> struct Lin2 {
        T member2a;
        U member2b;
    };
};

template <class T> using Lin1Alias = typename Lout<T>::Lin1;
template <class T, class U> using Lin2Alias = typename Lout<T>::template Lin2<U>;

int main(void) {
    ::Lin1Alias<int> x;
    ::Lin2Alias<double, const char*> y;
}
```

Template class 내부의 template class를 접근하려면 [저런 식으로](https://stackoverflow.com/questions/1090819/template-class-inside-class-template-in-c) `::template`를 해줘야 하는데, 왜 그런지는 아직 잘 모르겠습니다..

---

## Variable Templates

C++14부터는 변수에도 템플릿을 씌우는 게 가능해졌습니다.
그 전에도 static data member나 `constexpr` function template 등으로 사실상 템플릿 변수가 가능하긴 했지만, 어쨌든 하나의 직관적인 방법이 가능해진 셈입니다.

syntax는 다음과 같습니다.

```
template <...> variable_name;
```

예시를 들어보겠습니다.

```cpp
#include <iostream>

template <class T> T pi = T(3.14);

int main(void) {
    std::cout << pi<int> << '\n' << pi<double> << std::endl;
}
```

Variable template는 namespace scope 또는 class scope(이 경우 static data member template이 됩니다)에서 등록될 수 있습니다.

---

## Template Specialization

Template parameter로 특정 값 또는 타입을 넣었을 때만 어떤 행동을 다르게 하고 싶을 수 있습니다.
그게 가능한데, 그걸 [template specialization](https://learn.microsoft.com/en-us/cpp/cpp/template-specialization-cpp?view=msvc-170)이라고 합니다.
Template function에서도 잠깐 설명드렸지만, 이건 overloading과는 조금 다른 개념입니다.

Specialization에는 두 종류가 있는데, 하나는 [full specialization](https://en.cppreference.com/w/cpp/language/template_specialization)이고 다른 하나는 [partial specialization](https://en.cppreference.com/w/cpp/language/partial_specialization)입니다.

### Full specialization

Full specialization은 어떤 템플릿의 파라미터들을 전부 명시적으로 지정해주는, 하나의 케이스에 대해서만 차별화시키는 specialization입니다.
Syntax는 다음과 같습니다.

```
template <> ...
```

예시를 들어보겠습니다.

```cpp
#include <iostream>

template <class T> T literal(T x) { return x; }
template <> int literal(int x) { return 0; }

int main(void) {
    std::cout << literal(1) << '\n' << literal(1.0) << std::endl;
}
```

`literal` 함수는 `int` 타입이 파라미터로 주어졌을 때에 대해서만 다르게 동작합니다. (`int`에 대한 `full specialization`이 적용됨)

또한, explicit specialization을 하기 위해서는 코드 상의 다른 어떤 곳에도 다음 코드처럼 해당 파라미터의 instantiation을 불러오는 코드가 "먼저" 있으면 안 됩니다.

```cpp
#include <algorithm>
#include <vector>

template <class T> void sort(std::vector<T> &vec) {
    std::sort(vec.begin(), vec.end());
}

int main(void) {
    std::vector<int> x = {3, 2, 1};
    sort(x);
}

// template <> void sort<int>(std::vector<int> &vec) {} // Compile Error!
```

또한, declare만 되고 definition이 만들어지지 않은 template class는 full specialization 등에 대해서도 다른 incomplete type처럼 자유롭게 사용할 수 있습니다.

```cpp
template <class T> struct X;
template <> struct X<int>;

int main(void) {
    X<int> *ptr;
}
```

### Partial specialization

Partial specialization은 템플릿 파라미터의 일부만 specialization을 합니다.
Function template에 대해서는 partial specialization을 하는 것이 불가능합니다.
다음은 코드 예시입니다.

```cpp
#include <iostream>
#include <string>

template <class T1, class T2, int I> struct A {
    static std::string get() { return "Primary " + std::to_string(I); }
};
template <class T1, int I> struct A<T1, T1*, I> {
    static std::string get() { return "Partial " + std::to_string(I); }
};
template <class T1> struct A<T1, T1*, 3> {
    static std::string get() { return "AnotherPartial"; }
};

int main(void) {
    std::cout << A<int, double, 7>::get() << '\n';
    std::cout << A<int, int*, 7>::get() << '\n';
    std::cout << A<int, int*, 3>::get() << '\n'; 
}
```

또한, template argument에는 다음과 같은 제한이 적용됩니다.

- Template argument list가 primary template이랑 완전히 동일해서는 안 됩니다.
    ```cpp
    template <class A, class B> class C {};
    // template <class D, class E> class C<D, E> {}; // Compile Error!
    ```
- Default argument가 argument list에 나타날 수 없습니다.
- Pack expansion에 해당하는 argument는 항상 argument list의 마지막에 있어야 합니다.
- 어떤 type argument에 의존하는 non-type argument는 specialize 될 수 없습니다.
    ```cpp
    template <class T, T t> struct A {};
    // template <class T> struct A<T, 1> {}; // Compile Error!
    ```

---

## Template Instantiation

Template 함수/클래스 등등의 정의 자체는 컴파일 과정에서 아무런 코드를 생성하지 않습니다.
해당 template이 사용되는 코드 상에서 specialize 되는 타입을 모두 찾아 해당 코드들을 generate합니다.

코드 상에서 template function, class가 특정 파라미터(`<int>` 등)에 대해 처음 호출될 때, 컴파일러는 [instantiation](https://learn.microsoft.com/en-us/cpp/cpp/function-template-instantiation?view=msvc-170)을 생성합니다.
Template function은 호출이 될 때마다 해당 template parameter에 해당하는 instantiation을 찾아서 호출됩니다.
Instantiation은 보통 프로그래머 입장에서 굳이 따로 무언가를 하지 않아도 알아서 잘 생성되지만, 원한다면 explicit하게 만들어낼 수 있습니다.

### Explicit Instantiation

[Explicit instantiation](https://en.cppreference.com/w/cpp/language/function_template#Explicit_instantiation)은 템플릿 내의 인자를 구체적으로 지정해줘서 auto type deducing을 하지 않는 function template instantiation입니다.
Syntax는 다음과 같습니다.

- Template functions
  - `template return_type function_name <...> (...);` : [Template argument deduction](https://en.cppreference.com/w/cpp/language/template_argument_deduction)이 아예 없는 정의
  - `template return_type function_name (...);` : Template argument deduction이 파라미터에 대해서만 실행되는 정의
- Template classes
  - `template class/struct/union name <...>;`

맨 앞에다가 `extern`을 선택적으로 붙일 수도 있습니다.

### Forced instantiation by expression

C++ 레퍼런스에 따르면.. 다음과 같습니다.

> The existence of a definition of function is considered to affect the semantics of the program if the function is [needed for constant evaluation](https://en.cppreference.com/w/cpp/language/constant_expression#Functions_and_variables_needed_for_constant_evaluation) by an expression, even if constant evaluation of the expression is not required or if constant expression evaluation does not use the definition.

경우에 따라 어떤 expression이 특정 함수의 evaluation을 필요로 하면 해당 함수의 정의를 컴파일러가 찾는다고 이해했습니다.
그래서 예시 코드가 해당 조건에 만족하는 지 조금 바꿔서 테스트해봤는데, 정말 컴파일 에러가 뜨더군요.

```cpp
template<typename T>
constexpr int f() { return T::unknown_static_member; }

template<bool B, typename T>
void g(decltype(B ? f<T>() : 0)) {}
 
template<bool B, typename T>
void h(decltype(int{B ? f<T>() : 0})) {}
 
int main(void) {
    g<true, int>(0); 
    // h<true, int>(0); // Compile Error, f<int> is needed
}
```

`decltype(B ? f<int>() : 0)` 에서 `B`가 참값이기 때문에 `f<int>`가 eval되어야 하는 것처럼 보이는데.. `f<int>`의 return type만 보고 실제 함수를 eval하는 것은 아니라는 게 신기했습니다.

### Deep template instantiation depth

Template은 매 instantiation마다 서로 다른 코드를 생성하기 때문에, 마음만 먹으면 다음과 같이 아주 많은 코드를 생성해내는 것이 가능합니다.

```cpp
#include <iostream>

template <unsigned int i> void say() {
    std::cout << i << ' ';
    say<i-1>();
}

template <> void say<0>() {
    std::cout << 0 << std::endl;
}

int main(void) {
    say<1 << 20>(); // Generates 1048576, ..., 1, 0
}
```

그래서 template을 잘못 사용하면 컴파일러가 생성할 instantiation의 양이 너무 커지는데요.
다행히도 gcc의 경우에는 이를 막기 위해 `template instantiation depth limit`이 존재합니다.
`-ftemplate-depth` 옵션을 주면 됩니다.
다른 컴파일러도 비슷한 옵션이 있을 거라 생각합니다.

이건 컴파일러마다 다를 수도 있을 것 같은데, (적어도 gcc 7.5.0 버젼에 대해서는) 다음과 같은 식으로 specialization이 되어 있지 않은 코드를 컴파일러가 분석하면 instantiation에 따라 아예 호출되지 않는 코드가 있더라도 semantic에 영향이 간다고 분석하는 듯 합니다.
다음 코드는 컴파일시 `template instantiation depth limit exceeded` 에러가 발생하며, underflow가 일어나는 것을 보실 수 있습니다.

```cpp
template <unsigned int I> void recursive() {
    if(I == 0) return;
    else recursive<I-1>();
}

int main(void) {
    recursive<3>();
}
```

---

## Variadic Templates (Parameter Pack)

[Variadic templates](https://learn.microsoft.com/en-us/cpp/cpp/ellipses-and-variadic-templates?view=msvc-170) 또는 [Parameter pack](https://en.cppreference.com/w/cpp/language/parameter_pack)이란, 임의의 개수의 템플릿 파라미터를 가지는 템플릿을 의미합니다.
Syntax는 다음과 같습니다.

```
template <something T...> blabla;
```

다음 코드는 템플릿 파라미터들의 합을 구하는 sum function의 예시입니다.
`sum1`은 같은 타입 `T` 파라미터를 몇 개든 받을 수 있습니다.

```cpp
#include <iostream>

template <class T> T sum1() { return T{0}; }
// template <class T, T v1> T sum1() { return v1; } // Ambiguous!
template <class T, T v1, T... v2> T sum1() {
    return v1 + sum1<T, v2...>();
}

int main(void) {
    std::cout << sum1<int, 1>() << '\n';
    std::cout << sum1<int, 1, 2>() << '\n';
    std::cout << sum1<int, 1, 2, 3>() << '\n';
}
```

다음 코드는 파라미터들을 print하는 print function의 예시입니다. `print`는 서로 다른 타입(`Types...`)의 파라미터를 몇 개든 받을 수 있습니다.

```cpp
#include <iostream>

template <class T> void print(std::ostream &out, T value) {
    out << value << std::endl;
}

template <class T, class... Types> void print(std::ostream &out, T value, Types... values) {
    out << value << ' ';
    print(out, values...);
}

int main(void) {
    print(std::cout, 1, 2.3, "abc");
}
```

### Fold Expression

Fold expression이란, binary operator 하나로 parameter pack의 모든 원소를 연산시키는 것을 의미합니다.
Syntax 및 각 syntax에 연결되는 결과는 다음과 같습니다.

1. `(E op ...)` -> `E1 op (E2 op ( ... (E[N-1] op E[N])))`
2. `(... op E)` -> `((E1 op E2) op ... ) op E[N]`
3. `(E op ... op I)` -> `E1 op (E2 op ... (E[N-1] op (E[N] op I)))`
4. `(I op ... op E)` -> `(((I op E1) op E2) op ... ) op E[N]`

보통 동일한 연산자를 여러 번 적용하는 연산의 경우 왼쪽부터 오른쪽으로 accumulate하는 경우가 많은데, 그게 2번, 4번의 syntax라는 점을 주의하셔야 할 것 같습니다.

다음 코드는 fold expression을 사용하는 예시입니다.

```cpp
#include <iostream>

template <class... Args> int any(Args... bools) {
    return (int)(... || bools);
}

int main(void) {
    std::cout << any(false, false, false) << any(false, false, true) << '\n';
}
```

Fold expression을 사용하실 때는 몇 가지를 주의하셔야 합니다.

1. Fold expression 바깥에 반드시 syntax에 써진 대로 괄호를 써줘야 합니다.
2. Fold expression의 init 값에 단순 값이 아닌 수식을 넣을 경우, 괄호로 감싸주어야 합니다.
    ```cpp
    #include <iostream>

    template <int Init, class... Args>
    int sum_with_double_init(Args... args) {
        // return (Init * 2 + ... + args);
        return ((Init * 2) + ... + args);
    }

    int main(void) {
        std::cout << sum_with_double_init<5>(1, 2, 3) << '\n';
    }
    ```

---

이상으로 template에 관하여 여러 가지를 많이 살펴보았습니다!
근데 아직 빠진 내용이 있을 수 있어 추후에 포스트를 보완할 수 있습니다.
이상으로, C++ 시리즈 3번째 포스팅을 마치겠습니다. 감사합니다!
