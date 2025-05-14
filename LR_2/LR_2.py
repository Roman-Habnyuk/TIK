import numpy as np
import random
import matplotlib.pyplot as plt
from collections import Counter
import math

# --- Генерація матриці переходів ---
def generate_transition_matrix():
    return np.array([
        [0.4, 0.3, 0.2, 0.1],
        [0.1, 0.4, 0.3, 0.2],
        [0.2, 0.1, 0.4, 0.3],
        [0.3, 0.2, 0.1, 0.4]
    ])

# --- Генерація послідовності ---
def generate_sequence(matrix, length=1000, alphabet=['A', 'B', 'C', 'D']):
    sequence = [random.choice(alphabet)]
    for _ in range(length - 1):
        prev_index = alphabet.index(sequence[-1])
        next_symbol = random.choices(alphabet, weights=matrix[prev_index])[0]
        sequence.append(next_symbol)
    return ''.join(sequence)

# --- Обчислення ентропії ---
def calculate_entropy(text):
    frequencies = Counter(text)
    total = len(text)
    return -sum((count / total) * math.log2(count / total) for count in frequencies.values())

# --- Кумулятивна ентропія ---
def cumulative_entropy(sequence):
    entropies = []
    for i in range(10, len(sequence)+1, 10):
        chunk = sequence[:i]
        entropies.append(calculate_entropy(chunk))
    return entropies

# --- Побудова графіків ---
def plot_histogram(sequence):
    frequencies = Counter(sequence)
    plt.figure(figsize=(6, 4))
    plt.bar(frequencies.keys(), frequencies.values(), color='skyblue')
    plt.title('Частоти символів')
    plt.xlabel('Символ')
    plt.ylabel('Кількість')
    plt.savefig('symbol_frequencies.png')
    plt.close()

def plot_entropy_growth(entropy_values):
    plt.figure(figsize=(8, 4))
    plt.plot(range(10, len(entropy_values)*10+1, 10), entropy_values, color='green')
    plt.title('Кумулятивна ентропія (довжина послідовності)')
    plt.xlabel('Кількість символів')
    plt.ylabel('Ентропія')
    plt.grid(True)
    plt.savefig('entropy_growth.png')
    plt.close()

# --- Основна програма ---
if __name__ == "__main__":
    alphabet = ['A', 'B', 'C', 'D']
    matrix = generate_transition_matrix()
    sequence = generate_sequence(matrix, 1000, alphabet)
    entropy = calculate_entropy(sequence)

    # Зберігаємо у файл
    with open('sequence_and_entropy.txt', 'w', encoding='utf-8') as f:
        f.write("Згенерована послідовність:\n")
        f.write(sequence + '\n\n')
        f.write(f"Обчислена ентропія: {entropy:.4f} біт/символ\n")

    # Побудова графіків
    plot_histogram(sequence)
    entropy_values = cumulative_entropy(sequence)
    plot_entropy_growth(entropy_values)

    print("Результати збережено у файл sequence_and_entropy.txt та графіки у .png")
