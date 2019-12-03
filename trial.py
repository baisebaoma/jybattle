from scripts.player import *

p.connect("asd", "asd")

username = 'asd'
password = 'asd'
thing = "rp"
add = 100

exec(f"temp = p.player_list[p.find('{username}')].{thing}")
exec(f"p.player_list[p.find('{username}')].{thing} += 100")
print(temp)
exec(f"print(p.player_list[p.find('{username}')].{thing})")

