class Solution(object):
    def maximum69Number (self, num):
        """
        :type num: int
        :rtype: int
        """
        num_str = str(num)
        for i in range(len(num_str)):
            if num_str[i] == '6':
                num_str = num_str[:i] + '9' + num_str[i+1:]
                break
        return int(num_str)
