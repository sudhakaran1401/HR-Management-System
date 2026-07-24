def build_message(message_type, text):

    return {
        "type": message_type,
        "text": text
    }


def extract_first_form_error(form):

    for errors in form.errors.values():
        for error in errors:
            return error

    return "Invalid form data"