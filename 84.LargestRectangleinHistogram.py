class Solution(object):
    def largestRectangleArea(self, heights):
        """
        :type heights: List[int]
        :rtype: int
        """
        stack = []
        max_area = 0
        n = len(heights)

        for i in range(n):
            while stack and heights[i] < heights[stack[-1]]:
                height = heights[stack.pop()]
                width = i if not stack else i - stack[-1] - 1
                area = height * width
                max_area = max(max_area, area)
            stack.append(i)

        while stack:
            height = heights[stack.pop()]
            width = n if not stack else n - stack[-1] - 1
            area = height * width
            max_area = max(max_area, area)
        return max_area
