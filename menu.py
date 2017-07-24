import runpy

print("\t\tMAIN MENU")
print("1. Sign Up ")
print("2. Sign In ")
print("3. Admin Sign In")
print("4. quit")
choice = int(input())
if choice == 1:
    runpy.run_path("Customer.py")
elif choice == 2:
    runpy.run_path("CustomerSignIn.py")
elif choice == 3:
    runpy.run_path("AdminSignIn.py")
elif choice == 4:
    runpy.run_path("Quit")
else:
    print("Wrong choice!")
