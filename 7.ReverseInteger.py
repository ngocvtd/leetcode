class Solution(object):
    def reverse(self, x):
        """
        :type x: int
        :rtype: int
        """
        abs_str = str(abs(x))
        
        num = abs_str[::-1].lstrip('0')

        if x < 0:
            num = '-'+num
        try:
            num = int(num)
        except ValueError:
            return 0

        if num > 2**31 - 1 or num < -2**31 -1:
            return 0
        return num
