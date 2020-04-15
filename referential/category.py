import hashlib
import uuid

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
                self.depth = 0
                self.parent_id = self.category_id
                
            else:
                self.depth = -1
                self.parent_id = parent_id
                ### Search for parent parent_id
                ### Add category_id to parent.children
                ### Update depth : parent.depth + 1
                
    
    def search_by_name(self, name = None):
        """
        return the object Category whom name matches or return None
        name : a string to match in the given category tree
        """
        pass
    
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
        print(";".join([str(self.category_id),self.category_name, self.description,str(self.digest), str(self.depth), str(self.parent_id)]))
        for child in self.children:
            child.export(depth = depth - 1, format = format)
        pass
    
    def add(self, name = None, description = "", parent_id = None):
        """
        Create a new Category object and add it to the parent with parent_id uuid
        if no parent is specified, the new object is added to the current object children
        name string name of the category
        parent_id id of the node to attach this new category"""
        
        ### Need to search if the child already exists in the referential
        if parent_id is None:
            new_category = Category(name = name, description = description, parent_id = self.category_id)
            new_category.depth = self.depth + 1
            self.children.append(new_category)
        else:
            parent = self.search(parent_id)
            if parent is None:
                raise Exception("Node not found")
            else:
                parent.add(name, description, None)
    
    def __iter__(self):
        """
        iterator which looops through the children categories of the node
        """
        yield self
        for category in self.children:
            yield category
            
    def __repr__(self):
        return f"<User: cid:{self.category_id}, name:{self.category_name}, hash:{self.digest}, depth:{self.depth}>"