class ListNode(object):
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution(object):

    def addTwoNumbers(self, l1, l2):
        """
        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        >>> s = Solution()
        >>> l1 = ListNode(1, ListNode(2, ListNode(3)))
        >>> l2 = ListNode(5, ListNode(3, ListNode(8)))
        >>> s.addTwoNumbers(l1, l2)
        """
        num1 = self.getNum(l1)
        num2 = self.getNum(l2)
        rnum = num1 + num2
        return self.getReturnNum(rnum)

    def getNum(self, l):
        """
        Searches through the linked list <l> and
        returns the number it represents as an integer
        """
        num = ''
        num += str(l.val)
        curr = l.next
        while curr is not None:
            prev = num
            num = str(curr.val) + prev
            curr = curr.next
        return int(num)

    def getReturnNum(self, rnum):
        """
        Creates a linked list containing the return
        number
        """
        rnum = str(rnum)
        rl = ListNode(rnum[-1])
        i = -2
        curr = rl
        while i >= -len(rnum):
            curr.next = ListNode(rnum[i])
            curr = curr.next
        return rl
