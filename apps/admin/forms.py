# third-party imports
import re
from wtforms.validators import ValidationError
from wtforms import validators

def validate_url(form, field):
	if field.data:
		validator = validators.URL(require_tld=False)
		return validator.__call__(form, field)
