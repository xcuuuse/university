import numpy as np
import matplotlib.pyplot as plt

def dft(x):
    x = np.asarray(x, dtype=float)
    N = x.shape[0]
    n = np.arange(N)
    k = n.reshape((N, 1))
    M = np.exp(-2j * np.pi * k * n / N)
    return np.dot(M, x)

def fft(x):
    x = np.asarray(x, dtype=float)
    N = x.shape[0]
    if N % 2 != 0:
        raise ValueError("size has to be a power of 2")
    elif N <= 32:
        return dft(x)
    else:
        x_even = fft(x[::2])
        x_odd = fft(x[1::2])
        factor = np.exp(-2j * np.pi * np.arange(N) / N)
        return np.concatenate([x_even + factor[:N // 2] * x_odd, x_even + factor[N // 2:] * x_odd])


def test_signal(func_name, freqs, amps, N=1024, fs=1024):
    t = np.arange(N) / fs
    func = np.sin if func_name == "sin" else np.cos
    x = sum(a * func(2 * np.pi * f * t) for f, a in zip(freqs, amps))
    X = fft(x)
    freq_axis = np.arange(N) * fs / N
    half = N // 2
    amp_spectrum = 2 * np.abs(X[:half]) / N
    ok_ref = np.allclose(X, np.fft.fft(x))
    peaks = np.sort(np.argsort(amp_spectrum)[-len(freqs):])
    found = freq_axis[peaks]
    mask = np.ones(half, bool)
    mask[peaks] = False
    fig, ax = plt.subplots(2, 1, figsize=(10, 6))
    ax[0].plot(t[:200], x[:200])
    ax[0].set_title(f"Входной сигнал: {func_name}, f = {freqs} Гц")
    ax[0].set_xlabel("t, с")
    ax[0].grid()
    ax[1].stem(freq_axis[:half], amp_spectrum)
    ax[1].set_title("Амплитудный спектр (наш FFT)")
    ax[1].set_xlabel("Частота, Гц")
    ax[1].set_ylabel("Амплитуда")
    ax[1].grid()
    plt.tight_layout()
    plt.savefig(f"spectrum_{func_name}.png", dpi=100)
    plt.show()
    return ok_ref and np.allclose(sorted(freqs), found)


if __name__ == "__main__":
    test_signal("sin", freqs=[50], amps=[1.0])
    test_signal("cos", freqs=[30, 120, 300], amps=[1.0, 0.5, 2.0])
    try:
        fft(np.zeros(100))
    except ValueError as e:
        print(f"\nN=100 -> ValueError: {e}")