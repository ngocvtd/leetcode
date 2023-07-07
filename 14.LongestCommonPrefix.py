class Solution(object):
    def longestCommonPrefix(self, strs):
        """
        :type strs: List[str]
        :rtype: str
        """
        if not strs:  # If the input list is empty
            return ""

        min_len = min(len(s) for s in strs)

        for i in range(min_len):
            if not all(s[i] == strs[0][i] for s in strs[1:]):
                return strs[0][:i]

        return strs[0][:min_len]
