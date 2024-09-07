from datetime import datetime

import pymongo
from bson import ObjectId
from pydantic import BaseModel, Field, conint
from pymongo.errors import PyMongoError
from rest_framework.exceptions import ValidationError

from tastybook.managers import MongoManager
from tastybook.settings import DB


class RecipeNotFound(Exception):
    pass


class Recipe(BaseModel):
    name: str
    ingredients: dict[str, str]
    complexity: conint(ge=1, le=5)
    process: list[str]
    author: int
    is_vegan: bool
    created_at: str = Field(
        default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))

class RecipesManager(MongoManager):
    db = DB["recipes"]

    @classmethod
    def create_recipe(cls, recipe_data):
        new_recipe = Recipe.model_validate(recipe_data).model_dump()
        new_recipe_id = cls.db.insert_one(new_recipe).inserted_id
        return cls.get_recipe(new_recipe_id)

    @classmethod
    def get_recipe(cls, recipe_id):
        if ObjectId.is_valid(recipe_id):
            existing_recipe = cls.db.find_one(
                {
                    "_id": ObjectId(recipe_id)
                }
            )
            if not existing_recipe:
                raise RecipeNotFound("Recipe not found")
            return cls.id_to_string(existing_recipe)
        raise ValidationError("Invalid recipe id")

    @classmethod
    def get_all_recipes(cls):
        recipes = cls.db.find()
        return cls.to_list(recipes)

    @classmethod
    def update_recipe(cls, recipe_id, update_data):
        document = cls.db.find_one_and_update(
            {
                "_id": ObjectId(recipe_id)
            },
            {
                "$set": update_data
            },
            return_document=pymongo.ReturnDocument.AFTER
        )
        return cls.id_to_string(document)

    @classmethod
    def delete_recipe(cls, recipe_id):
        if ObjectId.is_valid(recipe_id):
            existing_recipe = cls.db.find_one_and_delete({"_id": ObjectId(recipe_id)})
            if not existing_recipe:
                raise RecipeNotFound("Recipe not found")
            return existing_recipe
        return ValidationError("Invalid recipe id")

    @classmethod
    def delete_recipes_by_credential(cls, query, **kwargs):
        try:
            result = cls.db.delete_many(query, **kwargs)
            return result.deleted_count
        except PyMongoError:
            return None

    @classmethod
    def recipe_filter(cls, query):
        cursor = cls.db.find(query)
        return cls.to_list(cursor)

    @classmethod
    def is_author(cls, user_id, recipe_id):
        recipe = cls.get_recipe(recipe_id)
        return recipe.get("author") == user_id
