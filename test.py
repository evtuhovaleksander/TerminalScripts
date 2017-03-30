from sql import *
r=Resource_ORM()
r.resource='123456789012345678901234567890123456789012345'
r.save()
print(r.id)