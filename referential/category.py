import hashlib
import uuid

from datetime import datetime

def log(message = "", level = 0):
    def switch_level(level):
        switcher = {
            0: "INFO",
            1: "WARN",
            2: "ERRO",
            3: "CRIT"
        }
        return switcher.get(level, "UNKN")
    print(f"{datetime.now()}:{switch_level(level)}:{message}")
    
class Category:
    
    def __init__(self, name = None, description = "", parent_id = None):
        """
        Initiate a category node whith no children
        name is the node name
        description is a string to describe the category usage or purpose for the user
        parent_id is the category_id of the parent node
            if parent_id is category_id the node is the Root Node of the referential
            depth is 0 by default for the root node
        """
        if name is None:
            return None
        else:
            self.category_id = str(uuid.uuid4())
            self.category_name = name;
            self.description = description
            self.children = []
            self.digest = (hashlib.md5(name.encode())).hexdigest()
            if parent_id is None:
                log(f"Creating root node '{self.category_name}','{self.category_id}'")
                self.depth = 0
                self.parent_id = self.category_id
                
            else:
                log(f"Creating child node '{self.category_name}','{self.category_id}' with parent '{parent_id}'")
                self.depth = -1
                self.parent_id = parent_id
                ### Search for parent parent_id
                ### Add category_id to parent.children
                ### Update depth : parent.depth + 1
                
    
    def search_by_name(self, name = None):
        """
        return the object Category whose name matches or return None
        name : a string to match in the given category tree
        """
        if self.category_name == name:
            return self
        elif len(self.children) == 0:
            return None
        else:
            for child in self.children:
                node = child.search_by_name(name)
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

    
    def add(self, name = None, description = "", parent_id = None, parent_name = None):
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
        
        if self.search_by_name(name) is not None:
            log(f"Node with same name '{name}' already exist", 1)
            return None
        if parent_id is None and parent_name is None:
            new_category = Category(name = name, description = description, parent_id = self.category_id)
            new_category.depth = self.depth + 1
            self.children.append(new_category)
            log(f"Added node '{name}', '{new_category.category_id}'")
            return new_category
        elif parent_id is not None:
            parent = self.search(parent_id)
            if parent is None:
                log(f"Parent Node with id '{parent_id}' not found", 1)
                return None
                
            else:
                
                return parent.add(name, description, None)
        elif parent_name is not None:
            parent = self.search_by_name(parent_name)
            if parent is None:
                log(f"Parent Node with name '{parent_name}' not found", 1)
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
        return f"Category: cid:{self.category_id}, name:{self.category_name}, hash:{self.digest}, depth:{self.depth}"