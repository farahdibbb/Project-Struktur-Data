# ============================================================
# SOAL 1(a) - Big Integer ADT menggunakan Singly Linked List
# Setiap digit disimpan dalam node terpisah, urutan dari
# digit paling tidak signifikan (least significant) ke paling signifikan.
# ============================================================

class Node:
    """Node untuk singly linked list."""
    def __init__(self, digit):
        self.digit = digit      # menyimpan satu digit (0-9)
        self.next = None


class BigInteger:
    """
    Big Integer ADT menggunakan singly linked list.
    Digit disimpan dari least-significant ke most-significant.
    Contoh: 45839 -> head -> [9] -> [3] -> [8] -> [5] -> [4] -> None
    Mendukung bilangan negatif dengan atribut self.negative.
    """

    def __init__(self, initValue="0"):
        self.head = None
        self.negative = False
        self._build_from_string(str(initValue))

    # ----------------------------------------------------------
    # Helper internal: membangun linked list dari string
    # ----------------------------------------------------------
    def _build_from_string(self, s):
        s = s.strip()
        if not s:
            s = "0"

        # Tangani tanda negatif
        if s[0] == '-':
            self.negative = True
            s = s[1:]
        elif s[0] == '+':
            s = s[1:]

        # Hapus leading zeros
        s = s.lstrip('0') or '0'

        # Validasi: hanya digit
        if not s.isdigit():
            raise ValueError(f"Nilai tidak valid: '{s}'")

        # Masukkan digit dari kiri ke kanan -> head akan menunjuk digit terkecil
        self.head = None
        for ch in s:
            self._prepend(int(ch))

    def _prepend(self, digit):
        """Sisipkan node baru di depan (head) linked list."""
        node = Node(digit)
        node.next = self.head
        self.head = node

    # ----------------------------------------------------------
    # Helper: konversi linked list ke integer Python (internal)
    # ----------------------------------------------------------
    def _to_int(self):
        result = 0
        multiplier = 1
        current = self.head
        while current:
            result += current.digit * multiplier
            multiplier *= 10
            current = current.next
        return -result if self.negative else result

    # ----------------------------------------------------------
    # Helper: buat BigInteger baru dari integer Python
    # ----------------------------------------------------------
    @classmethod
    def _from_int(cls, value):
        return cls(str(value))

    # ----------------------------------------------------------
    # toString() - representasi string
    # ----------------------------------------------------------
    def toString(self):
        digits = []
        current = self.head
        while current:
            digits.append(str(current.digit))
            current = current.next
        # digits sekarang dalam urutan least-significant dulu, balikkan
        digits.reverse()
        result = ''.join(digits)
        if self.negative and result != '0':
            result = '-' + result
        return result

    def __repr__(self):
        return f"BigInteger('{self.toString()}')"

    def __str__(self):
        return self.toString()

    # ----------------------------------------------------------
    # comparable(other) - perbandingan logis
    # ----------------------------------------------------------
    def comparable(self, other, operator):
        """
        Membandingkan self dengan other BigInteger.
        operator: '<', '<=', '>', '>=', '==', '!='
        """
        a = self._to_int()
        b = other._to_int()
        ops = {
            '<':  a < b,
            '<=': a <= b,
            '>':  a > b,
            '>=': a >= b,
            '==': a == b,
            '!=': a != b,
        }
        if operator not in ops:
            raise ValueError(f"Operator tidak dikenal: '{operator}'")
        return ops[operator]

    # Dunder methods untuk operator perbandingan
    def __lt__(self, other):  return self.comparable(other, '<')
    def __le__(self, other):  return self.comparable(other, '<=')
    def __gt__(self, other):  return self.comparable(other, '>')
    def __ge__(self, other):  return self.comparable(other, '>=')
    def __eq__(self, other):  return self.comparable(other, '==')
    def __ne__(self, other):  return self.comparable(other, '!=')

    # ----------------------------------------------------------
    # arithmetic(rhsInt, op) - operasi aritmatika
    # ----------------------------------------------------------
    def arithmetic(self, rhsInt, op):
        """
        Melakukan operasi aritmatika antara self dan rhsInt.
        op: '+', '-', '*', '//', '%', '**'
        Mengembalikan BigInteger baru.
        """
        a = self._to_int()
        b = rhsInt._to_int()
        ops = {
            '+':  a + b,
            '-':  a - b,
            '*':  a * b,
            '//': a // b,
            '%':  a % b,
            '**': a ** b,
        }
        if op not in ops:
            raise ValueError(f"Operator tidak dikenal: '{op}'")
        return BigInteger._from_int(ops[op])

    # Dunder methods untuk operator aritmatika
    def __add__(self, other):  return self.arithmetic(other, '+')
    def __sub__(self, other):  return self.arithmetic(other, '-')
    def __mul__(self, other):  return self.arithmetic(other, '*')
    def __floordiv__(self, other): return self.arithmetic(other, '//')
    def __mod__(self, other):  return self.arithmetic(other, '%')
    def __pow__(self, other):  return self.arithmetic(other, '**')

    # ----------------------------------------------------------
    # bitwise_ops(rhsInt, op) - operasi bitwise
    # ----------------------------------------------------------
    def bitwise_ops(self, rhsInt, op):
        """
        Melakukan operasi bitwise antara self dan rhsInt.
        op: '|', '&', '^', '<<', '>>'
        Mengembalikan BigInteger baru.
        """
        a = self._to_int()
        b = rhsInt._to_int()
        ops = {
            '|':  a | b,
            '&':  a & b,
            '^':  a ^ b,
            '<<': a << b,
            '>>': a >> b,
        }
        if op not in ops:
            raise ValueError(f"Operator tidak dikenal: '{op}'")
        return BigInteger._from_int(ops[op])

    # Dunder methods untuk operator bitwise
    def __or__(self, other):   return self.bitwise_ops(other, '|')
    def __and__(self, other):  return self.bitwise_ops(other, '&')
    def __xor__(self, other):  return self.bitwise_ops(other, '^')
    def __lshift__(self, other): return self.bitwise_ops(other, '<<')
    def __rshift__(self, other): return self.bitwise_ops(other, '>>')


