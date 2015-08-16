from django.shortcuts import render_to_response

def view(_):
    """ Summarize product information. """

    html_data = {}
    return render_to_response("products/index.html", html_data)
