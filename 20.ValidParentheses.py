class Solution(object):
    def isValid(self, s):
        """
        :type s: str
        :rtype: bool
        """
        stack = []

        for char in s:
            if char == '(' or char == '{' or char == '[':
                stack.append(char)
            elif char == ')' or char == '}' or char == ']':
                if not stack:
                    return False
                if char == ')' and stack[-1] != '(':
                    return False
                if char == '}' and stack[-1] != '{':
                    return False
                if char == ']' and stack[-1] != '[':
                    return False
                stack.pop()

        return len(stack) == 0