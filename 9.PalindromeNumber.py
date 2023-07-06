class Solution(object):
    def isPalindrome(self, x):
        """
        :type x: int
        :rtype: bool
        """
        # đổi số thành chuỗi
        num_str = str(x)

        # đảo ngược chuỗi 
        reverse = num_str[::-1]

        # kiểm tra
        if reverse == num_str :
            return True
        return False