# ============================================================
# SOAL 2 - Assignment Combo Operators
# Menambahkan: +=, -=, *=, //=, %=, **=, <<=, >>=, |=, &=, ^=
# ============================================================

    # Aritmatika assignment
    def __iadd__(self, other):
        result = self.arithmetic(other, '+')
        self._rebuild(result)
        return self

    def __isub__(self, other):
        result = self.arithmetic(other, '-')
        self._rebuild(result)
        return self

    def __imul__(self, other):
        result = self.arithmetic(other, '*')
        self._rebuild(result)
        return self

    def __ifloordiv__(self, other):
        result = self.arithmetic(other, '//')
        self._rebuild(result)
        return self

    def __imod__(self, other):
        result = self.arithmetic(other, '%')
        self._rebuild(result)
        return self

    def __ipow__(self, other):
        result = self.arithmetic(other, '**')
        self._rebuild(result)
        return self

    # Bitwise assignment
    def __ilshift__(self, other):
        result = self.bitwise_ops(other, '<<')
        self._rebuild(result)
        return self

    def __irshift__(self, other):
        result = self.bitwise_ops(other, '>>')
        self._rebuild(result)
        return self

    def __ior__(self, other):
        result = self.bitwise_ops(other, '|')
        self._rebuild(result)
        return self

    def __iand__(self, other):
        result = self.bitwise_ops(other, '&')
        self._rebuild(result)
        return self

    def __ixor__(self, other):
        result = self.bitwise_ops(other, '^')
        self._rebuild(result)
        return self

    def _rebuild(self, other_bigint):
        """Rebuild linked list dari BigInteger lain (untuk in-place ops)."""
        self.head = None
        self.negative = other_bigint.negative
        # Salin node dari other_bigint
        current = other_bigint.head
        nodes = []
        while current:
            nodes.append(current.digit)
            current = current.next
        # nodes sudah dalam urutan LS -> MS, prepend terbalik agar urutan tetap
        for digit in reversed(nodes):
            self._prepend(digit)


