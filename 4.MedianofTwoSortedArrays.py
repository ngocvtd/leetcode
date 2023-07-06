class Solution(object):
    def findMedianSortedArrays(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: float
        """
        merged_arr = nums1 + nums2

        n = len(merged_arr)
        for i in range(n-1):
            for j in range(n-1-i):
                if merged_arr[j] > merged_arr[j + 1]:
                    merged_arr[j], merged_arr[j + 1] = merged_arr[j + 1], merged_arr[j]

        if n % 2 != 0:
            return merged_arr[(n-1)//2]
        else:
            return (merged_arr[n//2] + merged_arr[(n//2)-1]) / 2.0
