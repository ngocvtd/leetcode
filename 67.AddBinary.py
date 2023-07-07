class Solution(object):
    def addBinary(self, a, b):
        """
        :type a: str
        :type b: str
        :rtype: str
        """
        result = ""
        i, j = len(a) - 1, len(b) - 1
        carry = 0

        while i >= 0 or j >= 0:
            bit_a = int(a[i]) if i >= 0 else 0
            bit_b = int(b[j]) if j >= 0 else 0

            summation = bit_a + bit_b + carry
            result = str(summation % 2) + result
            carry = summation // 2

            i -= 1
            j -= 1

        if carry > 0:
            result = str(carry) + result

        return result
