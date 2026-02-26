from collections import Counter
import csv


def build_sequence(max_digits=5000000, regime="ratio_to_zero", C=2):
    """
    Build decimal digits of f(x,r(t),N0) up to ~max_digits (excluding '0.')
    x_t = '7', |x| = 1
    g(t) = str(t)
    r(t) depends on regime:
      - 'ratio_to_zero'   : r(t) = 1
      - 'ratio_to_infty'  : r(t) = t
      - 'ratio_to_const'  : r(t) = round(C * len(g(t)))
    """
    digits = []  # we collect just the digits after '0.'
    t = 1
    while len(digits) < max_digits:
        g_t = str(t)
        if regime == "ratio_to_zero":
            r_t = 1
        elif regime == "ratio_to_infty":
            r_t = t
        elif regime == "ratio_to_const":
            r_t = max(1, round(C * len(g_t)))
        else:
            raise ValueError("Unknown regime")

        # x_t = '7' repeated r_t times
        x_block = '7' * r_t
        block = x_block + g_t
        digits.extend(block)
        t += 1
    # truncate to exactly max_digits
    return ''.join(digits[:max_digits])


def digit_frequencies(s):
    cnt = Counter(s)
    n = len(s)
    return {d: cnt[d] / n for d in '0123456789'}


def bigram_frequencies(s):
    if len(s) < 2:
        return {f"{i}{j}": 0.0 for i in '0123456789' for j in '0123456789'}
    bigrams = [s[i:i + 2] for i in range(len(s) - 1)]
    cnt = Counter(bigrams)
    n = len(bigrams)
    return {bg: cnt[bg] / n for i in '0123456789' for j in '0123456789' for bg in [f"{i}{j}"]}


def save_to_csv(filename, data):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Regime'] + sorted(data[0][1].keys()))
        for regime_name, freqs in data:
            writer.writerow([regime_name] + [freqs[k] for k in sorted(freqs)])


if __name__ == "__main__":
    maxN = 5000000  # increase if you want more accuracy

    # Case 1: (r(t)*|x|)/|g(t)| → 0
    seq_zero = build_sequence(max_digits=maxN, regime="ratio_to_zero")
    print("Case 1: ratio -> 0, r(t)=1")
    print()
    freq_zero_digit = digit_frequencies(seq_zero)
    freq_zero_bigram = bigram_frequencies(seq_zero)

    # Case 2: (r(t)*|x|)/|g(t)| → ∞
    seq_inf = build_sequence(max_digits=maxN, regime="ratio_to_infty")
    print("Case 2: ratio -> ∞, r(t)=t")
    print()
    freq_inf_digit = digit_frequencies(seq_inf)
    freq_inf_bigram = bigram_frequencies(seq_inf)

    # Case 3: (r(t)*|x|)/|g(t)| → C > 0 (e.g. C=2)
    C = 2
    seq_const = build_sequence(max_digits=maxN, regime="ratio_to_const", C=C)
    print(f"Case 3: ratio -> C={C}, r(t)≈C*len(g(t))")
    print()
    freq_const_digit = digit_frequencies(seq_const)
    freq_const_bigram = bigram_frequencies(seq_const)

    # Save digit frequencies to CSV
    digit_data = [
        ("ratio_to_zero", freq_zero_digit),
        ("ratio_to_infty", freq_inf_digit),
        ("ratio_to_const_C=2", freq_const_digit)
    ]
    save_to_csv("digit_frequencies.csv", digit_data)

    # Save bigram frequencies to CSV
    bigram_data = [
        ("ratio_to_zero", freq_zero_bigram),
        ("ratio_to_infty", freq_inf_bigram),
        ("ratio_to_const_C=2", freq_const_bigram)
    ]
    save_to_csv("bigram_frequencies.csv", bigram_data)

    print("CSVs saved: digit_frequencies.csv and bigram_frequencies.csv")
