from referential.category import Category

class TestCategory:
    
    def test_init(self):
        assert Category("Space Management").category_name == "Space Management"
       
    def test_iter(self):
        cat1 = Category("incidents")
        cat1.add("space management")
        cat1.add("user management")
        cat1.add("password", "", cat1.children[1].category_id)
        assert len([cat for cat in cat1]) == 4
        
    def test_export(self):
        cat1 = Category("incidents")
        cat1.add("space management")
        cat1.add("user management")
        cat1.add("password", "", cat1.children[1].category_id)
        export = cat1.export()
        assert len(export) == 4
        assert isinstance(export, list)
        assert isinstance(export[0], dict)
        
    def test_add_root(self):
        cat1 = Category("incidents")
        assert cat1.add("space management") is not None
        assert cat1.children[0].category_name == "space management"
        
        
                
    def test_depth(self):
        cat1 = Category("incidents")
        cat1.add("space management")
        assert cat1.depth == 0
        assert cat1.children[0].depth == 1
        
    def test_add_non_root(self):
        cat1 = Category("incidents")
        cat1.add("space management")
        cat1.add("user management")
        cat1.add("password", "", cat1.children[1].category_id)
        assert cat1.children[1].children[0].category_name == "password"
        
    def test_search(self):
        cat1 = Category("incidents")
        cat1.add("space management")
        cat1.add("user management")
        assert cat1.search(cat1.children[1].category_id) == cat1.children[1]
        
    def test_search_none(self):
        cat1 = Category("incidents")
        cat1.add("space management")
        cat1.add("user management")
        assert cat1.search("c69e9c1b-a9ee-48f5-8d76-b90dce1a74a2") is None
        
    def test_search_by_name(self):
        cat1 = Category("incidents")
        cat1.add("space management")
        cat1.add("user management")
        assert cat1.search_by_name("user management") == cat1.children[1]
        assert cat1.search_by_name("space management") == cat1.children[0]
        

    def test_search_by_name_none(self):
        cat1 = Category("incidents")
        cat1.add("space management")
        cat1.add("user management")       
        assert cat1.search_by_name("not a category") == None
        
        
    def test_add_already_exist(self):
        cat1 = Category("incidents")
        cat1.add("incidents")
        assert cat1.add("incidents") is None
        
    def test_add_parent_not_found(self):
        cat1 = Category("incidents")
        
        assert cat1.add("test","test","00000") is None
        