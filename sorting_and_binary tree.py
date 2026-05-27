"""
Tugas Algoritma — Bab 12 & 13
==============================
Kelas:
  - ListNode        : node singly linked list
  - AdvancedSorter  : Merge Sort array, Merge Sort linked list, Quick Sort
  - ExprHeapSorter  : Expression Tree, In-Place HeapSort, Complete Tree Validator
"""

import math
from typing import List, Optional
from collections import deque


# ===========================================================================
# NODE SINGLY LINKED LIST
# ===========================================================================

class ListNode:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next


# ===========================================================================
# BAB 12 — AdvancedSorter
# ===========================================================================

class AdvancedSorter:
    def __init__(self):
        pass

    # =========================================================
    # 1. ARRAY MERGE SORT (Virtual Sublists + Single tmpArray)
    # =========================================================

    def sort_array(self, arr: List[int]) -> List[int]:
        """Mengurutkan arr secara ascending (in-place) menggunakan Merge Sort.
        Hanya mengalokasi satu tmpArray berukuran n di awal — tidak ada
        sublist fisik atau alokasi tambahan di dalam rekursi.
        """
        if len(arr) <= 1:
            return arr
        tmp_array = [0] * len(arr)          # satu-satunya alokasi tambahan
        self._rec_merge_sort(arr, 0, len(arr) - 1, tmp_array)
        return arr

    def _rec_merge_sort(self, arr, first, last, tmp_array):
        """Rekursif bagi-dan-gabung menggunakan indeks virtual."""
        if first >= last:
            return
        mid = (first + last) // 2
        self._rec_merge_sort(arr, first, mid, tmp_array)
        self._rec_merge_sort(arr, mid + 1, last, tmp_array)
        self._merge_virtual(arr, first, mid, last, tmp_array)

    def _merge_virtual(self, arr, left_start, mid, right_end, tmp_array):
        """Gabungkan dua virtual sublist arr[left_start..mid] dan
        arr[mid+1..right_end] menggunakan tmp_array sebagai buffer sementara.

        Stabilitas dijaga dengan kondisi <=:
          jika arr[a] <= arr[b] → ambil dari sublist kiri terlebih dahulu.
        """
        a = left_start      # penunjuk sublist kiri
        b = mid + 1         # penunjuk sublist kanan
        k = left_start      # penunjuk output di tmp_array

        while a <= mid and b <= right_end:
            # "<=" menjamin stabilitas: elemen kiri dipilih saat sama
            if arr[a] <= arr[b]:
                tmp_array[k] = arr[a]
                a += 1
            else:
                tmp_array[k] = arr[b]
                b += 1
            k += 1

        while a <= mid:
            tmp_array[k] = arr[a]
            a += 1
            k += 1

        while b <= right_end:
            tmp_array[k] = arr[b]
            b += 1
            k += 1

        # Kembalikan hasil gabungan ke arr
        for i in range(left_start, right_end + 1):
            arr[i] = tmp_array[i]

    # =========================================================
    # 2. LINKED LIST MERGE SORT (Fast-Slow + Dummy Merge)
    # =========================================================

    def sort_linked_list(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """Mengurutkan singly linked list secara ascending menggunakan
        Merge Sort. Tidak mengalokasi node baru selama sorting
        (kecuali 1 dummy node statis per pemanggilan _merge_linked_lists).
        """
        if head is None or head.next is None:
            return head

        right_head = self._split_linked_list(head)
        left_head  = head

        left_sorted  = self.sort_linked_list(left_head)
        right_sorted = self.sort_linked_list(right_head)

        return self._merge_linked_lists(left_sorted, right_sorted)

    def _split_linked_list(self, head: ListNode) -> Optional[ListNode]:
        """Temukan titik tengah list dengan teknik fast-slow pointer
        (satu traversal, tanpa menghitung panjang).

        midPoint : bergerak 1 langkah per iterasi → berhenti di tengah
        curNode  : bergerak 2 langkah per iterasi → berhenti di akhir

        Setelah loop, midPoint berada di node tengah.
        Putus sambungan di sana lalu kembalikan head sublist kanan.
        """
        midPoint = head       # lambat: maju 1 langkah
        curNode  = head.next  # cepat : maju 2 langkah

        while curNode is not None and curNode.next is not None:
            midPoint = midPoint.next
            curNode  = curNode.next.next

        right_head    = midPoint.next
        midPoint.next = None            # putus tautan — akhiri sublist kiri
        return right_head

    def _merge_linked_lists(
        self,
        listA: Optional[ListNode],
        listB: Optional[ListNode]
    ) -> Optional[ListNode]:
        """Gabungkan dua linked list yang sudah terurut secara STABLE.

        Teknik dummy node + tail reference:
          - dummy : node sentinal statis (tidak ikut hasil akhir)
          - tail  : selalu menunjuk ke node terakhir dalam hasil gabungan

        Tidak ada alokasi node baru; hanya pointer .next yang digeser.
        Kompleksitas ruang O(1) (di luar stack rekursi).
        """
        dummy = ListNode(0)   # node sentinal
        tail  = dummy

        while listA is not None and listB is not None:
            # "<=" menjamin stabilitas: elemen listA dipilih saat sama
            if listA.data <= listB.data:
                tail.next = listA
                listA = listA.next
            else:
                tail.next = listB
                listB = listB.next
            tail = tail.next

        tail.next = listA if listA is not None else listB

        return dummy.next

    # =========================================================
    # 3. QUICK SORT PARTITION (Median-of-Three Pivot)
    # =========================================================

    def sort_array_quick(self, arr: List[int]) -> List[int]:
        """Entry-point Quick Sort dengan depth-limit fallback ke Merge Sort."""
        if len(arr) <= 1:
            return arr
        n = len(arr)
        max_depth = int(2 * math.log2(n)) if n > 1 else 1
        self._quick_sort_recursive(arr, 0, n - 1, max_depth)
        return arr

    def _quick_sort_recursive(self, arr, first, last, depth_limit):
        """Rekursi Quick Sort. Jika depth_limit habis, beralih ke
        Merge Sort untuk mencegah kompleksitas O(n²).
        """
        if first >= last:
            return

        if depth_limit == 0:
            # Fallback: urutkan sub-array dengan Merge Sort
            sub = arr[first:last + 1]
            self.sort_array(sub)
            arr[first:last + 1] = sub
            return

        pivot_idx = self.partition_quick(arr, first, last)
        self._quick_sort_recursive(arr, first,         pivot_idx - 1, depth_limit - 1)
        self._quick_sort_recursive(arr, pivot_idx + 1, last,          depth_limit - 1)

    def partition_quick(self, arr: List[int], first: int, last: int) -> int:
        """Pilih pivot menggunakan Median-of-Three (first, mid, last),
        kemudian lakukan partisi in-place (Hoare-style, sesuai Listing 12.5).

        Langkah:
          1. Hitung mid = (first + last) // 2.
          2. Urutkan triplet sehingga median berada di arr[first] (pivot).
          3. Dua penunjuk i dan j bergerak saling mendekati.
          4. Tempatkan pivot pada posisi akhirnya, kembalikan indeks itu.

        Catatan stabilitas:
          Partisi standar tidak inherently stable. Untuk data integer
          ini tidak menjadi masalah karena nilai yang sama tidak perlu
          mempertahankan urutan relatif (sesuai persyaratan Quick Sort).
        """
        mid = (first + last) // 2

        # Median-of-Three: urutkan triplet agar arr[mid] adalah median
        if arr[first] > arr[mid]:
            arr[first], arr[mid] = arr[mid], arr[first]
        if arr[first] > arr[last]:
            arr[first], arr[last] = arr[last], arr[first]
        if arr[mid] > arr[last]:
            arr[mid], arr[last] = arr[last], arr[mid]
        # Pindahkan median ke arr[first] sebagai pivot
        arr[first], arr[mid] = arr[mid], arr[first]

        pivot = arr[first]

        # Hoare-style dua penunjuk (sesuai Listing 12.5)
        i = first + 1
        j = last

        while True:
            while i <= last and arr[i] < pivot:
                i += 1
            while j > first and arr[j] > pivot:
                j -= 1
            if i >= j:
                break
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
            j -= 1

        # Tempatkan pivot pada posisi akhirnya
        arr[first], arr[j] = arr[j], arr[first]
        return j


# ===========================================================================
# BAB 13 — ExprHeapSorter
# ===========================================================================

class ExprHeapSorter:

    OPERATORS = {'+', '-', '*', '/'}

    def __init__(self, expr_str: str):
        self.expr   = expr_str
        self.values = []    # diisi oleh parse_and_evaluate

    # =========================================================
    # 1. EXPRESSION TREE BUILDER & EVALUATOR
    # =========================================================

    def parse_and_evaluate(self) -> List[int]:
        """Tokenisasi → bangun pohon → evaluasi → kembalikan list nilai."""
        tokens = self._tokenize(self.expr)
        root   = self._build_tree(tokens)
        result = self._eval_tree(root)
        self.values = [int(result)]
        return self.values

    def _tokenize(self, expr: str) -> deque:
        """Ubah string ekspresi menjadi deque token.
        Token: '(', ')', operator, bilangan bulat. Spasi diabaikan.
        Bilangan multi-digit didukung.
        """
        tokens = deque()
        i = 0
        while i < len(expr):
            ch = expr[i]
            if ch == ' ':
                i += 1
                continue
            if ch in ('(', ')') or ch in self.OPERATORS:
                tokens.append(ch)
                i += 1
            elif ch.isdigit():
                j = i
                while j < len(expr) and expr[j].isdigit():
                    j += 1
                tokens.append(int(expr[i:j]))
                i = j
            else:
                raise ValueError(f"Token tidak valid: '{ch}'")
        return tokens

    def _build_tree(self, tokens: deque) -> Optional[dict]:
        """Bangun pohon ekspresi rekursif dari antrian token
        (sesuai Listing 13.9).

        Pola rekursi untuk ekspresi terparentheses penuh:
          '('     → buat subtree kiri → ambil operator
                  → buat subtree kanan → buang ')'
          integer → leaf node langsung

        Node: {'val': operator|operand, 'left': node|None, 'right': node|None}
        """
        if not tokens:
            return None

        token = tokens.popleft()

        if token == '(':
            left_child = self._build_tree(tokens)

            if not tokens:
                raise ValueError("Ekspresi tidak lengkap: operator tidak ditemukan.")
            operator = tokens.popleft()
            if operator not in self.OPERATORS:
                raise ValueError(f"Diharapkan operator, ditemukan: '{operator}'")

            right_child = self._build_tree(tokens)

            # Buang ')' penutup
            if tokens and tokens[0] == ')':
                tokens.popleft()

            return {'val': operator, 'left': left_child, 'right': right_child}

        elif isinstance(token, int):
            return {'val': token, 'left': None, 'right': None}

        else:
            raise ValueError(f"Token tidak terduga saat membangun pohon: '{token}'")

    def _eval_tree(self, node: Optional[dict]):
        """Evaluasi pohon ekspresi secara postorder (kiri → kanan → root).

        Kompleksitas ruang stack rekursi = O(h), h = tinggi pohon.
        Untuk ekspresi terparentheses penuh, h ≈ kedalaman kurung bersarang.
        """
        if node is None:
            return 0

        # Leaf node: kembalikan nilai operand
        if node['left'] is None and node['right'] is None:
            return node['val']

        left_val  = self._eval_tree(node['left'])
        right_val = self._eval_tree(node['right'])

        op = node['val']
        if op == '+': return left_val + right_val
        if op == '-': return left_val - right_val
        if op == '*': return left_val * right_val
        if op == '/':
            if right_val == 0:
                raise ValueError("Pembagian nol terdeteksi dalam ekspresi.")
            return left_val // right_val
        raise ValueError(f"Operator tidak dikenal: '{op}'")

    # =========================================================
    # 2 & 3. IN-PLACE HEAPSORT
    # =========================================================

    def heapsort_inplace(self, arr: List[int]) -> List[int]:
        """Urutkan arr secara ascending menggunakan in-place heapsort.

        Fase 1 — Bangun max-heap dari daun ke akar:
          Mulai dari indeks n//2 - 1 (parent node terakhir) turun ke 0.

        Fase 2 — Ekstraksi & sort:
          Tukar arr[0] (maks) dengan arr[end], kurangi heap_size,
          sift-down dari akar. Ulangi sampai heap berukuran 1.

        Kompleksitas waktu O(n log n), ruang O(1) — benar-benar in-place.
        """
        n = len(arr)
        if n <= 1:
            return arr

        # Fase 1: bangun max-heap
        for i in range(n // 2 - 1, -1, -1):
            self._sift_down(arr, n, i)

        # Fase 2: ekstraksi satu per satu
        for end in range(n - 1, 0, -1):
            arr[0], arr[end] = arr[end], arr[0]
            self._sift_down(arr, end, 0)

        return arr

    def _sift_down(self, arr: List[int], heap_size: int, idx: int):
        """Pulihkan heap-order property dengan menggeser node ke bawah
        (sesuai Listing 13.10 & 13.12).

        Rumus indeks: left = 2*idx+1, right = 2*idx+2.
        Cari largest di antara idx, left, right yang dalam batas heap_size.
        Jika largest != idx, tukar lalu lanjutkan dari posisi baru.

        Perbandingan maksimum per panggilan: 2 * floor(log2(n)).
        """
        while True:
            left    = 2 * idx + 1
            right   = 2 * idx + 2
            largest = idx

            if left < heap_size and arr[left] > arr[largest]:
                largest = left
            if right < heap_size and arr[right] > arr[largest]:
                largest = right

            if largest == idx:
                break

            arr[idx], arr[largest] = arr[largest], arr[idx]
            idx = largest

    # =========================================================
    # 4. COMPLETE BINARY TREE VALIDATOR
    # =========================================================

    def is_complete_tree(self, arr: List[int]) -> bool:
        """Verifikasi apakah array memenuhi properti complete binary tree.

        Algoritma BFS-flag:
          Begitu ditemukan node tanpa anak lengkap (found_incomplete = True),
          semua node setelahnya harus berupa leaf. Jika ada yang masih punya
          anak → bukan complete tree.

        Kondisi tidak valid juga:
          Node punya anak kanan tetapi tidak punya anak kiri.
        """
        n = len(arr)
        if n == 0:
            return True

        found_incomplete = False

        for i in range(n):
            left      = 2 * i + 1
            right     = 2 * i + 2
            has_left  = left  < n
            has_right = right < n

            if found_incomplete:
                if has_left or has_right:
                    return False
            else:
                if not has_left and has_right:
                    return False    # anak kanan ada tanpa anak kiri — mustahil
                if not has_right:
                    found_incomplete = True

        return True


# ===========================================================================
# HELPER LINKED LIST
# ===========================================================================

def linked_list_to_list(head):
    result = []
    while head:
        result.append(head.data)
        head = head.next
    return result

def list_to_linked_list(data):
    if not data:
        return None
    head = ListNode(data[0])
    cur  = head
    for val in data[1:]:
        cur.next = ListNode(val)
        cur = cur.next
    return head


# ===========================================================================
# UJI COBA
# ===========================================================================

if __name__ == "__main__":

    # ------------------------------------------------------------------
    # BAB 12 — AdvancedSorter
    # ------------------------------------------------------------------
    sorter = AdvancedSorter()

    print("=" * 55)
    print("BAB 12 — AdvancedSorter")
    print("=" * 55)

    # 1. Array Merge Sort
    print("\n--- 1. Array Merge Sort ---")
    arr1 = [38, 27, 43, 3, 9, 82, 10]
    print("Sebelum :", arr1)
    sorter.sort_array(arr1)
    print("Sesudah :", arr1)

    arr2 = [5, 3, 5, 1, 3, 2, 5]
    print("\nStabilitas (duplikat):")
    print("Sebelum :", arr2)
    sorter.sort_array(arr2)
    print("Sesudah :", arr2)

    # 2. Linked List Merge Sort
    print("\n--- 2. Linked List Merge Sort ---")
    ll = list_to_linked_list([6, 3, 8, 1, 5, 2, 9, 4])
    print("Sebelum :", linked_list_to_list(ll))
    sorted_ll = sorter.sort_linked_list(ll)
    print("Sesudah :", linked_list_to_list(sorted_ll))

    # 3. Quick Sort (Median-of-Three + depth-limit)
    print("\n--- 3. Quick Sort (Median-of-Three) ---")
    arr3 = [64, 34, 25, 12, 22, 11, 90]
    print("Sebelum :", arr3)
    sorter.sort_array_quick(arr3)
    print("Sesudah :", arr3)

    arr4 = list(range(20, 0, -1))
    print("\nWorst-case descending (n=20):")
    print("Sebelum :", arr4)
    sorter.sort_array_quick(arr4)
    print("Sesudah :", arr4)

    # ------------------------------------------------------------------
    # BAB 13 — ExprHeapSorter
    # ------------------------------------------------------------------
    print("\n" + "=" * 55)
    print("BAB 13 — ExprHeapSorter")
    print("=" * 55)

    # 1. Expression Tree
    print("\n--- 1. Expression Tree & Evaluator ---")
    expr = "((8 * 5) + (9 / (7 - 4)))"
    ehs  = ExprHeapSorter(expr)
    val  = ehs.parse_and_evaluate()
    print(f"Ekspresi : {expr}")
    print(f"Hasil    : {val[0]}")   # 8*5=40, 7-4=3, 9/3=3, 40+3=43

    try:
        ExprHeapSorter("(8 / (3 - 3))").parse_and_evaluate()
    except ValueError as e:
        print(f"Pembagian nol tertangkap: {e}")

    # 2 & 3. In-Place HeapSort
    print("\n--- 2 & 3. In-Place HeapSort ---")
    data = [val[0], 12, 7, 3, 99, 55, 23, 1]
    print("Sebelum :", data)
    ehs2 = ExprHeapSorter("")
    ehs2.heapsort_inplace(data)
    print("Sesudah :", data)

    data2 = [5, 1, 5, 3, 5, 2]
    print("\nDuplikat sebelum :", data2)
    ehs2.heapsort_inplace(data2)
    print("Duplikat sesudah :", data2)

    # 4. Complete Tree Validator
    print("\n--- 4. Complete Binary Tree Validator ---")
    for a in [[1, 3, 5, 7, 23, 55, 99], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5, 6]]:
        print(f"Array {a} → Complete: {ehs2.is_complete_tree(a)}")

    print("\nSemua uji selesai.")
