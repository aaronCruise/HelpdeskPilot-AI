from pydantic import BaseModel, field_validator
from app.models.ticket import CATEGORIES, PRIORITIES

class RecommendationCreate(BaseModel):
    category: CATEGORIES
    priority: PRIORITIES
    summary: str
    recommended_step: str

    @field_validator('category')
    def validate_category(cls, category):
        if not category:
            raise ValueError('Category must be populated.')
        return category

    @field_validator('priority')
    def validate_priority(cls, priority):
        if not priority:
            raise ValueError('Priority must be populated.')
        return priority

    @field_validator('summary')
    def validate_summary(cls, summary):
        if not summary:
            raise ValueError('Summary must be populated.')
        return summary

    @field_validator('recommended_step')
    def validate_recommended_step(cls, recommended_step):
        if not recommended_step:
            raise ValueError('Recommended step must be populated.')
        return recommended_step