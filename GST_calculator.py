#-------------------------------------------------------------------------------
# Name:        module2
# Purpose:
#
# Author:      prana
#
# Created:     24-11-2023
# Copyright:   (c) prana 2023
# Licence:     <your licence>
#-------------------------------------------------------------------------------

Production = int(input("Cost of Production: "))
CGST = int(Production * 9/100)
SGST = int(Production * 9/100)
Total_cost = int(Production + CGST + SGST)
print("The total cost is:",Total_cost)