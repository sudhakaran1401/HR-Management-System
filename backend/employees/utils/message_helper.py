def get_form_error(form):

    for errors in form.errors.values():

        for error in errors:

            return {
                "type": "error",
                "text": error
            }

    return {
        "type": "error",
        "text": "Invalid form data"
    }