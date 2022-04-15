# # Definition for singly-linked list.
# # from typing import List, Optional


# # from xml.dom.minicompat import NodeList


# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

#     def __repr__(self) -> str:
#         return f"val {self.val}  , next {self.next}"

# class Solution:
#     def addTwoNumbers(self, l1, l2):
        
#         dummy = ListNode(0)
#         carry = 0
        
#         p =l1
#         q =l2
#         curr = dummy

#         while (p or q ) :
#             print(f"{p} , {q}")
#             if p.val == None :
#                 p.val = 0
#             if q.val == None :
#                 q.val = 0
                
#             sum = p.val + q.val + carry
#             print(sum,"sum")
#             carry = int(sum /10)
#             print(carry,"carry")
#             # set dummy next 
#             curr.next = ListNode(sum % 10)
#             print(curr.next,f"set dummy next to {sum%10}")

#             # update dummy
#             curr = curr.next
            
#             if p.next != None :
#                 p = p.next
#             if q.next != None :
#                 q = q.next
        
#         if carry > 0 :
#             print("enter carry 1")
#             curr.next = ListNode(carry)
            
#         return dummy.next
        


      
# # [2,4,3]
# # [5,6,4]
# # [0]
# # [0]
# # [9,9,9,9,9,9,9]
# # [9,9,9,9]



# def toNodeList(listz):
#     head = None
#     curr = None
#     print(f"Input {listz}")
#     for x in listz :
#         curr = ListNode(x,curr)
#         print(f"Create Node {curr}")

#         # curr.next = curr
#     #     if head == None :
#     #         head = curr
#     # return head
#     return curr


# l1 = toNodeList([2,3,4])
# print(l1.next)
# # l2 = toNodeList([5,6,4])  
# # print(l1)
# # print(l2)

# # Solution().addTwoNumbers(l1,l2)
        
