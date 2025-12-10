import timeit
from pathlib import Path
import matplotlib.pyplot as plt


def build_shift_table(pattern):
    """
    Create shift table for the Boyer-Moore algorithm.
    """
    table = {}
    length = len(pattern)

    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    table.setdefault(pattern[-1], length)
    return table


def boyer_moore_search(text, pattern):
    """
    Search for pattern in text using the Boyer–Moore algorithm.
    """
    if not pattern or not text:
        return -1

    shift_table = build_shift_table(pattern)
    i = 0
    pat_len = len(pattern)
    text_len = len(text)

    while i <= text_len - pat_len:
        j = pat_len - 1

        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1

        if j < 0:
            return i
        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))
    return -1


def compute_lps(pattern):
    """
    Compute the LPS array for KMP.
    """
    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps


def kmp_search(text, pattern):
    """
    Search for pattern in text using the Knuth–Morris–Pratt algorithm.
    """
    M = len(pattern)
    N = len(text)

    lps = compute_lps(pattern)

    i = 0
    j = 0

    while i < N:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

        if j == M:
            return i - j

    return -1


def polynomial_hash(s, base=256, modulus=101):
    """
    Return the polynomial hash of string s.
    """
    n = len(s)
    hash_value = 0
    for i, char in enumerate(s):
        power_of_base = pow(base, n - i - 1) % modulus
        hash_value = (hash_value + ord(char) * power_of_base) % modulus
    return hash_value


def rabin_karp_search(text, pattern):
    """
    Search for pattern in text using the Rabin–Karp algorithm.
    """
    substring_length = len(pattern)
    main_string_length = len(text)

    if (
        substring_length == 0
        or main_string_length == 0
        or substring_length > main_string_length
    ):
        return -1

    base = 256
    modulus = 101

    substring_hash = polynomial_hash(pattern, base, modulus)
    current_slice_hash = polynomial_hash(text[:substring_length], base, modulus)

    h_multiplier = pow(base, substring_length - 1) % modulus

    for i in range(main_string_length - substring_length + 1):
        if substring_hash == current_slice_hash:
            if text[i : i + substring_length] == pattern:
                return i

        if i < main_string_length - substring_length:
            current_slice_hash = (
                current_slice_hash - ord(text[i]) * h_multiplier
            ) % modulus
            current_slice_hash = (
                current_slice_hash * base + ord(text[i + substring_length])
            ) % modulus
            if current_slice_hash < 0:
                current_slice_hash += modulus

    return -1


def load_articles() -> dict:
    """
    Load article texts from the src folder.
    """
    base_dir = Path(__file__).resolve().parent
    src_dir = base_dir / "src"
    article1 = (src_dir / "стаття 1.txt").read_text(encoding="utf-8")
    article2 = (src_dir / "стаття 2.txt").read_text(encoding="utf-8")
    return {
        "article_1": article1,
        "article_2": article2,
    }


def analyze_search_algorithms(texts, patterns, run_qty):
    """
    Measure execution time of Boyer–Moore, KMP and Rabin–Karp
    for each text and pattern using timeit.
    """
    algorithms = {
        "boyer_moore": boyer_moore_search,
        "kmp": kmp_search,
        "rabin_karp": rabin_karp_search,
    }

    results = {
        text_name: {
            pattern_name: {alg_name: 0.0 for alg_name in algorithms.keys()}
            for pattern_name in patterns.keys()
        }
        for text_name in texts.keys()
    }

    print("\n--- Substring search analysis (seconds) ---")

    for text_name, text in texts.items():
        for pattern_name, pattern in patterns.items():
            print(f"\n*** Text: {text_name}, pattern: {pattern_name!r} ***")
            for alg_name, func in algorithms.items():
                t = (
                    timeit.timeit(
                        stmt=lambda f=func, t_=text, p_=pattern: f(t_, p_),
                        number=run_qty,
                    )
                    / run_qty
                )
                results[text_name][pattern_name][alg_name] = t
                print(f"{alg_name:>11}: {t:.8f}s")

    return results


def display_search_results(results):
    """
    Display results using bar charts for each text+pattern combination.
    """
    for text_name, patterns in results.items():
        for pattern_name, times in patterns.items():
            algorithms = list(times.keys())
            values = [times[a] for a in algorithms]

            plt.figure(figsize=(7, 4))
            plt.bar(algorithms, values)
            plt.ylabel("Time (seconds)")
            plt.title(f"Performance for {text_name}, pattern: {pattern_name}")
            plt.grid(axis="y", linestyle="--", alpha=0.5)
            plt.show()


if __name__ == "__main__":
    texts = load_articles()

    patterns = {
        "existing": "алгоритмів",
        "fake": "test123456",
    }

    results = analyze_search_algorithms(texts, patterns, run_qty=500)

    display_search_results(results)
