
class Search:
    __slots__ = ['__request', '__tags']


    def __init__(self) -> None:
        self.request = ''
        self.tags = list()

    def __str__(self) -> str:
        return f'{self.__request}, {self.__tags}'

    

    @property
    def request(self):
        return self.__request


    @request.setter
    def request (self, value):
        self.__request = value

    @property
    def tags(self):
        return self.__tags

    @tags.setter
    def tags (self, value):
        self.__tags = value



class Instruction:
    __slots__ = ['__receipt_id', '__instruction_pos', '__instruction']

    def __init__(self, instr_pos = 1, instr = "aboba") -> None:
        self.instruction_pos = instr_pos
        self.instruction = instr

    def __str__(self) -> str:
        return f"{self.receipt_id}, {self.instruction_pos}, {self.instruction}"


    @property
    def receipt_id(self):
        return self.__receipt_id

    @receipt_id.setter
    def receipt_id(self, value):
        self.__receipt_id = value

    @property
    def instruction_pos(self):
        return self.__instruction_pos

    @instruction_pos.setter
    def instruction_pos(self, value):
        self.__instruction_pos = value

    @property
    def instruction(self):
        return self.__instruction

    @instruction.setter
    def instruction(self, value):
        self.__instruction = value


class Ingredient:
    __slots__ = ['__receipt_id', '__ingredient_pos', '__unit', '__quantity', '__ingredient']

    def __init__(self, ingr_pos = 1, quantity = 1,  ingr = "aboba", unit = 'gramm') -> None:
        self.ingredient_pos = ingr_pos
        self.unit = unit
        self.quantity = quantity
        self.ingredient = ingr
    

    def __str__(self) -> str:
        return f"{self.receipt_id}, {self.ingredient_pos}, {self.unit}, {self.quantity}, {self.ingredient}"


    @property
    def receipt_id(self):
        return self.__receipt_id

    @receipt_id.setter
    def receipt_id(self, value):
        self.__receipt_id = value

    @property
    def ingredient_pos(self):
        return self.__ingredient_pos

    @ingredient_pos.setter
    def ingredient_pos(self, value):
        self.__ingredient_pos = value

    @property
    def unit(self):
        return self.__unit

    @unit.setter
    def unit(self, value):
        self.__unit = value

    @property
    def quantity(self):
        return self.__quantity

    @quantity.setter
    def quantity(self, value):
        self.__quantity = value

    @property
    def ingredient(self):
        return self.__ingredient

    @ingredient.setter
    def ingredient(self, value):
        self.__ingredient = value





class Recipe():
    __slots__ = ['__id', '__title', '__description', '__image', '__tags', '__ingredients', '__instructions', '__user_id']
    
    def __init__ (self, dict_, id):
        self.__id = id
        self.title = dict_['title']
        self.description =  dict_['description']
        self.image = dict_['image']
        self.tags = dict_['tags']
        self.ingredients = dict_['ingredients']
        self.instructions = dict_['instructions']
        self.user_id = dict_['user_id']

    def add_instruction(self, instruction):
        self.instructions.append(Instruction(self.id, len(self.instructions + 1), instruction))

    def add_ingredient(self, ingredient, unit):
        self.ingredients.append(Ingredient(self.id, len(self.ingredients + 1), ingredient, unit))

    def __str__(self) -> str:
        return f"{self.id}, {self.title}, {self.description}, {self.ingredients}, {self.instructions}"

    @property
    def tags(self):
        return self.__tags

    @tags.setter
    def tags (self, value):
        self.__tags = value

    @property
    def id(self):
        return self.__id

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, new_value):
        self.__title = new_value

    @property
    def description(self):
        return self.__description
        
    @description.setter
    def description(self, new_value):
        self.__description = new_value
    
    @property
    def ingredients(self):
        return self.__ingredients
        
    @ingredients.setter
    def ingredients(self, new_value):
        self.__ingredients = new_value

    @property
    def instructions(self):
        return self.__instructions

    @instructions.setter
    def instructions(self, new_value):
        self.__instructions = new_value

    @property
    def image(self):
        return self.__image

    @image.setter
    def image (self, value):
        self.__image = value

    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id (self, value):
        self.__user_id = value

class Tag:
    __slots__ = ['__tag']

    def __init__(self, tag) -> None:
        self.tag = tag

    @property
    def tag(self):
        return self.__tag

    @tag.setter
    def tag (self, value):
        self.__tag = value