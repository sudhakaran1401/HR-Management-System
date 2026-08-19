def leave_request( leave_requests, viewer_role ):

    return {
        "leave_requests": leave_requests,
        "page_obj": leave_requests,
        "viewer_role": viewer_role,
    }