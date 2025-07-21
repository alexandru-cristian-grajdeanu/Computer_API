from pydantic import BaseModel, EmailStr, field_validator


class UserRegister(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    def password_strength(cls, value):
        import re
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must include at least one uppercase letter.")
        if not re.search(r"[a-z]", value):
            raise ValueError("Password must include at least one lowercase letter.")
        if not re.search(r"\d", value):
            raise ValueError("Password must include at least one number.")
        if not re.search(r"[@$!%*?&]", value):
            raise ValueError("Password must include at least one special character: @$!%*?&")
        return value
