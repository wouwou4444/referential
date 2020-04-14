import hashlib
import uuid

class Category:
    
    def __init__(self, name = None, description = None, parent_id = None):
        if name is None:
            return None
        else:
            self.category_id = uuid.uuid4()
            self.category_name = name;
            self.category_description = description
            self.category_parent_id = parent_id
            self.children_ids = None
            self.digest = (hashlib.md5(name.encode())).hexdigest()
            if parent_id is None:
                self.depth = 0
                self.parent_id = self.category_id
                
            else:
                self.depth = -1
                self.parent_id = parent_id
                ### Search for parent parent_id
                ### Add category_id to parent.children_ids
                ### Update depth : parent.depth + 1
    
    def exist(self, hash = 0):
        pass
    
    def children(self):
        pass
    
    def append_child(self, child_id):
        pass
    
    def __repr__(self):
        return f"<User: cid:{self.category_id}, name:{self.category_name}, hash:{self.digest}, depth:{self.depth}>"