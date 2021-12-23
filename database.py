import sqlite3
import db_api



CREATE_TABLE_RECIPES = "CREATE TABLE IF NOT EXISTS Recipes(\
                        id           INTEGER    PRIMARY KEY AUTOINCREMENT,\
                        recipe_title	    VARCHAR(50)		NOT NULL,\
                        recipe_description	VARCHAR(500)		NOT NULL)\
                        "

CREATE_TABLE_INSTRUCTIONS = "CREATE TABLE IF NOT EXISTS Instructions(\
	recipe_id INTEGER NOT NULL,\
    instruction_position INTEGER PRIMARY KEY AUTOINCREMENT, \
    instruction VARCHAR(250) NOT NULL, \
    FOREIGN KEY (recipe_id) \
        REFERENCES Recipes(id) \
        ON DELETE CASCADE)\
    "

CREATE_TABLE_INGREDIENTS = "CREATE TABLE IF NOT EXISTS Ingredients(\
	recipe_id INTEGER NOT NULL,\
    ingredient_position INTEGER PRIMARY KEY AUTOINCREMENT, \
    unit VARCHAR(25) NOT NULL, \
    quantity REAL NOT NULL, \
    ingredient VARCHAR(50) NOT NULL, \
    FOREIGN KEY (recipe_id) REFERENCES Recipes(id) ON DELETE CASCADE)\
    "

CREATE_TABLE_TAGS = "CREATE TABLE IF NOT EXISTS Tags(\
 recipe_id INTEGER NOT NULL,\
    tag VARCHAR(25), \
    FOREIGN KEY (recipe_id) REFERENCES Recipes(id) ON DELETE CASCADE)\
    "

CREATE_TABLE_COMMENTS = "CREATE TABLE IF NOT EXISTS Comments(\
    recipe_id INTEGER NOT NULL,\
    username VARCHAR(20) NOT NULL , \
    body VARCHAR (100), \
    FOREIGN KEY (recipe_id) REFERENCES Recipes(id) ON DELETE CASCADE)\
"

def connect():
    connection =  sqlite3.connect('data.db')
    connection.execute("PRAGMA foreign_keys = ON;")
    return connection

def create_tables():
    connection = connect()
    with connection:
        connection.execute(CREATE_TABLE_RECIPES)
        connection.execute(CREATE_TABLE_INSTRUCTIONS)
        connection.execute(CREATE_TABLE_INGREDIENTS)
        connection.execute(CREATE_TABLE_COMMENTS)
        connection.execute(CREATE_TABLE_TAGS)

        connection.commit()
        # connection.close()

# def print_tables(connection):
#     with connection:
#         current = connection.cursor()
#         current.execute("SELECT * FROM Recipes INNER JOIN Instructions ON Recipes.id = Instructions.recipe_id\
#                         INNER JOIN Ingredients ON Recipes.id = Ingredients.recipe_id")
#         return current.fetchall()

def get_recipes_count():
    connection = connect()
    with connection:
        cur = connection.cursor()
        cur.execute("SELECT COUNT(*) FROM Recipes")
        result = cur.fetchall()[0][0]
        return result

def search_title(title):
    connection = connect()
    id_list = db_api.RecipeRepository.search_by_title(connection, title)
    result = []
    if id_list:
        for recipe_id in id_list:
            result.append( db_api.RecipeRepository.search(connection, recipe_id))
    return result

def recipeToString(recipe_dict):
    recipe = recipe_dict["recipe"]
    ingredients_list = recipe_dict["ingredients"]
    instruction_list = recipe_dict["instructions"]
    result = f'Рецепт з назвою - {recipe[1]},\nОпис:\n {recipe[2]}\n\
        Інгрідієнти:\n {[[value[4], value[3], value[2]] for value in ingredients_list]}\n\
        Послідовність дій : {[value[2] for value in instruction_list]}'
    return result

def search_tags(tag):
    connection = connect()
    result = []
    id_list = []
    
    id_list = id_list + db_api.TagsRepository.search(connection, tag)
    print(id_list)
    # print(db_api.TagsRepository.search(connection, tag))
    if id_list:
        for recipe_id in id_list:
            result.append(db_api.RecipeRepository.search(connection, recipe_id))
    
    return result

def print_tables():
    connection = connect()
    with connection:
        current = connection.cursor()
        current.execute("SELECT * FROM Recipes")
        return current.fetchall()

# class Recipe():
#     def __init__(self):
#         self.id = 10
#         self.title = 'sadas'
#         self.description = 'abobas'


# class Instructions():
#     def __init__(self):
#         self.recipe_id = 10
#         self.position = 2
#         self.instruction = 'put in it'

# class Ingredients():
#     def __init__(self):
#         self.recipe_id = 10
#         self.position = 1
#         self.unit = 'mg'
#         self.quantity = 5
#         self.ingredient = 'banana'
        

# print(get_recipes_count())
# recipe = Recipe()
# # instruction = Instructions()
# instruction1 = Instructions()
# ingredient = Ingredients()

# connection = connect()
# # with connection:
# #     cur = connection.cursor()
# #     cur.execute("SELECT * FROM Instructions")
# #     print(cur.fetchall())
# #     connection.commit()

create_tables()

# # db_api.RecipeRepository.insert(connection, recipe);
# # db_api.InstructionRepository.insert(connection, instruction)
# # db_api.InstructionRepository.insert(connection, instruction1)
# # db_api.IngredientRepository.insert(connection, ingredient)
# # print(print_tables(connection))

# # with connection:
# #     cur = connection.cursor()
# #     cur.execute("SELECT * FROM Recipes WHERE id=?", (10,))
# #     print(cur.fetchone())
# #     connection.commit()

# # print(print_tables(connection))
# # db_api.RecipeRepository.delete(connection, recipe.id)
# print(db_api.RecipeRepository.search(connection, 10))
# # print(print_tables(connection))

# # print(print_tables(connection))
# # print(print_tables(connection))
# # db_api.RecipeRepository.delete(connection, recipe.id)
# # print_tables(connection)
# # print(db_api.InstructionRepository.search(connection, instruction.recipe_id))

# # with connection:
# #     cur = connection.cursor()
# #     cur.execute("DROP TABLE Instructions")
# #     cur.execute("DROP TABLE Recipes")
# #     cur.execute("DROP TABLE Ingredients")
# #     connection.commit()
