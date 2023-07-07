class Solution(object):
    
    def selfDividingNumbers(self, left, right):
        """
        :type left: int
        :type right: int
        :rtype: List[int]
        """
        def isSelfDividing(n):
            num = n
            while n > 0:
                digit = n % 10
                if digit == 0 or num % digit != 0:
                    return False
                n //= 10
            return True

        result = []
        for i in range(left, right + 1):
            if isSelfDividing(i):
                result.append(i)
        return result
