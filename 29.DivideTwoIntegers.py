class Solution(object):
    def divide(self, dividend, divisor):
        if dividend == 0:
            return 0
        if divisor == 0:
            return float('inf')

        is_negative = (dividend < 0) ^ (divisor < 0)
        dividend = abs(dividend)
        divisor = abs(divisor)

        result = 0
        while dividend >= divisor:
            temp_divisor = divisor
            quotient = 1

            while dividend >= (temp_divisor << 1):
                temp_divisor <<= 1
                quotient <<= 1

            dividend -= temp_divisor
            result += quotient

        if is_negative:
            result = -result

        if result < -2147483648:
            return -2147483648
        if result > 2147483647:
            return 2147483647

        return result
