z_amount = int(input("Enter your total applicable amount = "))
z_deduction = float(2.5)
z_bank = 50000
if z_amount >=z_bank:
    print ("ZAKAT APPLICABLE")
if z_amount <=z_bank:
    print ("ZAKAT NOT APPLICABLE")
else:    
    zakat = (z_amount*z_deduction)/100
	print (zakat)