from flask import flash

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))

def is_valid_extension(filename):
    valid_extensions = ['png', 'jpg']
    extension = filename.rsplit('.', 1)[1].lower()
    return extension in valid_extensions