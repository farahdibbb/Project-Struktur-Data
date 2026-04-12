# ============================================================
# SOAL 1(b) - Big Integer ADT menggunakan Python List
# Setiap digit disimpan sebagai elemen list, urutan dari
# digit paling tidak signifikan (index 0) ke paling signifikan.
# ============================================================

class BigIntegerList:
    """
    Big Integer ADT menggunakan Python list.
    digits[0] = digit paling tidak signifikan (least significant).
    Contoh: 45839 -> digits = [9, 3, 8, 5, 4]
    """

    def __init__(self, initValue="0"):
        self.digits = []
        self.negative = False
        self._build_from_string(str(initValue))

    # ----------------------------------------------------------
    # Helper: membangun list dari string
    # ----------------------------------------------------------
    def _build_from_string(self, s):
        s = s.strip()
        if not s:
            s = "0"

        if s[0] == '-':
            self.negative = True
            s = s[1:]
        elif s[0] == '+':
            s = s[1:]

        s = s.lstrip('0') or '0'

        if not s.isdigit():
            raise ValueError(f"Nilai tidak valid: '{s}'")

        # Simpan digit dari LS ke MS (balik string)
        self.digits = [int(ch) for ch in reversed(s)]

    # ----------------------------------------------------------
    # Helper: konversi ke integer Python
    # ----------------------------------------------------------
    def _to_int(self):
        result = 0
        for i, d in enumerate(self.digits):
            result += d * (10 ** i)
        return -result if self.negative else result

    @classmethod
    def _from_int(cls, value):
        return cls(str(value))

    # ----------------------------------------------------------
    # toString()
    # ----------------------------------------------------------
    def toString(self):
        # digits[0] = LS, digits[-1] = MS -> balik untuk tampilan
        result = ''.join(str(d) for d in reversed(self.digits))
        if self.negative and result != '0':
            result = '-' + result
        return result

    def __repr__(self):
        return f"BigIntegerList('{self.toString()}')"

    def __str__(self):
        return self.toString()

    # ----------------------------------------------------------
    # comparable()
    # ----------------------------------------------------------
    def comparable(self, other, operator):
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

    def __lt__(self, other):  return self.comparable(other, '<')
    def __le__(self, other):  return self.comparable(other, '<=')
    def __gt__(self, other):  return self.comparable(other, '>')
    def __ge__(self, other):  return self.comparable(other, '>=')
    def __eq__(self, other):  return self.comparable(other, '==')
    def __ne__(self, other):  return self.comparable(other, '!=')

    # ----------------------------------------------------------
    # arithmetic()
    # ----------------------------------------------------------
    def arithmetic(self, rhsInt, op):
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
        return BigIntegerList._from_int(ops[op])

    def __add__(self, other):      return self.arithmetic(other, '+')
    def __sub__(self, other):      return self.arithmetic(other, '-')
    def __mul__(self, other):      return self.arithmetic(other, '*')
    def __floordiv__(self, other): return self.arithmetic(other, '//')
    def __mod__(self, other):      return self.arithmetic(other, '%')
    def __pow__(self, other):      return self.arithmetic(other, '**')

    # ----------------------------------------------------------
    # bitwise_ops()
    # ----------------------------------------------------------
    def bitwise_ops(self, rhsInt, op):
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
        return BigIntegerList._from_int(ops[op])

    def __or__(self, other):    return self.bitwise_ops(other, '|')
    def __and__(self, other):   return self.bitwise_ops(other, '&')
    def __xor__(self, other):   return self.bitwise_ops(other, '^')
    def __lshift__(self, other):return self.bitwise_ops(other, '<<')
    def __rshift__(self, other):return self.bitwise_ops(other, '>>')

    # ----------------------------------------------------------
    # SOAL 2 - Assignment Combo Operators
    # ----------------------------------------------------------
    def _rebuild(self, other):
        self.digits = list(other.digits)
        self.negative = other.negative

    def __iadd__(self, other):
        self._rebuild(self.arithmetic(other, '+')); return self
    def __isub__(self, other):
        self._rebuild(self.arithmetic(other, '-')); return self
    def __imul__(self, other):
        self._rebuild(self.arithmetic(other, '*')); return self
    def __ifloordiv__(self, other):
        self._rebuild(self.arithmetic(other, '//')); return self
    def __imod__(self, other):
        self._rebuild(self.arithmetic(other, '%')); return self
    def __ipow__(self, other):
        self._rebuild(self.arithmetic(other, '**')); return self
    def __ilshift__(self, other):
        self._rebuild(self.bitwise_ops(other, '<<')); return self
    def __irshift__(self, other):
        self._rebuild(self.bitwise_ops(other, '>>')); return self
    def __ior__(self, other):
        self._rebuild(self.bitwise_ops(other, '|')); return self
    def __iand__(self, other):
        self._rebuild(self.bitwise_ops(other, '&')); return self
    def __ixor__(self, other):
        self._rebuild(self.bitwise_ops(other, '^')); return self


# ============================================================
# PENGUJIAN
# ============================================================
if __name__ == "__main__":
    print("=" * 55)
    print("  SOAL 1(b) - Big Integer ADT: Python List")
    print("=" * 55)

    a = BigIntegerList("45839")
    b = BigIntegerList("12345")

    print(f"\n[toString()]")
    print(f"  a.digits (LS->MS) = {a.digits}")
    print(f"  a = {a.toString()}")
    print(f"  b = {b.toString()}")

    print(f"\n[comparable()]")
    print(f"  a > b  : {a.comparable(b, '>')}")
    print(f"  a == b : {a.comparable(b, '==')}")

    print(f"\n[arithmetic()]")
    print(f"  a + b  = {a.arithmetic(b, '+')}")
    print(f"  a - b  = {a.arithmetic(b, '-')}")
    print(f"  a * b  = {a.arithmetic(b, '*')}")
    print(f"  a // b = {a.arithmetic(b, '//')}")
    print(f"  a % b  = {a.arithmetic(b, '%')}")

    print(f"\n[bitwise_ops()]")
    x = BigIntegerList("60")
    y = BigIntegerList("13")
    print(f"  x | y  = {x.bitwise_ops(y, '|')}")
    print(f"  x & y  = {x.bitwise_ops(y, '&')}")
    print(f"  x ^ y  = {x.bitwise_ops(y, '^')}")
    print(f"  x << 1 = {x.bitwise_ops(BigIntegerList('1'), '<<')}")
    print(f"  x >> 1 = {x.bitwise_ops(BigIntegerList('1'), '>>')}")

    print(f"\n[Assignment Combo Operators - Soal 2]")
    c = BigIntegerList("100")
    d = BigIntegerList("25")
    c += d; print(f"  c += d   -> c = {c}")
    c -= d; print(f"  c -= d   -> c = {c}")
    c *= d; print(f"  c *= d   -> c = {c}")
    c //= d; print(f"  c //= d  -> c = {c}")

    e = BigIntegerList("2")
    e **= BigIntegerList("10"); print(f"  e **= 10 -> e = {e}")

    f = BigIntegerList("60")
    g = BigIntegerList("13")
    f <<= BigIntegerList("1"); print(f"  f <<= 1  -> f = {f}")
    f >>= BigIntegerList("1"); print(f"  f >>= 1  -> f = {f}")
    f |= g;  print(f"  f |= g   -> f = {f}")
    f &= g;  print(f"  f &= g   -> f = {f}")
    f ^= g;  print(f"  f ^= g   -> f = {f}")
