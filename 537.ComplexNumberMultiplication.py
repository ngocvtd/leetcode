class Solution(object):
    def complexNumberMultiply(self, num1, num2):
        """
        :type num1: str
        :type num2: str
        :rtype: str
        """
        num1_real, num1_imaginary = map(int, num1[:-1].split('+'))

        num2_real, num2_imaginary = map(int, num2[:-1].split('+'))

        num_real = (num1_real * num2_real) - (num1_imaginary * num2_imaginary)
        num_imaginary = (num1_real * num2_imaginary) + (num2_real * num1_imaginary) 

        rs = "{}+{}i".format(num_real, num_imaginary)

        return rs
