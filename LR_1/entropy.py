import collections
import math
import matplotlib.pyplot as plt

def calculate_entropy(text):
    """Обчислює ентропію тексту за формулою Шеннона."""
    frequency = collections.Counter(text)
    total_chars = len(text)
    entropy = -sum((count / total_chars) * math.log2(count / total_chars) for count in frequency.values())
    return entropy

def load_and_clean_text(filepath):
    """Завантажує текст із файлу та очищає його від зайвих символів."""
    with open(filepath, 'r', encoding='utf-8') as file:
        text = file.read()
    return ''.join(filter(str.isalnum, text.lower()))

def plot_entropy_vs_text_size(text, language):
    """Будує графік залежності ентропії від розміру тексту."""
    sizes = list(range(100, len(text), len(text) // 10))
    entropies = [calculate_entropy(text[:size]) for size in sizes]
    
    plt.plot(sizes, entropies, marker='o', label=language)
    plt.xlabel("Розмір тексту (символи)")
    plt.ylabel("Ентропія (біт/символ)")
    plt.title("Залежність ентропії від розміру тексту")
    plt.legend()
    plt.grid()

# Завантаження текстів
ukr_text = load_and_clean_text('ukrainian.txt')
eng_text = load_and_clean_text('english.txt')
chi_text = load_and_clean_text('chinese.txt')

# Обчислення ентропії
ukr_entropy = calculate_entropy(ukr_text)
eng_entropy = calculate_entropy(eng_text)
chi_entropy = calculate_entropy(chi_text)

# Вивід результатів
print(f'Ентропія українського тексту: {ukr_entropy:.4f}')
print(f'Ентропія англійського тексту: {eng_entropy:.4f}')
print(f'Ентропія китайського тексту: {chi_entropy:.4f}')

# Побудова графіків
plt.figure(figsize=(10, 6))
plot_entropy_vs_text_size(ukr_text, "Українська")
plot_entropy_vs_text_size(eng_text, "Англійська")
plot_entropy_vs_text_size(chi_text, "Китайська")
plt.show()
