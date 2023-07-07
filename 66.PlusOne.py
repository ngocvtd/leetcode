class Solution(object):
    def plusOne(self, digits):
        """
        :type digits: List[int]
        :rtype: List[int]
        """
        num_str = ''.join(map(str, digits))
        num = int(num_str)
        num += 1
        rs_str = str(num)
        rs = list(map(int, rs_str))
        return rs
