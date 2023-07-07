class Solution(object):
    def subtractProductAndSum(self, n):
        """
        :type n: int
        :rtype: int
        """
        product = 1
        sum_of_digits = 0

        while n > 0:
            digit = n % 10
            product *= digit
            sum_of_digits += digit
            n //= 10

        return product - sum_of_digits
