from my_lib import Message

m = Message("type", "contenu")
b = m.to_binary()
new_m = Message.from_binary(b)
print(m)
print(new_m)