import json

item = json.dumps({
                'type': 100,
                'message': 200,
                'player': 300
                }{
                'type': 100,
                'message': 200,
                'player': 300
                }).encode()

obj = json.loads(item)
print(obj)