# ============================================================
# PENGUJIAN
# ============================================================
if __name__ == "__main__":
    print("=" * 55)
    print("  SOAL 1(a) - Big Integer ADT: Singly Linked List")
    print("=" * 55)

    a = BigInteger("45839")
    b = BigInteger("12345")
    neg = BigInteger("-500")

    print(f"\n[toString()]")
    print(f"  a = {a.toString()}")
    print(f"  b = {b.toString()}")
    print(f"  neg = {neg.toString()}")

    print(f"\n[comparable()]")
    print(f"  a > b  : {a.comparable(b, '>')}")
    print(f"  a < b  : {a.comparable(b, '<')}")
    print(f"  a == b : {a.comparable(b, '==')}")
    print(f"  a != b : {a.comparable(b, '!=')}")
    print(f"  a >= b : {a.comparable(b, '>=')}")
    print(f"  a <= b : {a.comparable(b, '<=')}")

    print(f"\n[arithmetic()]")
    print(f"  a + b  = {a.arithmetic(b, '+')}")
    print(f"  a - b  = {a.arithmetic(b, '-')}")
    print(f"  a * b  = {a.arithmetic(b, '*')}")
    print(f"  a // b = {a.arithmetic(b, '//')}")
    print(f"  a % b  = {a.arithmetic(b, '%')}")
    print(f"  b ** BigInteger('2') = {b.arithmetic(BigInteger('2'), '**')}")

    print(f"\n[bitwise_ops()]")
    x = BigInteger("60")   # 0b111100
    y = BigInteger("13")   # 0b001101
    print(f"  x = {x}, y = {y}")
    print(f"  x | y  = {x.bitwise_ops(y, '|')}")
    print(f"  x & y  = {x.bitwise_ops(y, '&')}")
    print(f"  x ^ y  = {x.bitwise_ops(y, '^')}")
    print(f"  x << BigInteger('1') = {x.bitwise_ops(BigInteger('1'), '<<')}")
    print(f"  x >> BigInteger('1') = {x.bitwise_ops(BigInteger('1'), '>>') }")

    print("\n" + "=" * 55)
    print("  SOAL 2 - Assignment Combo Operators")
    print("=" * 55)

    c = BigInteger("100")
    d = BigInteger("25")
    print(f"\n  c = {c}, d = {d}")

    c += d; print(f"  c += d  -> c = {c}")
    c -= d; print(f"  c -= d  -> c = {c}")
    c *= d; print(f"  c *= d  -> c = {c}")
    c //= d; print(f"  c //= d -> c = {c}")
    c %= d; print(f"  c %= d  -> c = {c}")

    e = BigInteger("2")
    e **= BigInteger("10"); print(f"  e **= 10 -> e = {e}")

    f = BigInteger("60")
    g = BigInteger("13")
    print(f"\n  f = {f}, g = {g}")
    f <<= BigInteger("1"); print(f"  f <<= 1  -> f = {f}")
    f >>= BigInteger("1"); print(f"  f >>= 1  -> f = {f}")
    f |= g;  print(f"  f |= g   -> f = {f}")
    f &= g;  print(f"  f &= g   -> f = {f}")
    f ^= g;  print(f"  f ^= g   -> f = {f}")

    print("\n[Operator dunder (Pythonic)]")
    p = BigInteger("999")
    q = BigInteger("111")
    print(f"  p + q = {p + q}")
    print(f"  p - q = {p - q}")
    print(f"  p * q = {p * q}")
    print(f"  p > q : {p > q}")
    print(f"  p == q: {p == q}")
