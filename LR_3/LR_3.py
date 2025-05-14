import heapq
import os
import zlib
import lzma
from collections import Counter, defaultdict
import matplotlib.pyplot as plt

# Крок 1. Хаффманівське дерево
class Node:
    def __init__(self, char=None, freq=0):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):  # Для heapq
        return self.freq < other.freq

def build_huffman_tree(freq_table):
    heap = [Node(char, freq) for char, freq in freq_table.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        n1 = heapq.heappop(heap)
        n2 = heapq.heappop(heap)
        merged = Node(freq=n1.freq + n2.freq)
        merged.left = n1
        merged.right = n2
        heapq.heappush(heap, merged)

    return heap[0]

def generate_codes(node, prefix="", codebook=None):
    if codebook is None:
        codebook = dict()
    if node:
        if node.char is not None:
            codebook[node.char] = prefix
        generate_codes(node.left, prefix + "0", codebook)
        generate_codes(node.right, prefix + "1", codebook)
    return codebook

def huffman_encode(text, codebook):
    return ''.join(codebook[char] for char in text)

def decode_huffman(encoded, root):
    decoded = []
    node = root
    for bit in encoded:
        node = node.left if bit == '0' else node.right
        if node.char:
            decoded.append(node.char)
            node = root
    return ''.join(decoded)

# Крок 2. Стиснення іншими методами
def compress_zlib(text):
    return zlib.compress(text.encode())

def compress_lzma(text):
    return lzma.compress(text.encode())

# Крок 3. Основна логіка
def main():
    with open("input.txt", "r", encoding="utf-8") as f:
        text = f.read()

    freq = Counter(text)
    huff_root = build_huffman_tree(freq)
    codes = generate_codes(huff_root)
    encoded = huffman_encode(text, codes)

    # Статистика
    original_size = len(text.encode('utf-8')) * 8
    huff_size = len(encoded)
    zlib_size = len(compress_zlib(text)) * 8
    lzma_size = len(compress_lzma(text)) * 8

    # Таблиця кодів
    sorted_codes = sorted(codes.items(), key=lambda x: -freq[x[0]])
    code_table = "\n".join([f"{char!r}: {codes[char]} (частота: {freq[char]})" for char, _ in sorted_codes])

    # Графік
    lengths = [len(codes[char]) for char in freq]
    f_values = [freq[char] for char in freq]
    plt.figure(figsize=(10, 6))
    plt.scatter(f_values, lengths, alpha=0.7)
    plt.title("Графік: Частота vs Довжина коду")
    plt.xlabel("Частота символу")
    plt.ylabel("Довжина Хаффман-коду")
    plt.grid(True)
    plt.savefig("code_lengths_distribution.png")
    plt.close()

    # Запис звіту
    with open("report.txt", "w", encoding="utf-8") as f:
        f.write("Лабораторна №3 — Порівняння методів стиснення\n")
        f.write("="*50 + "\n\n")
        f.write("1. Код Хаффмана\n")
        f.write(f"  Розмір: {huff_size} біт\n")
        f.write("2. Zlib (LZ77)\n")
        f.write(f"  Розмір: {zlib_size} біт\n")
        f.write("3. LZMA (LZW)\n")
        f.write(f"  Розмір: {lzma_size} біт\n")
        f.write("4. Початковий розмір: " + str(original_size) + " біт\n\n")
        f.write("Коефіцієнти стиснення:\n")
        f.write(f"  Хаффман: {original_size/huff_size:.2f}x\n")
        f.write(f"  Zlib: {original_size/zlib_size:.2f}x\n")
        f.write(f"  LZMA: {original_size/lzma_size:.2f}x\n\n")
        f.write("="*50 + "\n\n")
        f.write("Таблиця кодів Хаффмана:\n\n")
        f.write(code_table)

if __name__ == "__main__":
    main()
