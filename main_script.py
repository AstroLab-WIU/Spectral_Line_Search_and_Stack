
ver =casalog.version()

if "CASA Version 5" in ver:
    print("Casa 5")
    execfile("c5_script.py")
elif "CASA Version 6" in ver:
    print("Casa 6")
    execfile("c6_script.py")
else:
    print("Casa Unkown")
