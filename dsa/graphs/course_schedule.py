"""
Problem:
Course Schedule

Pattern:
Graph cycle detection / Topological sort

Time Complexity:
O(N + E)

Space Complexity:
O(N + E)
"""

class Solution:
    def canFinish(self, numCourses, prerequisites):
        graph = {i: [] for i in range(numCourses)}
        indegree = [0] * numCourses

        for course, prereq in prerequisites:
            graph[prereq].append(course)
            indegree[course] += 1

        queue = [i for i in range(numCourses) if indegree[i] == 0]
        visited = 0

        while queue:
            course = queue.pop(0)
            visited += 1

            for next_course in graph[course]:
                indegree[next_course] -= 1
                if indegree[next_course] == 0:
                    queue.append(next_course)

        return visited == numCourses
