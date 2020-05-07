import hashlib
import uuid

from datetime import datetime

def log(message = "", level = 0):
    def switch_level(level):
        switcher = {
            0: "INFO",
            1: "WARNING",
            2: "ERROR",
            3: "CRITICAL"
        }
        return switcher.get(level, "UNKN")
    print(f"{datetime.now()}:{switch_level(level)}:{message}")
    
class Category:
    
    def __init__(self, name = None, description = "", parent_id = None, parent_full_name = None ):
        """
        Initiate a category node whith no children
        name is the node name
        description is a string to describe the category usage or purpose for the user
        parent_id is the category_id of the parent node
            if parent_id is category_id the node is the Root Node of the referential
            depth is 0 by default for the root node
        """
        if not Category.check_valid_name(name):
           raise Exception("mandatory name parameter is missing or can't be used")
        else:
            name = Category.format_name(name)
            self.category_id = str(uuid.uuid4())
            self.category_name = name;
            
            self.description = description
            self.children = []
            self.digest = (hashlib.md5(name.encode())).hexdigest()
            if parent_id is None:
                log(f"Creating root node '{self.category_name}','{self.category_id}'")
                self.depth = 0
                self.parent_id = self.category_id
                self.category_full_name = name;
                
            elif parent_id and parent_full_name:
                log(f"Creating child node '{self.category_name}','{self.category_id}' with parent '{parent_id}'")
                self.depth = -1
                self.parent_id = parent_id
                self.category_full_name = f"{parent_full_name}__{name}";
                ### Search for parent parent_id
                ### Add category_id to parent.children
                ### Update depth : parent.depth + 1
            else:
                raise Exception("both parameters are required when creating a child node")
                
    def check_valid_name(name = None):
        if not name:
            return False
        else:
            try:
                name=str(name)
            except Exception:
                log(f"{name} can't be used as a name")
                return False
            if "__" in name:
                log(f"can't be used as name: {name}", 2)
                return False
        return True
    
    def format_name(name = None):
        return  "".join([item.capitalize() if item != name.split()[0] else item.lower() for item in name.split() ])           

    def search_by_name(self, full_name = None):
        """
        return the object Category whose name matches or return None
        name : a string to match in the given category tree
        """
        if self.category_full_name == full_name:
            return self
        elif len(self.children) == 0:
            return None
        else:
            for child in self.children:
                node = child.search_by_name(full_name)
                if node:
                    return node
            return None
    
    def search(self, category_id = None):
        """
        return the object Category by category_id else return None
        category_id : uuid to look for in the category tree
        """
        if self.category_id == category_id:
            return self
        elif len(self.children) == 0:
            return None
        else:
            for child in self.children:
                node = child.search(category_id)
                if node:
                    return node
        return None
    
    def export(self, depth = -1, format = "csv"):
        """
        Export the tree in csv format using depth to limit the export from the given node
        depth : number how level to display from the given node
            -1 indicates to display everything until the end
            0 displays only the current node
        """
        return [{'category_id': cat.category_id, 
                 'category_name':cat.category_name, 
                 'description': cat.description, 
                 'depth': cat.depth, 
                 'parent_id': cat.parent_id,
                 'digest': cat.digest
                }  for cat in self]

    
    def add(self, name = None, description = "", parent_id = None, parent_full_name = None):
        """
        Create a new Category object and add it to the parent with parent_id uuid
        if no parent is specified, the new object is added to the current object children
        if parent can not be found or another node exists with the same name
            None is return
        name string name of the category
        parent_id id of the node to attach this new category"""
        
        ### Need to search if the child already exists in the referential
        ####
        ####   TO DO
        ####
        
        if (parent_id is None) and (parent_full_name is None)  and (self.search_by_name(f"{self.category_full_name}__{name}") is not None):
            log(f"Node with same name '{name}' already exist in {self.category_full_name}", 1)
            return None
        
        if parent_id is None and parent_full_name is None:
            new_category = Category(name = name, description = description, parent_id = self.category_id, parent_full_name = self.category_full_name)
            new_category.depth = self.depth + 1
            self.children.append(new_category)
            log(f"Added node '{name}, {new_category.category_full_name}', '{new_category.category_id}'")
            return new_category
        elif parent_id is not None:
            parent = self.search(parent_id)
            if parent is None:
                log(f"Parent Node with id '{parent_id}' not found", 1)
                return None
                
            else:
                
                return parent.add(name, description, None)
            
        elif parent_full_name is not None:
            parent = self.search_by_name(parent_full_name)
            if parent is None:
                log(f"Parent Node with name '{parent_full_name}' not found", 1)
                return None
                
            else:
                
                return parent.add(name, description, None)            
    
    def __iter__(self):
        """
        iterator which looops through the children categories of the node
        """
        yield self
        if self.children is not None:
            log("inside __iter__")
            for category in self.children:
                log("looping child")
                for cat in category.__iter__():
                    yield cat
            
    def __repr__(self):
        return f"Category: cid:{self.category_id}, full_name:{self.category_full_name}, name:{self.category_name}, hash:{self.digest}, depth:{self.depth}, parent_id:{self.parent_id}"