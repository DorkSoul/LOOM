"""
Recipes Routes - Recipe management and shopping lists
"""
from flask import render_template, request, jsonify
from app.modules.recipes import recipes_bp
from app.models.recipe import Recipe, RecipeIngredient, RecipeTag, ShoppingListItem
from app import db

@recipes_bp.route('/')
def index():
    """Recipes page"""
    return render_template('recipes/index.html')

@recipes_bp.route('/api/recipes', methods=['GET'])
def get_recipes():
    """Get all recipes"""
    category = request.args.get('category')
    cuisine = request.args.get('cuisine')
    search = request.args.get('search')

    query = Recipe.query

    if category:
        query = query.filter_by(category=category)

    if cuisine:
        query = query.filter_by(cuisine=cuisine)

    if search:
        query = query.filter(Recipe.name.contains(search) | Recipe.description.contains(search))

    recipes = query.order_by(Recipe.name).all()
    return jsonify([recipe.to_dict() for recipe in recipes])

@recipes_bp.route('/api/recipes/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    """Get a specific recipe"""
    recipe = Recipe.query.get_or_404(recipe_id)
    return jsonify(recipe.to_dict())

@recipes_bp.route('/api/recipes', methods=['POST'])
def create_recipe():
    """Create a new recipe"""
    data = request.get_json()

    recipe = Recipe(
        name=data['name'],
        description=data.get('description'),
        instructions=data.get('instructions'),
        prep_time=data.get('prep_time'),
        cook_time=data.get('cook_time'),
        servings=data.get('servings', 1),
        category=data.get('category'),
        cuisine=data.get('cuisine'),
        difficulty=data.get('difficulty', 'medium'),
        image_url=data.get('image_url')
    )

    db.session.add(recipe)
    db.session.flush()

    # Add ingredients
    if 'ingredients' in data:
        for ing_data in data['ingredients']:
            ingredient = RecipeIngredient(
                recipe_id=recipe.id,
                name=ing_data['name'],
                quantity=ing_data.get('quantity'),
                unit=ing_data.get('unit'),
                notes=ing_data.get('notes')
            )
            db.session.add(ingredient)

    # Add tags
    if 'tags' in data:
        for tag_name in data['tags']:
            tag = RecipeTag(recipe_id=recipe.id, tag_name=tag_name)
            db.session.add(tag)

    db.session.commit()

    return jsonify(recipe.to_dict()), 201

@recipes_bp.route('/api/recipes/<int:recipe_id>', methods=['PUT'])
def update_recipe(recipe_id):
    """Update a recipe"""
    recipe = Recipe.query.get_or_404(recipe_id)
    data = request.get_json()

    recipe.name = data.get('name', recipe.name)
    recipe.description = data.get('description', recipe.description)
    recipe.instructions = data.get('instructions', recipe.instructions)
    recipe.prep_time = data.get('prep_time', recipe.prep_time)
    recipe.cook_time = data.get('cook_time', recipe.cook_time)
    recipe.servings = data.get('servings', recipe.servings)
    recipe.category = data.get('category', recipe.category)
    recipe.cuisine = data.get('cuisine', recipe.cuisine)
    recipe.difficulty = data.get('difficulty', recipe.difficulty)

    db.session.commit()

    return jsonify(recipe.to_dict())

@recipes_bp.route('/api/recipes/<int:recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    """Delete a recipe"""
    recipe = Recipe.query.get_or_404(recipe_id)
    db.session.delete(recipe)
    db.session.commit()

    return '', 204

@recipes_bp.route('/api/shopping-list', methods=['GET'])
def get_shopping_list():
    """Get shopping list"""
    items = ShoppingListItem.query.order_by(ShoppingListItem.category, ShoppingListItem.name).all()
    return jsonify([item.to_dict() for item in items])

@recipes_bp.route('/api/shopping-list/from-recipe/<int:recipe_id>', methods=['POST'])
def add_recipe_to_shopping_list(recipe_id):
    """Add recipe ingredients to shopping list"""
    recipe = Recipe.query.get_or_404(recipe_id)

    for ingredient in recipe.ingredients:
        item = ShoppingListItem(
            name=ingredient.name,
            quantity=ingredient.quantity,
            unit=ingredient.unit,
            recipe_id=recipe.id
        )
        db.session.add(item)

    db.session.commit()

    return jsonify({'message': 'Ingredients added to shopping list'}), 201

@recipes_bp.route('/api/shopping-list/<int:item_id>', methods=['DELETE'])
def delete_shopping_item(item_id):
    """Delete a shopping list item"""
    item = ShoppingListItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()

    return '', 204
