from app.models.note import Note
from app.extensions import db
from sqlalchemy import or_
from app.utils.errors import NotFoundError, ValidationError

class NoteService:
    @staticmethod
    def get_all_notes(user_id, args):
        query = Note.query.filter_by(user_id=user_id)

        # 1. Search by title or content
        search = args.get('search')
        if search:
            search_pattern = f"%{search}%"
            query = query.filter(or_(Note.title.ilike(search_pattern), Note.content.ilike(search_pattern)))

        # 2. Filter by pinned status
        is_pinned = args.get('is_pinned')
        if is_pinned is not None:
            is_pinned_bool = is_pinned.lower() in ['true', '1', 't', 'y', 'yes']
            query = query.filter_by(is_pinned=is_pinned_bool)

        # 3. Sorting
        sort_by = args.get('sort_by', 'created_at')
        sort_order = args.get('sort_order', 'desc')
        
        if sort_by == 'title':
            order_col = Note.title
        elif sort_by == 'updated_at':
            order_col = Note.updated_at
        else:
            order_col = Note.created_at
            
        if sort_order == 'asc':
            query = query.order_by(order_col.asc())
        else:
            query = query.order_by(order_col.desc())

        # 4. Pagination
        page = args.get('page', 1, type=int)
        per_page = args.get('per_page', 10, type=int)

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return {
            "notes": [note.to_dict() for note in pagination.items],
            "total": pagination.total,
            "pages": pagination.pages,
            "current_page": pagination.page,
            "per_page": pagination.per_page,
            "has_next": pagination.has_next,
            "has_prev": pagination.has_prev
        }

    @staticmethod
    def get_note_by_id(user_id, note_id):
        note = Note.query.filter_by(id=note_id, user_id=user_id).first()
        if not note:
            raise NotFoundError("Note not found")
        return {"note": note.to_dict()}

    @staticmethod
    def create_note(user_id, data):
        title = data.get('title')
        content = data.get('content')

        if not title or not content:
            raise ValidationError("Title and content are required")

        new_note = Note(title=title, content=content, user_id=user_id)
        db.session.add(new_note)
        db.session.commit()

        return {"note": new_note.to_dict()}

    @staticmethod
    def update_note(user_id, note_id, data):
        note = Note.query.filter_by(id=note_id, user_id=user_id).first()
        if not note:
            raise NotFoundError("Note not found")

        title = data.get('title')
        content = data.get('content')
        is_pinned = data.get('is_pinned')

        if title is not None:
            note.title = title
        if content is not None:
            note.content = content
        if is_pinned is not None:
            note.is_pinned = is_pinned

        db.session.commit()
        return {"note": note.to_dict()}

    @staticmethod
    def delete_note(user_id, note_id):
        note = Note.query.filter_by(id=note_id, user_id=user_id).first()
        if not note:
            raise NotFoundError("Note not found")

        db.session.delete(note)
        db.session.commit()
        return {}
