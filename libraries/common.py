import os
import re

dirname = os.path.dirname(__file__)
userdata_file = os.path.join(dirname, '../userdata.jl')

fa_arrows = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAABj2lDQ1BJQ0MgcHJvZmlsZQAAKJF9kT1Lw1AUht+mFotUHHRQ6ZC' \
                b'hOogFURAHpyotgoXSVrDqYHLTDyFJQ5Li4ii4FhxEF78G/QGiq4OrIAiKIOLgL/BrkRLPTQIt0nrD5Tx57zkv95wLCOcq06yuCU' \
                b'DTbTObSojLhRWx+w0h+gQMISIxy0jnknl0XN8PCPB4H+denfParl6laDEgIBInmWHaxBXi6U3b4HxEPMAqkkJ8QTxu0gWJX7kue' \
                b'/zJueyyEOZs5rNzxFFisdzCcguziqkRzxLHFE0nf2HdY4XzNmdNrTH/nrzDSFFfylEcox1FCio2oMGAhSJEyKjRvwobcYo6KRay' \
                b'lJWg2bb3GXZ9MlQnu16MauZRJU/JdQB/i78ztkpTk55ThJxDL47zMQJ07wKNuuP8HDtO4wQIPgPXerO+SnOc+SK93tRih0Af9Xl' \
                b'509TkPeBqBxh8MiRTcqUgbaFUAt7P6LkKQP8d0LPqzc8/x+kjkN8CFm+B/QNgtEzeax36DvvzW0AamX9z/An+ApzfdJMMhO+eAA' \
                b'AABmJLR0QAxACJAMZ5NbLuAAAACXBIWXMAAA3XAAAN1wFCKJt4AAAAB3RJTUUH5AUFAhowK0+SbwAAAWtJREFUWMPFlz1PwzAQh' \
                b'p8GdkRYgK1lRpQysTGA4KcQ/mKRysZAQFRMUP4BbRBdCyrLRTImTuzgHied5MQf7+vzfdjQXvrARHSAsvSBKbAUnWmSsMFVSbjA' \
                b'VUg0ga+UxJ4svPTUGdD1WTjxJHABpAGEU+A8pgV2gRwoDF0YO15YfXfA9qodcmQQGLVdJKk58yvZ+V9lB8iAnu+EgeFweQQL5IZ' \
                b'jHvqEmunt8wgE5nUhmljg14HeHiopMDRJJBb4lkIq/0GiI42hY+efwI1joSNgU9rvwL1j3AmwXvG/AE4BXgMyXGydJNL4N+lIaL' \
                b'ic7wu4dczdBzak/QE8OcYdA2uOIzgrPw6AtwoTxQ7DX+FYRsFYHGKqYPVy5w92HhhLR6EFXlULHsUSJYnnCKAvLvA66QKXDSXV1' \
                b'weCi5FqOQ4pqSEXklzmRJOsRZbLYhLotbiURj9zV7JSfRs0kVB5HblIqL4PbRKq4FGf599e0upetDJv2wAAAABJRU5ErkJggg=='


def post_header():
    # I figure I'm basically printing this with every single console app, might as well put it in one spot, right?
    print("Cross - a Mastodon/Hubzilla cross-poster")
    print("       Holly Lotor Montalvo  2020       ")
    print("----------------------------------------", end="\n\n")


def get_instance_domain():
    instance = input("Please enter your instance's domain (i.e. example.com): ")
    instance = re.sub("^https?://", "", instance)  # Removes http(s) from the beginning.
    instance = re.sub("/.*$", "", instance)
    return instance