from abc import ABC, abstractmethod


class TableRepository(ABC):
    @abstractmethod
    def delete():
        pass

    @abstractmethod
    def insert():
        pass    

class RecipeRepository(TableRepository) :
    @staticmethod
    def search(connection, recipe_id):
        cur = connection.cursor()
        answer = {'recipe' : '',
                  'ingredients' : [],
                  'instructions' : [],             }
        #find recipe
        sql = 'SELECT * FROM Recipes WHERE id=?'
        cur.execute(sql, (recipe_id,))
        answer['recipe'] = cur.fetchone()
        #find ingredients
        answer['ingredients'] = IngredientRepository.search(connection, recipe_id)
        #find instructions
        answer['instructions'] = InstructionRepository.search(connection, recipe_id)
        return answer

    @staticmethod
    def search_by_title(connection, title):
        cur = connection.cursor()
        sql = f'SELECT id FROM Recipes WHERE recipe_title LIKE "%{title}%"'
        cur.execute(sql)
        return [int(value[0]) for value in cur.fetchall()]

    @staticmethod
    def delete(connection, recipe_id):
        sql = 'DELETE FROM Recipes WHERE id=?'
        cur = connection.cursor()
        cur.execute(sql, (recipe_id,))
        connection.commit() 

    @staticmethod
    def update(connection, entity):
        RecipeRepository.delete(connection, entity.id)
        RecipeRepository.insert(connection, entity)

    @staticmethod
    def insert(connection, entity):
        sql = 'INSERT INTO Recipes (id , recipe_title, recipe_description) VALUES(?,?,?)'
        cur = connection.cursor()
        cur.execute(sql, (entity.id, entity.title, entity.description, ))
        connection.commit()

class InstructionRepository(TableRepository) :

    @staticmethod
    def search(connection, recipe_id):
        sql = 'SELECT * FROM Instructions WHERE recipe_id=?'
        cur = connection.cursor()
        cur.execute(sql, (recipe_id,))
        connection.commit() 
        return cur.fetchall()
        

    @staticmethod
    def insert(connection, entity, recipe_id):
        sql = 'INSERT INTO Instructions (recipe_id, instruction) VALUES(?,?)'
        cur = connection.cursor()
        cur.execute(sql, (recipe_id, entity.instruction, ))
        connection.commit()


    
class IngredientRepository(TableRepository) :
    @staticmethod
    def search(connection, recipe_id):
        sql = 'SELECT * FROM Ingredients WHERE recipe_id=?'
        cur = connection.cursor()
        cur.execute(sql, (recipe_id,))
        connection.commit() 
        return cur.fetchall()


    @staticmethod
    def insert(connection, entity, recipe_id):
        sql = 'INSERT INTO Ingredients (recipe_id, unit, quantity, ingredient) VALUES(?,?,?,?)'
        cur = connection.cursor()
        cur.execute(sql, (recipe_id, entity.unit, entity.quantity, entity.ingredient,))
        connection.commit()

class TagsRepository(TableRepository) :
    @staticmethod
    def search(connection, tag):
        sql = f'SELECT recipe_id FROM Tags WHERE tag="{tag} "'
        cur = connection.cursor()
        cur.execute(sql)
        print([int(value[0]) for value in cur.fetchall()])
        return [int(value[0]) for value in cur.fetchall()]

    @staticmethod
    def insert(connection, entity,recipe_id):
        sql = 'INSERT INTO Tags (recipe_id, tag) VALUES(?,?)'
        cur = connection.cursor()
        cur.execute(sql, (recipe_id, entity.tag))
        connection.commit()