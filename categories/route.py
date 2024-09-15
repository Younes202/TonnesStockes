from datetime import datetime
from typing import Optional
from database.connection import Database
from fastapi import APIRouter, HTTPException, Depends, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from .model import Category
from auth.authenticate import authenticate
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="templates")

category_router = APIRouter(
    tags=["Categories"]
)
category_database = Database(Category)


@category_router.post("/new_category")
async def add_category(
        request: Request,
        name: str = Form(...),
        description: Optional[str] = Form(None),
):
    try:
        # Create a new category with the provided information
        category = Category(
            name=name,
            description=description,
            creation_date=datetime.utcnow(),
        )

        # Save the new category to the database
        await category_database.save(category)
        request.session['submission_message'] = "User saved successfully"
        # Redirect to the page showing the list of parent categories
        return RedirectResponse(url="category_list", status_code=303)
    except Exception as e:
        print(f"Exception during save operation: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save the category to the database. Error: {str(e)}"
        )


# Update your FastAPI route to handle the form submission
@category_router.post("/edit_or_delete")
async def edit_or_delete_category(
    request: Request,
    action: str = Form(...),
    category_id: str = Form(...),
    name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
):
    try:
        if action == "delete":
            # Delete the category by its ID
            await category_database.delete(category_id)
            request.session['submission_message'] = "Category deleted successfully."
        elif action == "edit":
            # Fetch the category by its ID
            category = await Category.get(category_id)
            if category:
                # Update category details
                category.name = name
                category.description = description
                category.creation_date = datetime.utcnow()
                await category.save()
                request.session['submission_message'] = "Category updated successfully."
            else:
                raise HTTPException(status_code=404, detail="Category not found")
        else:
            raise HTTPException(status_code=400, detail="Invalid action")

        # Redirect to the page showing the list of categories
        return RedirectResponse(url="/category/category_list", status_code=303)

    except Exception as e:
        print(f"Exception during edit or delete operation: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process the action. Error: {str(e)}")



# Define your routes here
@category_router.get("/category_list", response_class=HTMLResponse, name="read_categories")
async def read_categories(request: Request):
    categories = await Category.find().to_list()
    return templates.TemplateResponse("categories/list_category.html", {"request": request, "categories": categories})