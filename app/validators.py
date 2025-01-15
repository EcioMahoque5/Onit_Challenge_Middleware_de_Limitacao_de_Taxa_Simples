from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, ValidationError


class SetLimitsForm(FlaskForm):
    rate_limit = StringField('rate_limit', validators=[
        DataRequired(message="rate_limit is a required field!")])
    
    time_window = StringField('time_window', validators=[
        DataRequired(message="time_window is a required field!")])
    
    
    @staticmethod
    def validate_integer_field(value, field_name, min_value=1):
        """
            Valida se o campo pode ser convertido para inteiro e se está dentro dos limites.
        """
        try:
            converted_value = int(value)
            if converted_value < min_value:
                raise ValidationError(f"'{field_name}' must be at least {min_value}.")
            return converted_value
        except ValueError:
            raise ValidationError(f"'{field_name}' must be a valid integer.")

    def validate_rate_limit(self, field):
        self.rate_limit.data = self.validate_integer_field(field.data, "rate_limit")

    def validate_time_window(self, field):
        self.time_window.data = self.validate_integer_field(field.data, "time_window")