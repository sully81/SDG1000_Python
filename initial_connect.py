import visa

# rm = visa.ResourceManager()
# print("resources = ", rm.list_resources())

resources = visa.ResourceManager()
probe = resources.open_resource("USB0::0xF4ED::0xEE3A::SDG10GA2162699::INSTR", query_delay=0.25)
response = probe.query("*IDN?")
print(response)