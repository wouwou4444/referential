from referential.category import Category

class TestCategory:
    
    def test_init(self):
        assert Category("Space Management").category_name == "spaceManagement"
        assert Category("Space Management").category_full_name == "spaceManagement"
       
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
        assert cat1.children[0].category_name == "spaceManagement"
        
        
                
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
        assert cat1.search_by_name("incidents__userManagement") == cat1.children[1]
        assert cat1.search_by_name("incidents__spaceManagement") == cat1.children[0]
        

    def test_search_by_name_none(self):
        cat1 = Category("incidents")
        cat1.add("space management")
        cat1.add("user management")       
        assert cat1.search_by_name("not a category") == None
        
        
    def test_add_already_exist(self):
        cat1 = Category("incidents")
        cat1.add("incidents")
        assert cat1.add("incidents") is cat1.children[0]
        
    def test_add_already_exist_2(self):
        cat1 = Category("incidents")
        child1 = cat1.add("test",parent_full_name="incidents")
        assert child1
        assert cat1.add("test",parent_full_name="incidents") == child1  

    def test_add_already_exist_3(self):
        cat1 = Category("incidents")
        cat1.add("toto",parent_full_name="incidents")
        cat1.add("test",parent_full_name="incidents")
        child = cat1.add("tata",parent_full_name="incidents__test")
        assert child
        assert cat1.add("tata",parent_full_name="incidents__test") == child 
        
    def test_add_already_exist_4(self):
        cat1 = Category("incidents")
        cat1.add("toto",parent_full_name="incidents")
        cat1.add("test",parent_full_name="incidents")
        child = cat1.add("tata titi",parent_full_name="incidents__test")
        assert child
        assert cat1.add("tata titi",parent_full_name="incidents__test") == child   
        
    def test_add_already_exist_5(self):
        cat1 = Category("incidents")
        cat1.add("toto",parent_full_name="incidents")
        cat1.add("test",parent_full_name="incidents")
        assert cat1.add("tata titi",parent_full_name="incidents__test")
        assert cat1.add("tata titi",parent_full_name="incidents__toto")     
                
    def test_add_parent_not_found(self):
        cat1 = Category("incidents")       
        assert cat1.add("test","test","00000") is None
        
    def test_add_by_name(self):
        cat1 = Category("incidents") 
        cat1.add("toto", "toto")
        cat1.add("test","test")
        print(cat1)
        print(cat1.children[0])
        print(cat1.children[1])
        new_cat = cat1.add("child2_test","", parent_full_name = "incidents__test")
        assert new_cat is not None
        assert new_cat.parent_id == cat1.children[1].category_id
        
    def test_add_full_name_1(self):
        cat1 = Category("root")
        assert cat1.add("root__incidents").category_name == "incidents"
        
        assert cat1.add("root__requests").category_name == "requests"
        
    def test_add_full_name_2(self):
        cat1 = Category("root")
        assert cat1.add("root__incidents").category_name == "incidents"
        
        assert cat1.add("root__incidents__space").category_name == "space"