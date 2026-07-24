def get_first_form_error(form):

    for errors in form.errors.values():

        for error in errors:
            return error

    return "Invalid form data."