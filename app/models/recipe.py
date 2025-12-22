"""
Recipe Model - Recipe management and meal planning
"""
from datetime import datetime
from app import db

class Recipe(db.Model):
    """Recipe model for storing recipes"""
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    instructions = db.Column(db.Text, nullable=True)
    prep_time = db.Column(db.Integer, nullable=True)  # Minutes
    cook_time = db.Column(db.Integer, nullable=True)  # Minutes
    servings = db.Column(db.Integer, default=1)
    category = db.Column(db.String(50), nullable=True)  # breakfast, lunch, dinner, dessert, etc.
    cuisine = db.Column(db.String(50), nullable=True)
    difficulty = db.Column(db.String(20), default='medium')  # easy, medium, hard
    image_url = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    ingredients = db.relationship('RecipeIngredient', backref='recipe', lazy=True, cascade='all, delete-orphan')
    tags = db.relationship('RecipeTag', backref='recipe', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Recipe {self.name}>'

    def to_dict(self):
        """Convert recipe to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'instructions': self.instructions,
            'prep_time': self.prep_time,
            'cook_time': self.cook_time,
            'servings': self.servings,
            'category': self.category,
            'cuisine': self.cuisine,
            'difficulty': self.difficulty,
            'image_url': self.image_url,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'ingredients': [i.to_dict() for i in self.ingredients],
            'tags': [t.tag_name for t in self.tags]
        }

class RecipeIngredient(db.Model):
    """Ingredients for recipes"""
    __tablename__ = 'recipe_ingredients'

    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.String(50), nullable=True)
    unit = db.Column(db.String(50), nullable=True)
    notes = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f'<RecipeIngredient {self.name}>'

    def to_dict(self):
        """Convert ingredient to dictionary"""
        return {
            'id': self.id,
            'recipe_id': self.recipe_id,
            'name': self.name,
            'quantity': self.quantity,
            'unit': self.unit,
            'notes': self.notes
        }

class RecipeTag(db.Model):
    """Tags for recipes"""
    __tablename__ = 'recipe_tags'

    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    tag_name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<RecipeTag {self.tag_name}>'

class ShoppingListItem(db.Model):
    """Shopping list items generated from recipes"""
    __tablename__ = 'shopping_list_items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.String(50), nullable=True)
    unit = db.Column(db.String(50), nullable=True)
    category = db.Column(db.String(50), nullable=True)
    is_purchased = db.Column(db.Boolean, default=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<ShoppingListItem {self.name}>'

    def to_dict(self):
        """Convert shopping list item to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'quantity': self.quantity,
            'unit': self.unit,
            'category': self.category,
            'is_purchased': self.is_purchased,
            'recipe_id': self.recipe_id,
            'created_at': self.created_at.isoformat()
        }
