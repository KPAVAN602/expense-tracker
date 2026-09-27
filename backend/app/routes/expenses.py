from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import Expense

expenses_bp = Blueprint("expenses", __name__)
def validate_expense_data(data, partial=False):
    errors = []

    if not partial or "amount" in data:
        amount = data.get("amount")
        if amount is None:
            errors.append("amount is required")
        elif not isinstance(amount, (int, float)) or isinstance(amount, bool):
            errors.append("amount must be a number")
        elif amount <= 0:
            errors.append("amount must be greater than 0")

    if not partial or "category" in data:
        category = data.get("category")
        if not category or not isinstance(category, str) or not category.strip():
            errors.append("category is required and must be a non-empty string")

    if not partial or "title" in data:
        title = data.get("title")
        if not title or not isinstance(title, str) or not title.strip():
            errors.append("title is required and must be a non-empty string")
    return errors

@expenses_bp.route('/expenses', methods=['GET'])
@jwt_required()
def get_expenses():
    user_id = get_jwt_identity()
    expense_id = request.args.get('id')
    query = Expense.query.filter_by(user_id=user_id)

    if expense_id:
        query = query.filter_by(id=expense_id)
    expenses = query.all()

    res = [
        {
            "id": e.id,
            "amount": e.amount,
            "category": e.category,
            "title": e.title,
            "created_at": e.created_at.isoformat() if e.created_at else None
        }
        for e in expenses
    ]
    return jsonify(res), 200


@expenses_bp.route('/expenses', methods=['POST'])
@jwt_required()
def create_expense():
    user_id = get_jwt_identity()
    data = request.get_json(silent=True) or {}

    errors = validate_expense_data(data)
    if errors:
        return jsonify({"errors": errors}), 400

    expense = Expense(
        amount=data["amount"],
        category=data["category"].strip(),
        title=data["title"].strip(),
        user_id=user_id
    )
    db.session.add(expense)
    db.session.commit()

    return jsonify({"message": "Expense added successfully", "id": expense.id}), 201

@expenses_bp.route('/expenses/<int:id>', methods=['PUT'])
@jwt_required()
def upd_expense(id):
    user_id = get_jwt_identity()
    expense = Expense.query.filter_by(id=id, user_id=user_id).first()

    if not expense:
        return jsonify({"message": "Expense not found"}), 404

    data = request.get_json(silent=True) or {}

    errors = validate_expense_data(data)
    if errors:
        return jsonify({"errors": errors}), 400

    expense.amount = data["amount"]
    expense.category = data["category"].strip()
    expense.title = data["title"].strip()

    db.session.commit()
    return jsonify({"message": "Expense updated successfully"}), 200


@expenses_bp.route('/expenses/<int:id>', methods=['PATCH'])
@jwt_required()
def update(id):
    user_id = get_jwt_identity()
    expense = Expense.query.filter_by(id=id, user_id=user_id).first()

    if not expense:
        return jsonify({"message": "Expense not found"}), 404

    data = request.get_json(silent=True) or {}

    if not data:
        return jsonify({"message": "No fields provided to update"}), 400

    errors = validate_expense_data(data, partial=True)
    if errors:
        return jsonify({"errors": errors}), 400

    if 'title' in data:
        expense.title = data['title'].strip()
    if 'amount' in data:
        expense.amount = data['amount']
    if 'category' in data:
        expense.category = data['category'].strip()

    db.session.commit()
    return jsonify({"message": "Expense updated successfully"}), 200


@expenses_bp.route('/expenses/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_expense(id):
    user_id = get_jwt_identity()
    expense = Expense.query.filter_by(id=id, user_id=user_id).first()

    if not expense:
        return jsonify({"message": "Expense not found"}), 404

    db.session.delete(expense)
    db.session.commit()
    return jsonify({"message": "Expense deleted successfully"}), 200