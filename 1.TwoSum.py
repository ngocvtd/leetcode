class Solution(object):
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        index = {}

        for i, num in enumerate(nums):
            n = target - num
            if n not in index:
                index[num] = i
            else:
                return [index[n], i]    