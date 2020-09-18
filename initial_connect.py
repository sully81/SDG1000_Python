import pyvisa

rm = pyvisa.ResourceManager()
print("resources = ", rm.list_resources())

inst = rm.open_resource("USB0::0xF4ED::0xEE3A::SDG10GA2162699::INSTR", query_delay=0.25)
response = inst.query("*IDN?")
print(response)